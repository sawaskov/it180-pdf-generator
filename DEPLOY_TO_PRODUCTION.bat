@echo off
title Deploy IT180 PDF Generator to Production
color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     IT180 PDF Generator - Production Deployment              ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Step 1: Verify files
echo [STEP 1/5] Verifying project files...
if not exist "app.py" (
    echo [ERROR] app.py not found!
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)
if not exist "Procfile" (
    echo [ERROR] Procfile not found!
    pause
    exit /b 1
)
echo [OK] All required files present
echo.

:: Step 2: Check Git
echo [STEP 2/5] Checking Git repository...
git status >nul 2>&1
if errorlevel 1 (
    echo [INFO] Initializing Git repository...
    git init
    git add .
    git commit -m "IT180 PDF Generator - Ready for deployment"
    echo [OK] Git initialized
) else (
    echo [OK] Git repository found
    git status --short
    echo.
    set /p commit="Commit all changes? (Y/N): "
    if /i "!commit!"=="Y" (
        git add .
        git commit -m "Update for production deployment"
        echo [OK] Changes committed
    )
)
echo.

:: Step 3: Check GitHub
echo [STEP 3/5] Checking GitHub connection...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] No GitHub repository configured
    echo.
    echo You need to create a GitHub repository first:
    echo   1. Go to: https://github.com/new
    echo   2. Create a new repository (make it PUBLIC for free Render.com)
    echo   3. Copy the repository URL
    echo.
    start https://github.com/new
    echo.
    set /p repo_url="Paste your GitHub repository URL here: "
    if "!repo_url!"=="" (
        echo [ERROR] No repository URL provided
        echo Please create a GitHub repository and try again
        pause
        exit /b 1
    )
    
    git remote add origin "!repo_url!"
    echo [OK] GitHub remote added
    echo.
) else (
    git remote get-url origin
    echo [OK] GitHub remote configured
    echo.
)

:: Step 4: Push to GitHub
echo [STEP 4/5] Pushing code to GitHub...
echo.
set /p push="Push code to GitHub now? (Y/N): "
if /i "!push!"=="Y" (
    git branch -M main 2>nul
    git push -u origin main 2>&1
    if errorlevel 1 (
        echo.
        echo [WARNING] Push failed. This might be normal if:
        echo - Repository already has code
        echo - Authentication required
        echo.
        echo You can push manually later using:
        echo   git push -u origin main
        echo.
    ) else (
        echo [OK] Code pushed to GitHub!
    )
) else (
    echo [INFO] Skipping push. You can push manually later.
)
echo.

:: Step 5: Deploy to Render
echo [STEP 5/5] Deploy to Render.com
echo.
echo ═══════════════════════════════════════════════════════════
echo   READY TO DEPLOY!
echo ═══════════════════════════════════════════════════════════
echo.
echo Your code is ready for deployment!
echo.
echo NEXT STEPS:
echo.
echo 1. Go to: https://render.com
echo 2. Sign up / Log in (use GitHub for easiest setup)
echo 3. Click "New +" ^> "Web Service"
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
set /p open="Open Render.com in browser? (Y/N): "
if /i "!open!"=="Y" (
    start https://render.com
    echo.
    echo Browser opened!
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   Deployment preparation complete!
echo ═══════════════════════════════════════════════════════════
echo.
pause
