#!/usr/bin/env python3
"""Offline QQ Pet data CLI.

Commands:
  python cli.py status
  python cli.py raw
  python cli.py get pet.info.yb
  python cli.py set pet.info.yb 9999
  python cli.py backup
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
from pathlib import Path

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:  # pragma: no cover
    AES = None
    pad = None
    unpad = None

DEFAULT_KEY = "aes-256-cbc"


def find_store_path(custom_path: str = "") -> Path:
    if custom_path:
        path = Path(custom_path).expanduser()
        if path.exists():
            return path
        raise FileNotFoundError(f"store file not found: {path}")

    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        candidates = [
            Path(appdata) / "qq-pet-macos" / "config-macos.json",
            Path(appdata) / "pet" / "config.json",
            Path(appdata) / "pet" / "configDev.json",
        ]
    elif system == "Darwin":
        home = Path.home()
        candidates = [
            home / "Library" / "Application Support" / "qq-pet-macos" / "config-macos.json",
            home / "Library" / "Application Support" / "pet" / "config.json",
            home / "Library" / "Application Support" / "pet" / "configDev.json",
        ]
    else:
        home = Path.home()
        candidates = [
            home / ".config" / "qq-pet-macos" / "config-macos.json",
            home / ".config" / "pet" / "config.json",
            home / ".config" / "pet" / "configDev.json",
        ]

    for path in candidates:
        if path.exists():
            return path
    searched = ", ".join(str(p) for p in candidates)
    raise FileNotFoundError(f"QQ Pet store file was not found. Searched: {searched}")


def derive_key(encryption_key: str, iv: bytes) -> bytes:
    salt = iv.decode("latin1").encode("utf-8")
    return hashlib.pbkdf2_hmac("sha512", encryption_key.encode("utf-8"), salt, 10000, 32)


def is_plain_json(payload: bytes) -> bool:
    try:
        json.loads(payload.decode("utf-8"))
        return True
    except (ValueError, UnicodeDecodeError):
        return False


def read_store(path: Path, encryption_key: str) -> tuple[dict, bool]:
    payload = path.read_bytes()
    if not payload:
        return {}, False
    if is_plain_json(payload):
        return json.loads(payload.decode("utf-8")), False
    if len(payload) > 17 and payload[16:17] == b":":
        if AES is None:
            raise RuntimeError("pycryptodome is required: pip install -r requirements.txt")
        iv = payload[:16]
        ciphertext = payload[17:]
        key = derive_key(encryption_key, iv)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plain = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return json.loads(plain.decode("utf-8")), True
    raise ValueError("unknown store file format")


def write_store(path: Path, data: dict, encryption_key: str, encrypted: bool) -> None:
    raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
    if encrypted:
        if AES is None:
            raise RuntimeError("pycryptodome is required: pip install -r requirements.txt")
        iv = os.urandom(16)
        key = derive_key(encryption_key, iv)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        payload = iv + b":" + cipher.encrypt(pad(raw, AES.block_size))
    else:
        payload = raw
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(payload)
    os.replace(tmp, path)


def parse_value(raw: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def split_path(dotted: str) -> list[str]:
    parts = [part for part in dotted.split(".") if part]
    if not parts:
        raise ValueError("data path must not be empty")
    return parts


def get_value(data: dict, dotted: str):
    current = data
    for part in split_path(dotted):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted)
        current = current[part]
    return current


def set_value(data: dict, dotted: str, value) -> None:
    current = data
    parts = split_path(dotted)
    for part in parts[:-1]:
        if not isinstance(current, dict):
            raise ValueError(f"cannot descend into non-object segment: {part}")
        current = current.setdefault(part, {})
        if not isinstance(current, dict):
            raise ValueError(f"path segment is not an object: {part}")
    current[parts[-1]] = value


def load(args):
    path = find_store_path(args.store)
    data, encrypted = read_store(path, args.key)
    return path, data, encrypted


def cmd_status(args):
    path, data, encrypted = load(args)
    info = data.get("pet", {}).get("info", {})
    max_info = data.get("pet", {}).get("maxInfo", {})
    return {
        "store_path": str(path),
        "encrypted": encrypted,
        "name": info.get("name"),
        "host": info.get("host"),
        "growth": info.get("growth"),
        "level": max_info.get("level"),
        "hunger": info.get("hunger"),
        "clean": info.get("clean"),
        "health": info.get("health"),
        "mood": info.get("mood"),
        "yb": info.get("yb"),
    }


def cmd_raw(args):
    _path, data, _encrypted = load(args)
    return data


def cmd_get(args):
    path, data, _encrypted = load(args)
    return {"store_path": str(path), "path": args.path, "value": get_value(data, args.path)}


def cmd_set(args):
    path, data, encrypted = load(args)
    value = parse_value(args.value)
    set_value(data, args.path, value)
    if not args.no_backup:
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    write_store(path, data, args.key, encrypted)
    return {"success": True, "store_path": str(path), "path": args.path, "value": value}


def cmd_backup(args):
    path = find_store_path(args.store)
    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)
    return {"success": True, "backup_path": str(backup)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline QQ Pet data editor")
    parser.add_argument("--store", default="", help="custom store file path; auto-detect when empty")
    parser.add_argument("--key", default=DEFAULT_KEY, help="electron-store encryption key")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="show common pet fields").set_defaults(func=cmd_status)
    sub.add_parser("raw", help="print full raw store JSON").set_defaults(func=cmd_raw)

    get_p = sub.add_parser("get", help="get a value by dotted path")
    get_p.add_argument("path", help="example: pet.info.yb")
    get_p.set_defaults(func=cmd_get)

    set_p = sub.add_parser("set", help="set a value by dotted path")
    set_p.add_argument("path", help="example: pet.info.yb")
    set_p.add_argument("value", help="JSON value or string")
    set_p.add_argument("--no-backup", action="store_true", help="do not create config.json.bak")
    set_p.set_defaults(func=cmd_set)

    sub.add_parser("backup", help="copy store file to .bak").set_defaults(func=cmd_backup)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
