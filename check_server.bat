@echo off
title Check Server Status
color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║        IT180 PDF Generator - Server Status Check            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check if port 5000 is in use
netstat -ano | findstr ":5000" >nul 2>&1
if errorlevel 1 (
    color 0E
    echo [STATUS] Server is NOT running
    echo.
    echo Port 5000 is not in use.
    echo.
    echo To start the server, run: START_DEV_SERVER.bat
    echo.
    pause
    exit /b 0
)

color 0A
echo [STATUS] Server IS running!
echo.

:: Get process info
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    set PID=%%a
)

if defined PID (
    echo Process ID: %PID%
    echo Port: 5000
    echo.
    echo Server should be accessible at:
    echo   http://localhost:5000
    echo.
    set /p open="Open in browser? (Y/N): "
    if /i "!open!"=="Y" (
        start http://localhost:5000
        echo.
        echo Browser opened!
    )
) else (
    echo [WARNING] Could not get process details
)

echo.
pause
