@echo off
REM EVSU-OC IGP Sales Record System Launcher
REM This batch file runs the IGP Sales Record System

echo ========================================
echo EVSU-OC IGP Sales Record System
echo ========================================
echo.
echo Starting application...
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Run the Python application
python main.py

REM Pause if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Failed to start the application
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Python is not installed
    echo 2. Python is not in PATH
    echo 3. Missing files or dependencies
    echo.
    echo Please check the README.md for installation instructions.
    echo.
    pause
)
