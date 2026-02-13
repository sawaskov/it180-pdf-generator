@echo off
echo ========================================
echo   GitHub Repository Setup Helper
echo ========================================
echo.

:: Check if git is initialized
git status >nul 2>&1
if errorlevel 1 (
    echo Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit - IT180 PDF Generator"
    echo [OK] Git initialized
    echo.
)

:: Check for existing remote
git remote get-url origin >nul 2>&1
if not errorlevel 1 (
    echo Current GitHub remote:
    git remote get-url origin
    echo.
    set /p change="Change remote? (Y/N): "
    if /i "!change!"=="Y" (
        git remote remove origin
        goto :add_remote
    ) else (
        echo Keeping existing remote
        goto :push_code
    )
) else (
    :add_remote
    echo.
    echo [STEP 1] Create a GitHub repository:
    echo   1. Go to: https://github.com/new
    echo   2. Create a new repository (make it PUBLIC for free Render.com)
    echo   3. Copy the repository URL
    echo.
    start https://github.com/new
    echo.
    set /p repo_url="Enter your GitHub repository URL: "
    if "!repo_url!"=="" (
        echo No URL provided. Exiting.
        pause
        exit /b 1
    )
    
    git remote add origin "!repo_url!"
    echo [OK] Remote added
)

:push_code
echo.
echo [STEP 2] Pushing code to GitHub...
echo.

:: Check current branch
git branch --show-current >nul 2>&1
if errorlevel 1 (
    git checkout -b main
)

:: Try to push
git push -u origin main 2>&1
if errorlevel 1 (
    echo.
    echo [INFO] Push failed. Trying alternative...
    git branch -M main
    git push -u origin main
    if errorlevel 1 (
        echo.
        echo [ERROR] Could not push to GitHub
        echo.
        echo Common issues:
        echo - Repository doesn't exist yet
        echo - Authentication required (use GitHub Desktop or Git Credential Manager)
        echo - Branch name mismatch
        echo.
        echo You can manually push using:
        echo   git push -u origin main
        echo.
    ) else (
        echo [OK] Code pushed successfully!
    )
) else (
    echo [OK] Code pushed successfully!
)

echo.
echo ========================================
echo   GitHub Setup Complete!
echo ========================================
echo.
echo Your code is now on GitHub!
echo Next: Deploy to Render.com using deploy_to_render.bat
echo.
pause
