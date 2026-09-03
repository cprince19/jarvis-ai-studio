# JARVIS AI Studio — Desktop Foundation

Windows desktop foundation for the JARVIS YouTube automation agent.

## Current milestone

- PySide6 desktop shell
- Dark JARVIS theme
- Dashboard
- Video Queue placeholder
- Settings placeholder
- SQLite job database
- Application logging
- JSON configuration
- PyInstaller specification
- Windows build script

## Run from source

```powershell
cd desktop
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Build the Windows executable

Run `build.bat` from the `desktop` directory. The executable will be created under `desktop/dist/Jarvis.exe`.

## Safety rule

The application is designed so the eventual YouTube uploader must stop at an explicit approval gate. `approval_required_for_upload` defaults to `true` and must remain enabled unless the user intentionally changes the policy.

## Next milestone

Folder monitoring, background workers, real video queue state, and drag/drop intake will be added next.
