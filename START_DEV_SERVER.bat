@echo off
title IT180 PDF Generator - Start Development Server
color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        IT180 PDF Generator - Development Server             ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check if server is already running
netstat -ano | findstr ":5000" >nul 2>&1
if not errorlevel 1 (
    color 0E
    echo [WARNING] Server is already running on port 5000!
    echo.
    echo The server appears to be running already.
    echo.
    echo Options:
    echo   1. Open browser: http://localhost:5000
    echo   2. Stop existing server first (run stop_server.bat)
    echo   3. Continue anyway (may cause conflicts)
    echo.
    set /p action="What would you like to do? (1/2/3): "
    
    if "!action!"=="1" (
        start http://localhost:5000
        echo.
        echo Browser opened. Server is running!
        echo Close this window to keep the server running.
        echo.
        pause
        exit /b 0
    )
    
    if "!action!"=="2" (
        call stop_server.bat
        echo.
        echo Waiting 3 seconds before starting new server...
        timeout /t 3 >nul
    )
    
    if "!action!"=="3" (
        echo Continuing with new server instance...
        echo [WARNING] This may cause port conflicts!
        timeout /t 2 >nul
    )
)

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [OK] Python found
echo.

:: Check dependencies
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    python -m pip install -r requirements.txt
    echo.
)

echo ═══════════════════════════════════════════════════════════
echo   Starting Development Server...
echo ═══════════════════════════════════════════════════════════
echo.
echo Server will be available at:
echo   http://localhost:5000
echo.
echo [IMPORTANT]
echo - Keep this window open while using the server
echo - Press Ctrl+C to stop the server
echo - The server will start in 3 seconds...
echo.
timeout /t 3 >nul

:: Start the server
python app.py

:: If we reach here, server stopped
echo.
echo ═══════════════════════════════════════════════════════════
echo   Server has stopped
echo ═══════════════════════════════════════════════════════════
pause
