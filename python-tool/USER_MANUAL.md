QQ Pet Offline Tool Manual
==========================

Desktop app
-----------
Build the Windows portable exe from source:

  cd qq-pet-macos
  npm install
  $env:ELECTRON_MIRROR='https://npmmirror.com/mirrors/electron/'
  npm run build:win:portable

The generated exe is under:

  qq-pet-macos/dist/

Python data tool
----------------
The management tool is a single file:

  python-tool/cli.py

Install dependency once:

  cd python-tool
  pip install -r requirements.txt

Default data file on Windows:

  %APPDATA%\qq-pet-macos\config-macos.json

Use it after closing the desktop app:

  python cli.py status
  python cli.py raw
  python cli.py get pet.info.yb
  python cli.py set pet.info.yb 9999
  python cli.py set pet.info.name "MyPet"
  python cli.py set pet.info.isVip true
  python cli.py backup

Values are parsed as JSON first. Examples: 9999 is a number, true is a boolean,
and {"a":1} is an object. If parsing fails, the value is written as a string.

Notes
-----
Close the exe before editing data, then reopen it. This avoids the running app
overwriting local data after the CLI changes it.

This edition is offline-only. AI settings, DeepSeek config, local HTTP server,
WebSocket server, and network request dependency were removed.
