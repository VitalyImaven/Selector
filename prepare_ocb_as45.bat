@echo off
REM Build script for OCB project with AS 4.5

echo ========================================
echo  Configuring OCB Project for AS 4.5
echo ========================================
echo.

echo Configuring OCB project for AS 4.5...

"C:\Program Files\Automation Studio Selector\AutomationStudioSelector.exe" ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only

echo.

if %errorlevel% equ 0 (
    echo ========================================
    echo  [OK] Project ready for AS 4.5
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
) else (
    echo ========================================
    echo  [ERROR] Configuration FAILED
    echo ========================================
    exit /b 1
)

pause
