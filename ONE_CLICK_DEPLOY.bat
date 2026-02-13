@echo off
title IT180 PDF Generator - One Click Deploy
color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        IT180 PDF Generator - One Click Deployment           ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo This script will help you deploy your app to Render.com
echo.
pause

:: Verify files
echo.
echo [STEP 1] Verifying files...
if not exist "app.py" (
    echo ERROR: app.py not found!
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    pause
    exit /b 1
)
echo [OK] Files verified
echo.

:: Check Git
echo [STEP 2] Checking Git...
git status >nul 2>&1
if errorlevel 1 (
    echo Git not initialized. Initializing now...
    git init
    git add .
    git commit -m "Initial commit - Ready for deployment"
    echo.
    echo [IMPORTANT] You need to create a GitHub repository first!
    echo.
    set /p github_url="Enter your GitHub repository URL (or press Enter to skip): "
    if not "!github_url!"=="" (
        git remote add origin "!github_url!"
        git branch -M main
        echo.
        set /p push_now="Push to GitHub now? (Y/N): "
        if /i "!push_now!"=="Y" (
            git push -u origin main
        )
    ) else (
        echo.
        echo [INFO] To deploy, you need to:
        echo 1. Create a repo at: https://github.com/new
        echo 2. Run: git remote add origin YOUR_REPO_URL
        echo 3. Run: git push -u origin main
        echo.
    )
) else (
    echo [OK] Git repository found
    git status --short
    echo.
    set /p commit="Commit changes? (Y/N): "
    if /i "!commit!"=="Y" (
        git add .
        git commit -m "Update for deployment"
    )
)

echo.
echo [STEP 3] Opening Render.com...
echo.
echo Your deployment settings:
echo   Build Command: pip install -r requirements.txt
echo   Start Command: python app.py
echo   Environment: Python 3
echo   Plan: Free
echo.
echo Opening browser...
timeout /t 2 >nul
start https://render.com

echo.
echo ═══════════════════════════════════════════════════════════
echo   DEPLOYMENT INSTRUCTIONS
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Sign up / Log in to Render.com (if needed)
echo 2. Click "New +" button (top right)
echo 3. Select "Web Service"
echo 4. Connect your GitHub account
echo 5. Select your repository
echo 6. Configure:
echo    - Name: it180-pdf-generator
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: python app.py
echo    - Plan: Free
echo 7. (Optional) Add Environment Variable:
echo    - Key: SECRET_KEY
echo    - Value: (generate random string)
echo 8. Click "Create Web Service"
echo 9. Wait 2-5 minutes
echo 10. Get your public URL!
echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause
