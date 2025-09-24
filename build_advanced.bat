@echo off
echo ========================================
echo  Automation Studio Selector - Advanced Builder
echo  Created by Vitaly Grosman
echo  Indigo R&D Division
echo ========================================
echo.

:MENU
echo Please select build type:
echo.
echo 1. Quick Build (basic configuration)
echo 2. Development Build (debug enabled)
echo 3. Release Build (optimized)
echo 4. Single File Build (portable)
echo 5. Custom Build (advanced configuration)
echo 6. Exit
echo.
set /p choice=Enter your choice (1-6): 

if "%choice%"=="1" goto QUICK_BUILD
if "%choice%"=="2" goto DEV_BUILD
if "%choice%"=="3" goto RELEASE_BUILD
if "%choice%"=="4" goto SINGLE_FILE_BUILD
if "%choice%"=="5" goto CUSTOM_BUILD
if "%choice%"=="6" goto EXIT
echo Invalid choice. Please try again.
echo.
goto MENU

:QUICK_BUILD
echo.
echo ========================================
echo  QUICK BUILD - Basic Configuration
echo ========================================
pyinstaller automation_studio_selector.spec --clean --noconfirm
if errorlevel 1 goto BUILD_ERROR
goto BUILD_SUCCESS

:DEV_BUILD
echo.
echo ========================================
echo  DEVELOPMENT BUILD - Debug Enabled
echo ========================================
echo Creating development spec file...

REM Create a development version of the spec file
python -c "
import re
with open('automation_studio_selector_advanced.spec', 'r') as f:
    content = f.read()
content = re.sub(r'DEBUG_MODE = False', 'DEBUG_MODE = True', content)
content = re.sub(r'CONSOLE_MODE = False', 'CONSOLE_MODE = True', content)
content = re.sub(r'UPX_COMPRESSION = True', 'UPX_COMPRESSION = False', content)
with open('temp_dev.spec', 'w') as f:
    f.write(content)
"

pyinstaller temp_dev.spec --clean --noconfirm
del temp_dev.spec
if errorlevel 1 goto BUILD_ERROR
goto BUILD_SUCCESS

:RELEASE_BUILD
echo.
echo ========================================
echo  RELEASE BUILD - Optimized
echo ========================================
echo Creating release spec file...

REM Create a release version of the spec file
python -c "
import re
with open('automation_studio_selector_advanced.spec', 'r') as f:
    content = f.read()
content = re.sub(r'DEBUG_MODE = True', 'DEBUG_MODE = False', content)
content = re.sub(r'CONSOLE_MODE = True', 'CONSOLE_MODE = False', content)
content = re.sub(r'UPX_COMPRESSION = False', 'UPX_COMPRESSION = True', content)
content = re.sub(r'OPTIMIZE_SIZE = False', 'OPTIMIZE_SIZE = True', content)
with open('temp_release.spec', 'w') as f:
    f.write(content)
"

pyinstaller temp_release.spec --clean --noconfirm
del temp_release.spec
if errorlevel 1 goto BUILD_ERROR
goto BUILD_SUCCESS

:SINGLE_FILE_BUILD
echo.
echo ========================================
echo  SINGLE FILE BUILD - Portable Executable
echo ========================================
echo Creating single file spec...

python -c "
import re
with open('automation_studio_selector_advanced.spec', 'r') as f:
    content = f.read()

# Modify for single file
content = re.sub(
    r'exe = EXE\(\s*pyz,\s*a\.scripts,\s*\[\],\s*exclude_binaries=True,',
    'exe = EXE(\n    pyz,\n    a.scripts,\n    a.binaries,\n    a.zipfiles,\n    a.datas,\n    [],\n    exclude_binaries=False,',
    content,
    flags=re.DOTALL
)

# Remove COLLECT section
content = re.sub(r'coll = COLLECT\(.*?\)', '# Single file build - COLLECT section removed', content, flags=re.DOTALL)

with open('temp_single.spec', 'w') as f:
    f.write(content)
"

pyinstaller temp_single.spec --clean --noconfirm
del temp_single.spec
if errorlevel 1 goto BUILD_ERROR
goto BUILD_SUCCESS

:CUSTOM_BUILD
echo.
echo ========================================
echo  CUSTOM BUILD - Advanced Configuration
echo ========================================
echo Using advanced configuration file...
pyinstaller automation_studio_selector_advanced.spec --clean --noconfirm
if errorlevel 1 goto BUILD_ERROR
goto BUILD_SUCCESS

:BUILD_ERROR
echo.
echo ========================================
echo  BUILD FAILED!
echo ========================================
echo Check the error messages above.
echo Common solutions:
echo - Ensure all dependencies are installed
echo - Check that logo.png exists in assets folder
echo - Verify Python version compatibility
echo.
pause
goto MENU

:BUILD_SUCCESS
echo.
echo ========================================
echo  BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Executable location: dist\AutomationStudioSelector\
echo.

REM Test if executable exists and get its size
if exist "dist\AutomationStudioSelector\AutomationStudioSelector.exe" (
    for %%I in ("dist\AutomationStudioSelector\AutomationStudioSelector.exe") do set size=%%~zI
    set /a sizeMB=!size!/1024/1024
    echo Executable size: !sizeMB! MB
    echo.
) else (
    echo Warning: Executable not found!
)

echo Build Summary:
echo - Executable: dist\AutomationStudioSelector\AutomationStudioSelector.exe
echo - Dependencies: Included in dist\AutomationStudioSelector\ folder
echo - Data files: Logo and configuration examples included
echo.

set /p test=Do you want to test the executable? (y/n): 
if /i "%test%"=="y" (
    echo Starting executable for testing...
    start "" "dist\AutomationStudioSelector\AutomationStudioSelector.exe"
    echo.
    echo If the application starts successfully, the build is working!
)

echo.
set /p another=Build another configuration? (y/n): 
if /i "%another%"=="y" goto MENU

:EXIT
echo.
echo ========================================
echo  BUILD PROCESS COMPLETED
echo ========================================
echo.
echo Next steps:
echo 1. Test the executable on your development machine
echo 2. Test on a clean machine without Python
echo 3. Create installer using Inno Setup (installer_script.iss)
echo 4. Distribute the installer
echo.
echo Thank you for using Automation Studio Selector Builder!
pause

