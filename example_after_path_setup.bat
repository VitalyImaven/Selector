@echo off
REM Example script after adding to PATH
REM This will work from ANY directory!

echo ========================================
echo  Example: Using AutomationStudioSelector from PATH
echo ========================================
echo.

echo Configuring OCB project for AS 4.5...

REM No full path needed - just the command!
AutomationStudioSelector.exe ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only

if %errorlevel% equ 0 (
    echo [OK] Project configured successfully!
) else (
    echo [ERROR] Configuration failed
    exit /b 1
)

pause
