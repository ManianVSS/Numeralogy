@echo off
SETLOCAL

REM Check whether the virtual environment already exists.
IF EXIST .venv\Scripts\python.exe (
    echo Virtual environment already exists. Skipping creation and package installation.
) ELSE (
    echo Creating virtual environment...
    python -m venv .venv
    IF ERRORLEVEL 1 (
        echo Failed to create virtual environment. Ensure Python is installed and on PATH.
        EXIT /B 1
    )
    echo Activating virtual environment...
    call .venv\Scripts\activate
    IF ERRORLEVEL 1 (
        echo Failed to activate virtual environment.
        EXIT /B 1
    )
    echo Upgrading pip...
    python -m pip install --upgrade pip
    IF ERRORLEVEL 1 (
        echo Failed to upgrade pip.
        EXIT /B 1
    )
    echo Installing requirements...
    python -m pip install -r requirements.txt
    IF ERRORLEVEL 1 (
        echo Failed to install requirements from requirements.txt.
        EXIT /B 1
    )
)

REM Activate the environment and launch the application.
call .venv\Scripts\activate
IF ERRORLEVEL 1 (
    echo Failed to activate virtual environment.
    EXIT /B 1
)

echo Starting the Numeralogy application...
python numerology_pyqt.py
ENDLOCAL
