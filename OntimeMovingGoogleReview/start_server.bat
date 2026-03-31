@echo off
REM Quick start script for OnTime Moving Review System

echo.
echo ========================================
echo   OnTime Moving Review System
echo   Quick Start Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt -q

echo.
echo [3/4] Initializing database...
python review_manager.py init

echo.
echo [4/4] Starting API server...
echo.
echo ========================================
echo   Server will start at:
echo   http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python api_server.py

pause
