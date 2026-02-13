@echo off
title IT180 PDF Generator - Quick Deploy
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║   IT180 PDF Generator - Quick Deployment Assistant       ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Change to script directory
cd /d "%~dp0"

:: Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from python.org
    pause
    exit /b 1
)
python --version
echo [OK] Python found
echo.

:: Verify critical files
echo [2/5] Verifying project files...
if not exist "app.py" goto :missing_files
if not exist "requirements.txt" goto :missing_files
if not exist "Procfile" goto :missing_files
echo [OK] All critical files present
echo.

:: Check Git
echo [3/5] Checking Git repository...
git status >nul 2>&1
if errorlevel 1 (
    echo [INFO] No Git repository found
    echo.
    set /p init="Initialize Git? (Y/N): "
    if /i "!init!"=="Y" (
        echo Initializing Git...
        git init
        git add .
        git commit -m "Ready for deployment"
        echo [OK] Git initialized
    )
) else (
    echo [OK] Git repository found
    git status --short
    echo.
    set /p commit="Commit changes? (Y/N): "
    if /i "!commit!"=="Y" (
        git add .
        git commit -m "Update for deployment"
        echo [OK] Changes committed
    )
)
echo.

:: Generate deployment info
echo [4/5] Generating deployment information...
echo.
echo ═══════════════════════════════════════════════════════════
echo   DEPLOYMENT READY!
echo ═══════════════════════════════════════════════════════════
echo.
echo Your project is ready to deploy!
echo.
echo Recommended: Render.com (Free tier available)
echo.
echo Quick Steps:
echo   1. Go to: https://render.com
echo   2. Sign up / Log in
echo   3. Click "New +" ^> "Web Service"
echo   4. Connect GitHub and select your repo
echo   5. Use these settings:
echo      - Build: pip install -r requirements.txt
echo      - Start: python app.py
echo      - Plan: Free
echo   6. Deploy and get your URL!
echo.
echo ═══════════════════════════════════════════════════════════
echo.

:: Check if GitHub remote exists
echo [5/5] Checking GitHub connection...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] No GitHub remote configured
    echo.
    echo To connect to GitHub:
    echo   1. Create repo at: https://github.com/new
    echo   2. Run: git remote add origin YOUR_REPO_URL
    echo   3. Run: git push -u origin main
) else (
    git remote get-url origin
    echo [OK] GitHub remote configured
    echo.
    set /p push="Push to GitHub now? (Y/N): "
    if /i "!push!"=="Y" (
        git push -u origin main
        if errorlevel 1 (
            echo [INFO] Push failed - you may need to set upstream branch
            echo Try: git push -u origin main
        ) else (
            echo [OK] Code pushed to GitHub!
        )
    )
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   Next: Deploy at https://render.com
echo ═══════════════════════════════════════════════════════════
echo.
pause
exit /b 0

:missing_files
color 0C
echo [ERROR] Missing required files!
echo Please ensure app.py, requirements.txt, and Procfile exist
pause
exit /b 1
