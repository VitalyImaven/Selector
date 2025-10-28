@echo off
REM Build script for AS45 project
REM Version 1.3.0 - Enhanced with auto-detection of project path

echo ========================================
echo  Configuring AS45 Project
echo ========================================
echo.

REM Define the default/expected project path
set "DEFAULT_PROJECT_PATH=C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB"
REM To test auto-detection, comment out the line above with REM

REM Check if DEFAULT_PROJECT_PATH is defined and exists
if defined DEFAULT_PROJECT_PATH (
    if exist "%DEFAULT_PROJECT_PATH%\" (
        echo Using default project path: %DEFAULT_PROJECT_PATH%
        set "PROJECT_PATH=%DEFAULT_PROJECT_PATH%"
        goto :path_found
    )
)

REM Default path not set or doesn't exist - check if we're running from scripts directory
echo Default path not found or not set, attempting auto-detection...
    
    REM Get the current directory
    set "CURRENT_DIR=%~dp0"
    
    REM Check if we're in a 'scripts' directory
    echo Current directory: %CURRENT_DIR%
    
    REM Get parent directory (project root)
    for %%I in ("%CURRENT_DIR%\..") do set "PARENT_DIR=%%~fI"
    
    REM Check if parent directory looks like a project (contains .apj files)
    dir "%PARENT_DIR%\*.apj" /b >nul 2>&1
    if %errorlevel% equ 0 (
        echo Auto-detected project path: %PARENT_DIR%
        set "PROJECT_PATH=%PARENT_DIR%"
        goto :path_found
    )
)

REM If we reach here, neither method worked
echo ========================================
echo   ERROR: Cannot detect project path
echo ========================================
echo.
if defined DEFAULT_PROJECT_PATH (
    echo The default path does not exist:
    echo   %DEFAULT_PROJECT_PATH%
) else (
    echo No default path is configured.
)
echo.
echo Could not auto-detect a project in parent directory:
echo   %PARENT_DIR%
echo   ^(No .apj files found^)
echo.
echo Please either:
echo   1. Set the DEFAULT_PROJECT_PATH in this script
echo   2. Run this script from your project's \scripts directory
echo.
pause
exit /b 1

:path_found
echo.
echo Configuring AS45 project for AS 4.5...
echo Project path: %PROJECT_PATH%
echo.

python "C:\Work\Indigo\Python\Selector\Selector\main.py" ^
  -project-path "%PROJECT_PATH%" ^
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
    echo   - Project .apj from _as45.apj
    echo.
    echo Project ready at:
    echo   %PROJECT_PATH%
    echo.
    REM Your build commands here
) else (
    echo ========================================
    echo   Configuration FAILED
    echo ========================================
    exit /b 1
)

pause
