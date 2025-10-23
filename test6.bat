@echo off
REM Build script for AS6 project

echo ========================================
echo  Configuring AS6 Project
echo ========================================
echo.

echo Configuring AS6 project for AS 6...

python "C:\Work\Indigo\Python\Selector\Selector\main.py" ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB" ^
  -studio-path "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe" ^
  -as-version 6 ^
  -prepare-only

echo.

if %errorlevel% equ 0 (
    echo ========================================
    echo   Project ready for AS 6
    echo ========================================
    echo.
    echo Files updated:
    echo   - Libraries copied from Libraries_6
    echo   - Physical.pkg from Physical_6.pkg
    echo   - OCB.apj from OCB_as6.apj
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

