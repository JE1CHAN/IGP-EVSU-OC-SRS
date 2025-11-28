@echo off
REM Database Initialization Script
REM Run this script once to set up the database with sample data

echo ========================================
echo EVSU-OC IGP Database Initialization
echo ========================================
echo.
echo This will create the database and add sample products.
echo.
pause

cd /d "%~dp0"

echo.
echo Initializing database...
echo.

python database/db_manager.py

if errorlevel 1 (
    echo.
    echo ERROR: Database initialization failed!
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo SUCCESS: Database initialized!
    echo ========================================
    echo.
    echo Sample products have been added:
    echo - T-Shirts (S, M, L, XL)
    echo - Polo Shirts (M, L)
    echo - Cap (One Size)
    echo.
    echo You can now run the main system.
    echo.
    pause
)
