@echo off
echo ========================================
echo   Preparing IT180 PDF Generator
echo   for Cloud Deployment
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)

echo [OK] Python found
echo.

:: Verify all files
echo Verifying project files...
set ERRORS=0

if not exist "app.py" (
    echo [ERROR] app.py missing
    set /a ERRORS+=1
)
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt missing
    set /a ERRORS+=1
)
if not exist "Procfile" (
    echo [ERROR] Procfile missing
    set /a ERRORS+=1
)
if not exist "render.yaml" (
    echo [WARNING] render.yaml missing (optional)
)
if not exist "runtime.txt" (
    echo [WARNING] runtime.txt missing (optional)
)

if %ERRORS% GTR 0 (
    echo.
    echo [ERROR] Missing required files! Cannot proceed.
    pause
    exit /b 1
)

echo [OK] All required files present
echo.

:: Check template PDF
if exist "Templates\IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf" (
    echo [OK] Template PDF found in Templates folder
) else if exist "IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf" (
    echo [OK] Template PDF found in root folder
) else (
    echo [WARNING] Template PDF not found - app may not work correctly
)

:: Check logo
if exist "static\logo.webp" (
    echo [OK] Logo file found
) else (
    echo [WARNING] Logo file not found in static folder
)

echo.
echo ========================================
echo   Git Repository Setup
echo ========================================
echo.

git status >nul 2>&1
if errorlevel 1 (
    echo Git repository not initialized
    echo.
    set /p INIT="Initialize Git repository? (Y/N): "
    if /i "%INIT%"=="Y" (
        echo.
        echo Initializing Git...
        git init
        echo.
        echo Adding files...
        git add .
        echo.
        echo Creating initial commit...
        git commit -m "Initial commit - IT180 PDF Generator"
        echo.
        echo [OK] Git repository initialized!
        echo.
        echo [NEXT STEP] Create a GitHub repository and run:
        echo   git remote add origin YOUR_GITHUB_REPO_URL
        echo   git branch -M main
        echo   git push -u origin main
    )
) else (
    echo Git repository found
    echo.
    echo Current status:
    git status --short
    echo.
    set /p COMMIT="Commit all changes? (Y/N): "
    if /i "%COMMIT%"=="Y" (
        echo.
        git add .
        set /p MSG="Commit message (default: Update for deployment): "
        if "%MSG%"=="" set MSG=Update for deployment
        git commit -m "%MSG%"
        echo [OK] Changes committed
    )
)

echo.
echo ========================================
echo   Deployment Options
echo ========================================
echo.
echo Choose your deployment platform:
echo.
echo 1. Render.com (Recommended - Free tier available)
echo 2. Railway.app (Easy deployment)
echo 3. Replit (No Git needed)
echo 4. Show deployment instructions
echo 5. Exit
echo.
set /p CHOICE="Enter choice (1-5): "

if "%CHOICE%"=="1" (
    echo.
    echo Opening Render.com deployment guide...
    start https://render.com
    echo.
    echo See DEPLOY_NOW.md for step-by-step instructions
) else if "%CHOICE%"=="2" (
    echo.
    echo Opening Railway.app...
    start https://railway.app
    echo.
    echo Railway will auto-detect your Python app!
) else if "%CHOICE%"=="3" (
    echo.
    echo Opening Replit...
    start https://replit.com
    echo.
    echo Upload your files directly - no Git needed!
) else if "%CHOICE%"=="4" (
    if exist "DEPLOY_NOW.md" (
        start DEPLOY_NOW.md
    ) else (
        echo Deployment guide not found
    )
)

echo.
echo ========================================
echo   Preparation Complete!
echo ========================================
echo.
echo Your project is ready for deployment!
echo.
pause
