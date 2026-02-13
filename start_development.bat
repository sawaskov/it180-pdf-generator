@echo off
title IT180 PDF Generator - Development Server
color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        IT180 PDF Generator - Development Server             ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from python.org
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

:: Check if port 5000 is already in use
netstat -ano | findstr ":5000" >nul 2>&1
if not errorlevel 1 (
    color 0E
    echo [WARNING] Port 5000 is already in use!
    echo.
    echo The server might already be running.
    echo.
    set /p continue="Do you want to continue anyway? (Y/N): "
    if /i not "!continue!"=="Y" (
        echo.
        echo To stop the existing server:
        echo 1. Find the Python process using port 5000
        echo 2. Or close the command window running the server
        echo.
        pause
        exit /b 1
    )
)

:: Check if required files exist
echo Checking required files...
if not exist "app.py" (
    color 0C
    echo [ERROR] app.py not found!
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo [WARNING] requirements.txt not found
    echo Installing dependencies manually...
    python -m pip install Flask pandas pypdf reportlab openpyxl Werkzeug
) else (
    echo [OK] requirements.txt found
    echo.
    set /p install="Install/Update dependencies? (Y/N): "
    if /i "!install!"=="Y" (
        echo.
        echo Installing dependencies...
        python -m pip install -r requirements.txt
        echo.
    )
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   Starting Development Server...
echo ═══════════════════════════════════════════════════════════
echo.
echo The server will start on: http://localhost:5000
echo.
echo [IMPORTANT] 
echo - Keep this window open while the server is running
echo - Press Ctrl+C to stop the server
echo - Open your browser and go to: http://localhost:5000
echo.
echo ═══════════════════════════════════════════════════════════
echo.
timeout /t 3 >nul

:: Start the Flask app
python app.py

:: If we get here, the server stopped
echo.
echo ═══════════════════════════════════════════════════════════
echo   Server stopped
echo ═══════════════════════════════════════════════════════════
echo.
pause
