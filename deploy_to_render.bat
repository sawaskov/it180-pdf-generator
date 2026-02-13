@echo off
echo ========================================
echo   IT180 PDF Generator - Deployment Tool
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11 or later
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

:: Check if required files exist
echo Checking required files...
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
if not exist "Templates\IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf" (
    if not exist "IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf" (
        echo [WARNING] Template PDF not found in expected locations
        echo Please ensure the PDF template is in the project folder
    )
)
if not exist "static\logo.webp" (
    echo [WARNING] Logo file not found in static folder
)

echo [OK] All required files found
echo.

:: Check if git is initialized
echo Checking Git repository...
git status >nul 2>&1
if errorlevel 1 (
    echo [INFO] Git repository not initialized
    echo.
    set /p init_git="Do you want to initialize Git repository? (Y/N): "
    if /i "%init_git%"=="Y" (
        echo Initializing Git repository...
        git init
        git add .
        git commit -m "Initial commit - IT180 PDF Generator ready for deployment"
        echo.
        echo [OK] Git repository initialized
        echo.
        echo [IMPORTANT] Next steps:
        echo 1. Create a new repository on GitHub (https://github.com/new)
        echo 2. Copy the repository URL
        echo 3. Run: git remote add origin YOUR_REPO_URL
        echo 4. Run: git push -u origin main
        echo.
    ) else (
        echo [INFO] Skipping Git initialization
        echo You can deploy manually via Render.com web interface
    )
) else (
    echo [OK] Git repository found
    echo.
    echo Checking for uncommitted changes...
    git status --short
    echo.
    set /p commit_changes="Do you want to commit all changes? (Y/N): "
    if /i "%commit_changes%"=="Y" (
        git add .
        set /p commit_msg="Enter commit message (or press Enter for default): "
        if "!commit_msg!"=="" set commit_msg=Update for deployment
        git commit -m "%commit_msg%"
        echo [OK] Changes committed
    )
)

echo.
echo ========================================
echo   Deployment Preparation Complete!
echo ========================================
echo.
echo NEXT STEPS TO DEPLOY:
echo.
echo 1. Go to https://render.com
echo 2. Sign up for free account (or log in)
echo 3. Click "New +" ^> "Web Service"
echo 4. Connect your GitHub account
echo 5. Select your repository
echo 6. Configure:
echo    - Name: it180-pdf-generator
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: python app.py
echo    - Plan: Free
echo 7. Add Environment Variable (optional):
echo    - Key: SECRET_KEY
echo    - Value: (generate a random string)
echo 8. Click "Create Web Service"
echo 9. Wait 2-5 minutes for deployment
echo 10. Get your public URL!
echo.
echo For detailed instructions, see DEPLOY_NOW.md
echo.
pause
