@echo off
git --version
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    pause
    exit /b 1
)
echo Git version check completed

set "REPO_URL=https://github.com/jiedi720/SubtitleToolbox.git"
set "BRANCH=main"

echo ======================================
echo Force overwrite current folder with GitHub repo
echo Repo: %REPO_URL%
echo Branch: %BRANCH%
echo ======================================
echo.
echo WARNING: This will DISCARD all local changes!
echo Press Ctrl+C to cancel, or any key to continue...
pause >nul

REM Initialize if not a git repo
if not exist ".git" (
    echo Current directory is not a Git repo, initializing...
    git init
    git remote add origin %REPO_URL%
)

echo Fetching remote repo...
echo [==========                    ] 25%% Fetching...
git fetch origin
if %errorlevel% neq 0 (
    echo ERROR: Failed to fetch from remote repository
    pause
    exit /b 1
)

echo Force overwriting local files...
echo [==================            ] 50%% Resetting...
git reset --hard origin/%BRANCH%
if %errorlevel% neq 0 (
    echo ERROR: Failed to reset to remote branch
    pause
    exit /b 1
)

echo Cleaning untracked files (except this batch file)...
echo [========================      ] 75%% Cleaning...
git clean -fd --exclude="GitClone.bat"

echo [============================] 100%% Complete!

echo.
echo Overwrite completed successfully
pause