@echo off
REM Reset Auto-Sync Configuration to Defaults
REM This script deletes the saved auto-sync config so it will be recreated with new defaults (all disabled)

echo ========================================
echo Reset Auto-Sync Configuration
echo ========================================
echo.
echo This will delete your saved auto-sync settings.
echo The application will recreate them with all sync options DISABLED by default.
echo.
pause

set CONFIG_FILE=%USERPROFILE%\.automation_selector\auto_sync_config.xml

if exist "%CONFIG_FILE%" (
    echo.
    echo Deleting: %CONFIG_FILE%
    del "%CONFIG_FILE%"
    echo.
    echo [SUCCESS] Config file deleted!
    echo.
    echo Next time you open the application, all sync options will be disabled by default.
    echo You can enable individual options in Settings ^> Sync ^> Auto-Sync Settings if needed.
) else (
    echo.
    echo [INFO] Config file not found at: %CONFIG_FILE%
    echo It may have been already deleted or never created.
)

echo.
pause

