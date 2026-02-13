@echo off
title Stop IT180 PDF Generator Server
color 0C
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║        IT180 PDF Generator - Stop Server                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check if port 5000 is in use
netstat -ano | findstr ":5000" >nul 2>&1
if errorlevel 1 (
    echo [INFO] No server found running on port 5000
    echo The server is not running.
    pause
    exit /b 0
)

echo [INFO] Found server running on port 5000
echo.

:: Get the process ID
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    set PID=%%a
)

if defined PID (
    echo Process ID: %PID%
    echo.
    set /p confirm="Stop the server? (Y/N): "
    if /i "%confirm%"=="Y" (
        echo.
        echo Stopping server...
        taskkill /PID %PID% /F >nul 2>&1
        if errorlevel 1 (
            echo [ERROR] Could not stop the server
            echo You may need to close the command window manually
        ) else (
            echo [OK] Server stopped successfully
        )
    ) else (
        echo Cancelled.
    )
) else (
    echo [ERROR] Could not find process ID
    echo You may need to close the command window manually
)

echo.
pause
