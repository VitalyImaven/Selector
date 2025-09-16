@echo off
echo ========================================
echo  Automation Studio Selector Builder
echo  Created by Vitaly Grosman
echo  Indigo R&D Division
echo ========================================
echo.

echo Step 1: Installing/Updating PyInstaller...
pip install --upgrade pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo Step 2: Building executable with PyInstaller...
pyinstaller automation_studio_selector.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo Step 3: Testing executable...
echo Testing if the executable runs...
timeout /t 2 /nobreak >nul
tasklist /fi "imagename eq AutomationStudioSelector.exe" 2>nul | find /i "AutomationStudioSelector.exe" >nul
if not errorlevel 1 (
    echo Closing any running instances...
    taskkill /f /im "AutomationStudioSelector.exe" 2>nul
)

echo.
echo Step 4: Creating installer directory...
if not exist "installer" mkdir installer

echo.
echo ========================================
echo  BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Executable location: dist\AutomationStudioSelector\AutomationStudioSelector.exe
echo.
echo To create Windows installer:
echo 1. Install Inno Setup from https://jrsoftware.org/isdl.php
echo 2. Open installer_script.iss with Inno Setup
echo 3. Click Build -^> Compile to create the installer
echo.
echo The installer will be created in the 'installer' folder
echo.
pause
