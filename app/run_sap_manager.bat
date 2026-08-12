@echo off
REM SAP Script Manager Launcher
REM Runs the application with correct Python installation

setlocal enabledelayedexpansion

set PYTHON_PATH=C:\Users\vg72934\AppData\Local\Programs\Python\Python311\python.exe
set APP_DIR=%~dp0

echo Starting SAP Script Manager...
echo.

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found at %PYTHON_PATH%
    echo Please install Python 3.11 from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if SAP.py exists
if not exist "%APP_DIR%SAP.py" (
    echo Error: SAP.py not found in directory
    pause
    exit /b 1
)

REM Check if sap_gui_manager.py exists
if not exist "%APP_DIR%sap_gui_manager.py" (
    echo Error: sap_gui_manager.py not found in directory
    pause
    exit /b 1
)

REM Add app directory to PYTHONPATH so imports work
set PYTHONPATH=%PYTHONPATH%;%APP_DIR%

REM Run the application
"%PYTHON_PATH%" "%APP_DIR%sap_gui_manager.py"

if errorlevel 1 (
    echo.
    echo Error running application
    pause
)

endlocal
