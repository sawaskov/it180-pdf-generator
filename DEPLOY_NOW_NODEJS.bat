@echo off
chcp 65001 >nul
title IT180 PDF Generator - Node.js Deployment Assistant
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║   IT180 PDF Generator - Node.js Deployment Assistant      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check if Git is installed
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

:: Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is not installed!
    echo.
    echo Please install Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo ✅ Git and Node.js are installed
echo.

:: Check if package.json exists
if not exist "package.json" (
    echo ❌ package.json not found!
    echo.
    echo Please ensure you're in the project root directory.
    echo.
    pause
    exit /b 1
)

echo ✅ Project files found
echo.

:: Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to install dependencies!
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
    echo.
)

:: Check if .git is initialized
if not exist ".git" (
    echo 🔧 Initializing Git repository...
    call git init
    echo ✅ Git repository initialized
    echo.
)

:: Check for required files
echo 📋 Checking required files...
if not exist "server.js" (
    echo ❌ server.js not found!
    pause
    exit /b 1
)
if not exist "Procfile" (
    echo ❌ Procfile not found!
    pause
    exit /b 1
)
if not exist ".gitignore" (
    echo ❌ .gitignore not found!
    pause
    exit /b 1
)
if not exist "Templates\IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf" (
    echo ⚠️  Warning: PDF template not found in Templates folder
    echo    Make sure to add it before deploying!
    echo.
)

echo ✅ All required files found
echo.

:: Show menu
:MENU
echo.
echo ┌─────────────────────────────────────────────────────────────┐
echo │  DEPLOYMENT OPTIONS                                         │
echo └─────────────────────────────────────────────────────────────┘
echo.
echo   1. Deploy to Render.com (Recommended - FREE)
echo   2. Deploy to Railway.app (FREE)
echo   3. Deploy to Vercel (FREE)
echo   4. Setup GitHub Repository
echo   5. View Deployment Guide
echo   6. Exit
echo.
set /p choice="Select an option (1-6): "

if "%choice%"=="1" goto RENDER
if "%choice%"=="2" goto RAILWAY
if "%choice%"=="3" goto VERCEL
if "%choice%"=="4" goto GITHUB
if "%choice%"=="5" goto GUIDE
if "%choice%"=="6" goto END
goto MENU

:RENDER
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  Deploy to Render.com                                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Step 1: Make sure your code is on GitHub
echo Step 2: Go to https://render.com
echo Step 3: Sign up (free) with GitHub
echo Step 4: Click "New +" → "Web Service"
echo Step 5: Connect your GitHub repository
echo Step 6: Configure:
echo    - Build Command: npm install
echo    - Start Command: npm start
echo    - Plan: Free
echo Step 7: Deploy!
echo.
echo Opening Render.com in your browser...
timeout /t 2 >nul
start https://render.com
echo.
pause
goto MENU

:RAILWAY
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  Deploy to Railway.app                                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Step 1: Make sure your code is on GitHub
echo Step 2: Go to https://railway.app
echo Step 2: Sign up (free) with GitHub
echo Step 3: Click "New Project" → "Deploy from GitHub repo"
echo Step 4: Select your repository
echo Step 5: Railway auto-detects Node.js!
echo.
echo Opening Railway.app in your browser...
timeout /t 2 >nul
start https://railway.app
echo.
pause
goto MENU

:VERCEL
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  Deploy to Vercel                                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Step 1: Make sure your code is on GitHub
echo Step 2: Go to https://vercel.com
echo Step 3: Sign up (free) with GitHub
echo Step 4: Click "New Project"
echo Step 5: Import your GitHub repository
echo Step 6: Vercel auto-detects Node.js!
echo.
echo Opening Vercel in your browser...
timeout /t 2 >nul
start https://vercel.com
echo.
pause
goto MENU

:GITHUB
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  Setup GitHub Repository                                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Step 1: Go to https://github.com/new
echo Step 2: Create a new repository (make it PUBLIC for free hosting)
echo Step 3: Copy the repository URL
echo.
set /p repo_url="Enter your GitHub repository URL: "

if "%repo_url%"=="" (
    echo ❌ No URL provided!
    pause
    goto MENU
)

echo.
echo 🔧 Setting up Git remote...
call git remote remove origin 2>nul
call git remote add origin %repo_url%
echo ✅ Remote added: %repo_url%
echo.

echo 📤 Do you want to commit and push your code now? (Y/N)
set /p push_choice="> "

if /i "%push_choice%"=="Y" (
    echo.
    echo 📝 Committing files...
    call git add .
    call git commit -m "Initial commit - Node.js IT180 PDF Generator" 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo ⚠️  No changes to commit or commit failed
    ) else (
        echo ✅ Files committed
    )
    
    echo.
    echo 📤 Pushing to GitHub...
    call git branch -M main
    call git push -u origin main
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Code pushed to GitHub!
        echo.
        echo Your repository is ready for deployment!
    ) else (
        echo ❌ Failed to push. Please check your Git credentials.
        echo.
        echo You may need to:
        echo 1. Set up Git credentials: git config --global user.name "Your Name"
        echo 2. Set up Git email: git config --global user.email "your.email@example.com"
        echo 3. Or use GitHub Desktop for easier setup
    )
)

echo.
pause
goto MENU

:GUIDE
echo.
echo Opening deployment guide...
if exist "DEPLOY_NODEJS.md" (
    start DEPLOY_NODEJS.md
) else (
    echo ❌ Deployment guide not found!
)
echo.
pause
goto MENU

:END
echo.
echo 👋 Goodbye! Good luck with your deployment!
echo.
timeout /t 2 >nul
exit /b 0
