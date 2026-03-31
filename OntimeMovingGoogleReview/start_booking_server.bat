@echo off
echo ================================================
echo OnTime Moving - Booking System Startup
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Starting the booking API server...
echo.
echo The server will be available at:
echo   - Website: http://localhost:5000
echo   - Booking Form: http://localhost:5000/contact.html
echo   - Admin Login: http://localhost:5000/login.html
echo   - Admin Dashboard: http://localhost:5000/admin
echo   - API: http://localhost:5000/api
echo.
echo ================================================
echo DEFAULT LOGIN CREDENTIALS
echo ================================================
echo Username: admin
echo Password: admin123
echo.
echo IMPORTANT: Change these credentials in production!
echo ================================================
echo.
echo Press Ctrl+C to stop the server
echo.

python booking_api.py

pause
