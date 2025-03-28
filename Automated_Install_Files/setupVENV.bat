@echo off
setlocal

:: Define the name of the virtual environment folder
set VENV_DIR=.\.venv

:: Define the path that the Embedded Python installation resides at
set PYTHON_PATH=.\python-win

:: Define the path to the Python interpreter
set PYTHON_INTRP=%PYTHON_PATH%\python.exe

:: Create static dir for python 
mkdir static

:: Check if the virtual environment directory exists
if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Virtual environment found.
) else (
    echo Virtual environment not found. Creating one...
    :: Check if the Python executable exists
    if exist "%PYTHON_INTRP%" (
        echo Python executable found at %PYTHON_INTRP%.
        :: Create the virtual environment
	  "%PYTHON_INTRP%" -m pip install virtualenv
        "%PYTHON_INTRP%" -m virtualenv %VENV_DIR%
        xcopy %PYTHON_PATH%\python39.zip %VENV_DIR%\Scripts\ /Y
    ) else (
        echo Python executable not found at %PYTHON_INTRP%.
        exit /b 1
    )
)