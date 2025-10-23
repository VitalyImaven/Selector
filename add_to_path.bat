@echo off
REM Add Automation Studio Selector to system PATH
REM This allows you to run "AutomationStudioSelector" from anywhere

echo ========================================
echo  Add Automation Studio Selector to PATH
echo ========================================
echo.

set SELECTOR_PATH=C:\Program Files\Automation Studio Selector

echo This will add the following directory to your system PATH:
echo   %SELECTOR_PATH%
echo.
echo After this, you can run from anywhere:
echo   AutomationStudioSelector.exe [options]
echo.
echo NOTE: You must run this script as Administrator!
echo.

set /p confirm=Continue? (yes/no): 

if /i not "%confirm%"=="yes" (
    echo Cancelled
    pause
    exit /b 0
)

echo.
echo Adding to PATH...

REM Add to system PATH
setx PATH "%PATH%;%SELECTOR_PATH%" /M

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  [OK] Successfully added to PATH!
    echo ========================================
    echo.
    echo IMPORTANT: You need to:
    echo   1. Close this command prompt
    echo   2. Open a NEW command prompt
    echo   3. Then you can use: AutomationStudioSelector.exe
    echo.
) else (
    echo.
    echo ========================================
    echo  [ERROR] Failed to add to PATH
    echo ========================================
    echo.
    echo Make sure you ran this script as Administrator
    echo Right-click -^> Run as administrator
    echo.
)

pause
