@echo off
setlocal enabledelayedexpansion

:: --- CONFIGURATION ---
set "VENV_NAME=venv"
set "REQUIREMENTS=requirements.txt"
set "MAIN_SCRIPT=main.py"
set "ERROR_LOG=error_log_temp.txt"

:: --- CHECK FOR PYTHON ---
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed!
    pause
    exit /b
)

:: --- SETUP VENV (Only if missing) ---
if not exist "%VENV_NAME%" (
    echo Creating virtual environment...
    py -m venv %VENV_NAME%
    call %VENV_NAME%\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r %REQUIREMENTS%
    cls
) else (
    call %VENV_NAME%\Scripts\activate.bat
)

:RUN_SCRIPT
echo [INFO] Starting %MAIN_SCRIPT%...

python %MAIN_SCRIPT% 2> %ERROR_LOG%

if %errorlevel% neq 0 (
    echo.
    echo Script crashed. 
    
    :: Show the error to the user
    type %ERROR_LOG%
    echo.

    findstr /C:"ModuleNotFoundError" %ERROR_LOG% >nul 2>&1
    if !errorlevel! equ 0 (
        goto :INSTALL_AND_RETRY
    )
    
    findstr /C:"ImportError" %ERROR_LOG% >nul 2>&1
    if !errorlevel! equ 0 (
        goto :INSTALL_AND_RETRY
    )

    del %ERROR_LOG%
    pause
    exit /b
)

:: Clean exit
if exist %ERROR_LOG% del %ERROR_LOG%
pause
exit /b

:INSTALL_AND_RETRY
echo.
echo Missing library detected!
echo Installing requirements from %REQUIREMENTS%...
python -m pip install --upgrade pip
pip install -r %REQUIREMENTS%

echo.
echo Restarting script...
del %ERROR_LOG%
goto :RUN_SCRIPT
