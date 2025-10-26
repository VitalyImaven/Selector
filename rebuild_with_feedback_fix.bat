@echo off
REM ========================================
REM Rebuild Automation Studio Selector
REM with Fixed Feedback Feature
REM ========================================

echo.
echo ========================================
echo Rebuilding with Feedback Feature Fix
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ERROR: PyInstaller is not installed!
    echo Please install it with: pip install pyinstaller
    echo.
    pause
    exit /b 1
)

echo [1/3] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo       Done!
echo.

echo [2/3] Building executable with PyInstaller...
echo       This may take a few minutes...
echo.
pyinstaller automation_studio_selector_advanced.spec --clean
if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)
echo       Done!
echo.

echo [3/3] Verifying build...
if exist "dist\AutomationStudioSelector\AutomationStudioSelector.exe" (
    echo       Build successful!
    echo.
    echo ========================================
    echo BUILD COMPLETE!
    echo ========================================
    echo.
    echo Executable location:
    echo   dist\AutomationStudioSelector\AutomationStudioSelector.exe
    echo.
    echo To test the feedback feature:
    echo   1. Run the executable
    echo   2. Go to Help ^> Send Feedback/Report Issue...
    echo   3. Verify your email client opens
    echo.
) else (
    echo       ERROR: Executable not found!
    echo       Build may have failed.
    echo.
    pause
    exit /b 1
)

echo Do you want to open the dist folder? (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    explorer "dist\AutomationStudioSelector"
)

echo.
echo Press any key to exit...
pause >nul

