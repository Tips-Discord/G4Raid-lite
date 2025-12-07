@echo off
setlocal enabledelayedexpansion

set "VENV_NAME=venv"
set "REQUIREMENTS=requirements.txt"
set "MAIN_SCRIPT=main.py"

py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed!
    pause
    exit /b
)

if not exist "%VENV_NAME%" (
    echo Creating virtual environment...
    py -m venv %VENV_NAME%
)

call %VENV_NAME%\Scripts\activate.bat

set "TRIED_FIX=0"

:RUN_SCRIPT
echo  Starting %MAIN_SCRIPT%...
python %MAIN_SCRIPT%

if %errorlevel% neq 0 (
    echo.
    echo Script crashed.
    
    if exist "%VENV_NAME%\Lib\site-packages\curl_cffi" (
        pause
        exit /b
    )

    if "!TRIED_FIX!"=="0" (
        echo This might be a missing library. Attempting to install...

        python -m pip install --upgrade pip
        pip install -r %REQUIREMENTS%

        echo.
        echo Dependencies updated. Retrying script...

        set "TRIED_FIX=1"
        goto :RUN_SCRIPT
    ) else (
        echo Script crashed again after retry.
        echo Please run this file again to retry manually.
        pause
        exit /b
    )
)

echo.
pause
