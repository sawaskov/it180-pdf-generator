@echo off
title Deploy IT180 PDF Generator
color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║           IT180 PDF Generator - Deployment                   ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Choose an option:
echo.
echo   1. Quick Deploy (Recommended - Full automated setup)
echo   2. Setup GitHub Repository First
echo   3. Deploy to Render.com (After GitHub is set up)
echo   4. View Deployment Instructions
echo   5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" call quick_deploy.bat
if "%choice%"=="2" call setup_github.bat
if "%choice%"=="3" call deploy_to_render.bat
if "%choice%"=="4" (
    if exist "DEPLOY_NOW.md" (
        start DEPLOY_NOW.md
    ) else (
        echo.
        echo Deployment Instructions:
        echo.
        echo 1. Go to https://render.com
        echo 2. Sign up for free account
        echo 3. Click "New +" ^> "Web Service"
        echo 4. Connect GitHub and select your repo
        echo 5. Use: Build: pip install -r requirements.txt
        echo         Start: python app.py
        echo 6. Deploy and get your URL!
        echo.
        pause
    )
)
if "%choice%"=="5" exit
