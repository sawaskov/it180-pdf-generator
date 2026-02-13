@echo off
title Get Public URL - Quick Deploy
color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        Get Your Public URL - Quick Deployment                ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo This will help you deploy your app and get a public URL!
echo.
echo Choose your deployment method:
echo.
echo   1. Render.com (Recommended - FREE, Easy, 5 minutes)
echo   2. Railway.app (FREE, Auto-detects everything)
echo   3. Replit (FREE, No Git needed, Instant)
echo   4. Show step-by-step instructions
echo   5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto :render
if "%choice%"=="2" goto :railway
if "%choice%"=="3" goto :replit
if "%choice%"=="4" goto :instructions
if "%choice%"=="5" exit

:render
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo   Deploying to Render.com
echo ═══════════════════════════════════════════════════════════
echo.
echo Step 1: Prepare your code
call DEPLOY_TO_PRODUCTION.bat
if errorlevel 1 (
    echo.
    echo Preparation failed. Please check errors above.
    pause
    exit /b 1
)
echo.
echo Step 2: Opening Render.com...
start https://render.com
echo.
echo ═══════════════════════════════════════════════════════════
echo   FOLLOW THESE STEPS ON RENDER.COM:
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Sign up / Log in (use GitHub for easiest setup)
echo 2. Click "New +" ^> "Web Service"
echo 3. Connect GitHub ^> Select your repository
echo 4. Configure:
echo    - Name: it180-pdf-generator
echo    - Environment: Python 3
echo    - Build: pip install -r requirements.txt
echo    - Start: python app.py
echo    - Plan: Free
echo 5. Click "Create Web Service"
echo 6. Wait 2-5 minutes
echo 7. Get your URL: https://your-app-name.onrender.com
echo.
echo ═══════════════════════════════════════════════════════════
pause
exit /b 0

:railway
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo   Deploying to Railway.app
echo ═══════════════════════════════════════════════════════════
echo.
echo Step 1: Make sure your code is on GitHub
echo.
set /p on_github="Is your code on GitHub? (Y/N): "
if /i not "!on_github!"=="Y" (
    echo.
    echo Please push your code to GitHub first using DEPLOY_TO_PRODUCTION.bat
    pause
    exit /b 1
)
echo.
echo Opening Railway.app...
start https://railway.app
echo.
echo ═══════════════════════════════════════════════════════════
echo   FOLLOW THESE STEPS ON RAILWAY.APP:
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Sign up with GitHub
echo 2. Click "New Project"
echo 3. Select "Deploy from GitHub repo"
echo 4. Choose your repository
echo 5. Railway auto-detects everything!
echo 6. Get your URL instantly
echo.
pause
exit /b 0

:replit
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo   Deploying to Replit
echo ═══════════════════════════════════════════════════════════
echo.
echo Opening Replit...
start https://replit.com
echo.
echo ═══════════════════════════════════════════════════════════
echo   FOLLOW THESE STEPS ON REPLIT:
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Sign up (free)
echo 2. Click "Create Repl"
echo 3. Choose "Python" template
echo 4. Upload all your project files (drag and drop)
echo 5. In console, run: pip install -r requirements.txt
echo 6. Click "Run" button
echo 7. Get your public URL immediately!
echo.
echo ═══════════════════════════════════════════════════════════
pause
exit /b 0

:instructions
cls
if exist "PRODUCTION_DEPLOYMENT_GUIDE.md" (
    start PRODUCTION_DEPLOYMENT_GUIDE.md
) else (
    echo.
    echo Deployment Instructions:
    echo.
    echo See PRODUCTION_DEPLOYMENT_GUIDE.md for detailed steps
    echo.
    pause
)
exit /b 0
