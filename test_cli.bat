@echo off
echo ========================================
echo  Automation Studio Selector - CLI Test
echo  Created by Vitaly Grosman
echo  Indigo R&D Division
echo ========================================
echo.

echo Test 1: Show version
echo ----------------------------------------
python main.py -version
echo.

echo Test 2: Show help
echo ----------------------------------------
python main.py -help
echo.

echo Test 3: List configured projects
echo ----------------------------------------
python main.py -list-projects
echo.

echo Test 4: List configured studios
echo ----------------------------------------
python main.py -list-studios
echo.

echo Test 5: Show status
echo ----------------------------------------
python main.py -status
echo.

echo Test 6: Show sync status
echo ----------------------------------------
python main.py -sync-status
echo.

echo Test 7: Show configuration
echo ----------------------------------------
python main.py -show-config
echo.

REM Uncomment to test project opening (requires configured project)
REM echo Test 8: Open project (example)
REM echo ----------------------------------------
REM python main.py -open YourProjectName -studio AS6
REM echo.

echo ========================================
echo  CLI Tests Completed
echo ========================================
echo.
echo To test with the built executable:
echo   dist\AutomationStudioSelector\AutomationStudioSelector.exe -help
echo.
pause
