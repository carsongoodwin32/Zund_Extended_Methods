@echo off
setlocal

:: Get the directory of the batch file
set "BATCH_DIR=%~dp0"

:: Change the current directory to the batch file's directory
cd /d "%BATCH_DIR%"

:: Display the current directory (for confirmation)
echo Current directory is now: %CD%

:: Run getPython and setupVENV
powershell.exe -ExecutionPolicy Unrestricted -File "%BATCH_DIR%\Automated_Install_Files\getPython.ps1"
call "%BATCH_DIR%\Automated_Install_Files\setupVENV.bat"

:: Activate venv
call "%BATCH_DIR%\.venv\Scripts\activate.bat"
"%BATCH_DIR%\.venv\Scripts\python.exe" -m pip install -r "%BATCH_DIR%\requirements.txt"

:: Start the command prompt to allow you to use the virtual environment
"%BATCH_DIR%\.venv\Scripts\python.exe" "%BATCH_DIR%\ZEM.py"