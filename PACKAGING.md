# Running and Packaging

## Run the application

From the project root with the virtual environment activated:

```powershell
.venv\Scripts\activate
python main.py
```

Or in one line (PowerShell):

```powershell
.venv\Scripts\activate; python main.py
```

## Package to single-file .exe (PyInstaller)

1. Install PyInstaller in the project:

```powershell
.venv\Scripts\activate
uv add pyinstaller
```

2. Build a single-file, windowed executable (no console window):

```powershell
pyinstaller --onefile --windowed --name "TaskManager" main.py
```

The `.exe` will be in `dist/TaskManager.exe`.

3. If the app fails to start from the .exe (e.g. missing modules), add hidden imports:

```powershell
pyinstaller --onefile --windowed --name "TaskManager" ^
  --hidden-import=customtkinter ^
  --hidden-import=ui.main_window ^
  --hidden-import=ui.theme ^
  --hidden-import=ui.presenter ^
  --hidden-import=ui.task_dialog ^
  --hidden-import=ui.components.date_selector ^
  --hidden-import=ui.components.task_card ^
  --hidden-import=ui.components.search_bar ^
  --hidden-import=models ^
  --hidden-import=repository.database ^
  --hidden-import=repository.task_repository ^
  --hidden-import=repository.user_repository ^
  --hidden-import=services.task_service ^
  --hidden-import=services.user_service ^
  main.py
```

On Windows CMD (not PowerShell), use `^` for line continuation; in PowerShell use backtick `` ` ``.

4. The SQLite database `tasks.db` is created next to the executable when you first run the app. For a portable setup, run the .exe from a folder where it has write access (e.g. user's Documents or the same folder as the .exe).
