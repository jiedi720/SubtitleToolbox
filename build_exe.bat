@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   Universal PyInstaller Build Script (Directory Mode)
echo ============================================

REM Try to find .spec file in current directory
set SPEC_FILE=
for %%f in (*.spec) do (
    set SPEC_FILE=%%f
    goto :found_spec
)

:found_spec
if "%SPEC_FILE%"=="" (
    echo [Error] No .spec file found in current directory!
    pause
    exit /b 1
)

REM Extract project name from spec file (remove .spec extension)
set SCRIPT_NAME=%SPEC_FILE:.spec=%

REM Check if corresponding .py file exists
if not exist "%SCRIPT_NAME%.py" (
    echo [Error] %SCRIPT_NAME%.py not found!
    pause
    exit /b 1
)

echo [Info] Project name: %SCRIPT_NAME%
echo [Info] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo [Info] Installing dependencies from requirements.txt...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [Warning] requirements.txt not found, skipping dependency installation
)

REM Extract exe name from spec file
for /f "tokens=2 delims='" %%a in ('findstr /C:"name=" %SCRIPT_NAME%.spec') do (
    set EXE_NAME=%%a
    goto :found_name
)
:found_name

if "%EXE_NAME%"=="" (
    echo [Error] Could not find exe name in spec file!
    pause
    exit /b 1
)

echo [Info] Detected exe name: %EXE_NAME%
echo [Info] Starting build process with Directory mode (-D)...
echo [Info] Output directory: %EXE_NAME% (defined in spec file)
echo [Info] Build temp directory: C:\build_temp

REM Use Directory mode, output to current directory
REM The spec file's COLLECT name will determine the final folder name
python -m PyInstaller %SCRIPT_NAME%.spec --distpath="." --workpath="C:\build_temp\%SCRIPT_NAME%" --clean

if errorlevel 1 (
    echo [Error] Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Build completed successfully!
echo ============================================
echo Project: %SCRIPT_NAME%
echo Output directory: .\%EXE_NAME%\
echo Executable: .\%EXE_NAME%\%EXE_NAME%.exe
echo.
echo Note: This is Directory mode, all dependencies are in the same folder
echo       No temporary folder will be created during runtime
echo ============================================
pause