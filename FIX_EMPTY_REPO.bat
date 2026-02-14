@echo off
title Fix Empty GitHub Repository
color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        Fix Empty GitHub Repository Issue                     ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Your repository appears empty because code hasn't been pushed yet!
echo.
echo Current Git Configuration:
echo   Email: prinsloo_tfj@yahoo.com
echo   Name: Theuns
echo.
echo ═══════════════════════════════════════════════════════════
echo   STEP 1: Verify Your GitHub Account
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Go to: https://github.com
echo 2. Log in and check which account you're using
echo 3. Check if the email matches: prinsloo_tfj@yahoo.com
echo.
echo Do you want to open GitHub now? (Y/N)
set /p open_github="> "
if /i "%open_github%"=="Y" (
    start https://github.com
    echo.
    echo Browser opened! Check your account and repositories.
    echo.
    timeout /t 3 >nul
)
echo.
echo ═══════════════════════════════════════════════════════════
echo   STEP 2: Find or Create Your Repository
echo ═══════════════════════════════════════════════════════════
echo.
echo Do you already have a repository for this project? (Y/N)
set /p has_repo="> "
if /i "%has_repo%"=="Y" (
    echo.
    echo Please provide your GitHub repository URL.
    echo It should look like: https://github.com/USERNAME/REPO_NAME.git
    echo.
    set /p repo_url="Repository URL: "
    if not "!repo_url!"=="" (
        echo.
        echo Adding remote repository...
        git remote remove origin 2>nul
        git remote add origin "!repo_url!"
        echo [OK] Remote added: !repo_url!
        echo.
        goto :push_code
    ) else (
        echo [ERROR] No URL provided
        pause
        exit /b 1
    )
) else (
    echo.
    echo You need to create a repository first:
    echo 1. Go to: https://github.com/new
    echo 2. Repository name: it180-pdf-generator (or any name)
    echo 3. Make it PUBLIC (for free Render.com)
    echo 4. DO NOT initialize with README
    echo 5. Click "Create repository"
    echo 6. Copy the repository URL
    echo.
    start https://github.com/new
    echo.
    echo Browser opened! Create your repository and copy the URL.
    echo.
    timeout /t 5 >nul
    echo.
    set /p repo_url="Paste your repository URL here: "
    if not "!repo_url!"=="" (
        echo.
        echo Adding remote repository...
        git remote remove origin 2>nul
        git remote add origin "!repo_url!"
        echo [OK] Remote added: !repo_url!
        echo.
        goto :push_code
    ) else (
        echo [ERROR] No URL provided
        pause
        exit /b 1
    )
)

:push_code
echo.
echo ═══════════════════════════════════════════════════════════
echo   STEP 3: Push Your Code to GitHub
echo ═══════════════════════════════════════════════════════════
echo.
echo Ready to push your code to GitHub!
echo.
echo This will upload all your committed code to GitHub.
echo.
set /p push_now="Push code now? (Y/N): "
if /i "!push_now!"=="Y" (
    echo.
    echo Pushing code to GitHub...
    echo.
    git branch -M main
    git push -u origin main
    if errorlevel 1 (
        echo.
        echo [WARNING] Push failed. Possible reasons:
        echo - Authentication required (GitHub login)
        echo - Repository permissions issue
        echo - Network connection problem
        echo.
        echo You may need to:
        echo 1. Use GitHub Desktop for easier authentication
        echo 2. Or set up a Personal Access Token
        echo 3. Or use SSH keys
        echo.
        echo Try pushing manually:
        echo   git push -u origin main
        echo.
    ) else (
        echo.
        echo ═══════════════════════════════════════════════════════════
        echo   SUCCESS! Your code is now on GitHub!
        echo ═══════════════════════════════════════════════════════════
        echo.
        echo Your repository should no longer be empty!
        echo You can now deploy to Render.com
        echo.
    )
) else (
    echo.
    echo [INFO] Skipping push. You can push manually later using:
    echo   git push -u origin main
    echo.
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   Summary
echo ═══════════════════════════════════════════════════════════
echo.
echo Your local git is configured with: prinsloo_tfj@yahoo.com
echo.
echo Make sure you're using the SAME GitHub account when:
echo - Creating the repository
echo - Connecting to Render.com
echo.
echo If you have two GitHub accounts:
echo - Use the one that matches prinsloo_tfj@yahoo.com
echo - OR change your git config to match the other account
echo.
pause
