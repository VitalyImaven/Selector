@echo off
REM Build script for AS45 project

echo ========================================
echo  Configuring AS45 Project
echo ========================================
echo.

echo Configuring AS45 project for AS 4.5...

python "C:\Work\Indigo\Python\Selector\Selector\main.py" ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only

echo.

if %errorlevel% equ 0 (
    echo ========================================
    echo   Project ready for AS 4.5
    echo ========================================
    echo.
    echo Files updated:
    echo   - Libraries copied from Libraries_45
    echo   - Physical.pkg from Physical_45.pkg
    echo   - OCB.apj from OCB_as45.apj
    echo.
    echo Project ready at:
    echo   C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB\OCB.apj
    echo.
    REM Your build commands here
) else (
    echo ========================================
    echo   Configuration FAILED
    echo ========================================
    exit /b 1
)

pause
