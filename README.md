# QQ Pet Offline

Offline Windows desktop build of QQ Pet, with AI and backend server code removed.

## What is included

- `qq-pet-macos/`: Electron desktop app source.
- `python-tool/cli.py`: single-file local data editor.
- `python-tool/USER_MANUAL.md`: usage manual.

## Build the exe

```powershell
cd qq-pet-macos
npm install
$env:ELECTRON_MIRROR='https://npmmirror.com/mirrors/electron/'
npm run build:win:portable
```

The exe is generated in `qq-pet-macos/dist/`.

## Use the Python tool

```powershell
cd python-tool
pip install -r requirements.txt
python cli.py status
python cli.py set pet.info.yb 9999
```

Default data file on Windows: `%APPDATA%\qq-pet-macos\config-macos.json`. Close the desktop app before editing data, then reopen it.

## Removed

- AI chat settings
- DeepSeek API key/model settings
- LLM module
- Express HTTP server
- WebSocket server
- axios dependency
