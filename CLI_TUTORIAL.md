# Automation Studio Selector - CLI Tutorial

**Complete Guide to Command-Line Operations**

Created by: Vitaly Grosman  
Indigo R&D Division  
© 2025

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Basic Commands](#basic-commands)
4. [Project Operations](#project-operations)
5. [The Prepare-Only Mode](#the-prepare-only-mode)
6. [Real-World Examples](#real-world-examples)
7. [Automation Scripts](#automation-scripts)
8. [Troubleshooting](#troubleshooting)
9. [Quick Reference](#quick-reference)

---

## Introduction

The Automation Studio Selector can be controlled entirely from the command line, enabling:
- **Automation**: Batch processing and scheduled tasks
- **Scripting**: Integration with build scripts and workflows
- **Remote Operations**: Configure projects without GUI
- **CI/CD**: Integration with continuous integration pipelines

### **Two Modes of Operation:**

1. **GUI Mode**: No arguments → Opens the graphical interface
   ```bash
   AutomationStudioSelector.exe
   ```

2. **CLI Mode**: With arguments → Executes command and exits
   ```bash
   AutomationStudioSelector.exe -open MyProject -studio AS6
   ```

---

## Getting Started

### **Running CLI Commands**

There are three ways to run CLI commands depending on your situation:

#### **1. During Development (Python):**
```bash
python main.py -open OCB -studio AS45
```

#### **2. From Built Executable (dist folder):**
```bash
dist\AutomationStudioSelector\AutomationStudioSelector.exe -open OCB -studio AS45
```

#### **3. After Installation (Program Files):**
```bash
"C:\Program Files\Automation Studio Selector\AutomationStudioSelector.exe" -open OCB -studio AS45
```

### **Testing Your Setup:**

Try these commands to verify everything works:

```bash
# Show version
python main.py -version

# List your projects
python main.py -list-projects

# Show help
python main.py -help
```

---

## Basic Commands

### **📊 Information Commands**

#### **Show Version:**
```bash
python main.py -version
```
**Output:**
```
Automation Studio Selector v1.1.0
Created by Vitaly Grosman - Indigo R&D Division
© 2025
```

#### **List All Projects:**
```bash
python main.py -list-projects
```
**Output:**
```
Configured Projects:
--------------------------------------------------------------------------------
1. OCB
   Path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB
   Description: Migrated from single project configuration

2. As6
   Path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\As6
   Description: qqqqq

3. AS45
   Path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45
   Description: aaaaa
```

#### **List All Automation Studios:**
```bash
python main.py -list-studios
```
**Output:**
```
Configured Automation Studios:
--------------------------------------------------------------------------------
1. Automation Studio 4.5
   Executable: C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe

2. Automation Studio 6
   Executable: C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe
```

#### **List Everything:**
```bash
python main.py -list
```
Shows both projects and studios in one command.

#### **Application Status:**
```bash
python main.py -status
```
**Output:**
```
Automation Studio Selector - Status
================================================================================
Configured Studios: 2
Configured Projects: 3
Last Used Studio: 4.5
Last Used Project: OCB
```

#### **Show Configuration:**
```bash
python main.py -show-config
```
Shows complete configuration including all projects and studios.

---

## Project Operations

### **🚀 Opening Projects**

#### **Simple Form (Recommended):**
```bash
# Open OCB project with AS 4.5
python main.py OCB AS45

# Open As6 project with AS 6
python main.py As6 AS6

# Open AS45 project with AS 4.5
python main.py AS45 AS45
```

#### **Full Form:**
```bash
python main.py -open OCB -studio AS45
python main.py -open As6 -studio AS6
```

#### **Different Version Formats:**
All these work the same way:
```bash
python main.py OCB AS6        # AS6
python main.py OCB 6          # 6
python main.py OCB AS45       # AS45
python main.py OCB 4.5        # 4.5
python main.py OCB 45         # 45
```

### **🎯 Opening with Options**

#### **Silent Mode (No Output):**
```bash
python main.py OCB AS45 -silent
```
- No console output
- Returns exit code only
- Perfect for automation scripts

#### **Verbose Mode (Detailed Info):**
```bash
python main.py OCB AS45 -verbose
```
**Output:**
```
Opening project: OCB
Using AS: Automation Studio 4.5
Project path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB
✓ Project opened successfully with Automation Studio 4.5
```

#### **Wait for AS to Close:**
```bash
python main.py OCB AS45 -wait
```
- Opens Automation Studio
- Waits for you to close AS
- Then exits the CLI
- Useful for sequential operations

---

## The Prepare-Only Mode

### **🎯 What is Prepare-Only?**

The `-prepare-only` flag configures all project files for the selected AS version **WITHOUT** launching Automation Studio.

### **When to Use Prepare-Only:**

✅ **Batch processing** multiple projects  
✅ **Pre-configuration** before manual opening  
✅ **CI/CD pipelines** on build servers  
✅ **Scheduled tasks** via Task Scheduler  
✅ **Remote servers** without desktop GUI  
✅ **Testing** file operations  

### **Basic Usage:**

#### **Prepare OCB for AS 4.5:**
```bash
python main.py OCB AS45 -prepare-only
```

**Output:**
```
✓ Project prepared successfully for Automation Studio 4.5
  Files configured but Automation Studio NOT launched
```

#### **Prepare As6 for AS 6:**
```bash
python main.py As6 AS6 -prepare-only
```

#### **Silent Preparation (for scripts):**
```bash
python main.py OCB AS45 -prepare-only -silent
```
- No output
- Just does the work
- Returns exit code

#### **Verbose Preparation (see details):**
```bash
python main.py OCB AS45 -prepare-only -verbose
```

**Output:**
```
Preparing project: OCB
Using AS: Automation Studio 4.5
Project path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB
✓ Project prepared successfully for Automation Studio 4.5
  Files configured but Automation Studio NOT launched
  You can now manually open: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB\OCB.apj
```

### **What Prepare-Only Does:**

1. ✅ **Validates** project structure (checks Logical & Physical folders exist)
2. ✅ **Clears** the `Logical/Libraries` directory
3. ✅ **Copies** version-specific libraries:
   - For AS 4.5: `Libraries_45` → `Libraries`
   - For AS 6: `Libraries_6` → `Libraries`
4. ✅ **Updates** `Physical/Physical.pkg`:
   - For AS 4.5: copies from `Physical_45.pkg`
   - For AS 6: copies from `Physical_6.pkg`
5. ✅ **Updates** main project file `OCB.apj`:
   - For AS 4.5: copies from `OCB_as45.apj`
   - For AS 6: copies from `OCB_as6.apj`
6. ❌ **Does NOT** launch Automation Studio

### **After Preparation:**

The project is ready to be opened:
- **Double-click** `OCB.apj` in Windows Explorer
- **Or launch manually** with AS executable
- **Or use Selector GUI** to open
- All files are configured correctly for the chosen AS version

---

## Real-World Examples

### **Example 1: Morning Project Preparation**

**Scenario:** Prepare all your projects for AS 6 before starting work.

**Script (`morning_prep.bat`):**
```batch
@echo off
echo ========================================
echo  Morning Project Preparation
echo  Configuring all projects for AS 6
echo ========================================
echo.

echo Preparing OCB project...
python main.py OCB AS6 -prepare-only -silent
if %errorlevel% equ 0 (echo ✓ OCB ready) else (echo ✗ OCB failed)

echo Preparing As6 project...
python main.py As6 AS6 -prepare-only -silent
if %errorlevel% equ 0 (echo ✓ As6 ready) else (echo ✗ As6 failed)

echo Preparing AS45 project...
python main.py AS45 AS6 -prepare-only -silent
if %errorlevel% equ 0 (echo ✓ AS45 ready) else (echo ✗ AS45 failed)

echo.
echo ========================================
echo  All projects prepared for AS 6!
echo ========================================
pause
```

### **Example 2: Switch All Projects to AS 4.5**

**Scenario:** End of day, prepare all projects for AS 4.5 for tomorrow.

**Script (`switch_to_as45.bat`):**
```batch
@echo off
echo Switching all projects to AS 4.5...
echo.

for %%P in (OCB As6 AS45) do (
    echo Preparing %%P for AS 4.5...
    python main.py %%P AS45 -prepare-only -silent
    if errorlevel 1 (
        echo   ERROR: Failed to prepare %%P
    ) else (
        echo   ✓ %%P configured for AS 4.5
    )
)

echo.
echo All projects configured for AS 4.5
pause
```

### **Example 3: Open Project and Wait**

**Scenario:** Open project, work in AS, automatically sync when you close AS.

**Script (`work_session.bat`):**
```batch
@echo off
echo ========================================
echo  Starting Work Session
echo ========================================
echo.

echo Opening OCB with AS 4.5...
echo (Automation Studio will launch)
echo (Script will wait for you to close AS)
echo.

python main.py OCB AS45 -wait

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  Work session completed
    echo ========================================
    echo Your work has been automatically saved
) else (
    echo.
    echo ERROR: Failed to open project
)

pause
```

### **Example 4: Quick Project Switch**

**Scenario:** Quickly switch between projects during the day.

**Script (`quick_open.bat`):**
```batch
@echo off
echo Which project do you want to open?
echo.
echo 1. OCB (AS 4.5)
echo 2. OCB (AS 6)
echo 3. As6 (AS 6)
echo 4. AS45 (AS 4.5)
echo.
set /p choice=Enter choice (1-4): 

if "%choice%"=="1" python main.py OCB AS45
if "%choice%"=="2" python main.py OCB AS6
if "%choice%"=="3" python main.py As6 AS6
if "%choice%"=="4" python main.py AS45 AS45

pause
```

### **Example 5: Prepare for Manual Launch**

**Scenario:** Prepare project files, then launch AS with custom parameters.

**Script (`custom_launch.bat`):**
```batch
@echo off
echo Preparing OCB for AS 6...
python main.py OCB AS6 -prepare-only

if %errorlevel% equ 0 (
    echo.
    echo ✓ Project prepared successfully
    echo.
    echo Launching Automation Studio with custom parameters...
    
    REM Launch AS with your custom command-line arguments
    "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe" ^
        "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB\OCB.apj" ^
        /safe-mode ^
        /log-level debug
) else (
    echo ✗ Failed to prepare project
)

pause
```

---

## Automation Scripts

### **Daily Automated Preparation**

**Setup Windows Task Scheduler:**

1. **Create** `daily_prep.bat`:
```batch
@echo off
cd C:\Work\Indigo\Python\Selector\Selector
python main.py OCB AS6 -prepare-only -silent
python main.py As6 AS6 -prepare-only -silent
python main.py AS45 AS45 -prepare-only -silent
```

2. **Schedule** to run every weekday at 7:00 AM
3. **Result**: Projects are ready when you arrive

### **Build Server Integration**

**For automated builds on a build server:**

```batch
@echo off
REM build_pipeline.bat

echo ========================================
echo  Automated Build Pipeline
echo ========================================

REM Step 1: Prepare project
echo Step 1: Preparing project for AS 6...
"C:\Program Files\Automation Studio Selector\AutomationStudioSelector.exe" ^
    -open %PROJECT_NAME% -studio AS6 -prepare-only -silent

if %errorlevel% neq 0 (
    echo ERROR: Failed to prepare project
    exit /b 1
)

REM Step 2: Build project (your custom build command)
echo Step 2: Building project...
REM Add your AS build command here

REM Step 3: Run tests
echo Step 3: Running tests...
REM Add your test commands here

echo.
echo ========================================
echo  Build completed successfully!
echo ========================================
exit /b 0
```

### **Multi-Version Testing**

**Test project with both AS versions:**

```batch
@echo off
REM test_both_versions.bat

echo ========================================
echo  Multi-Version Testing
echo ========================================
echo.

REM Test with AS 4.5
echo Testing with AS 4.5...
python main.py OCB AS45 -prepare-only -silent
if %errorlevel% equ 0 (
    echo ✓ AS 4.5 configuration successful
    REM Add your AS 4.5 test commands here
) else (
    echo ✗ AS 4.5 configuration failed
    exit /b 1
)

echo.

REM Test with AS 6
echo Testing with AS 6...
python main.py OCB AS6 -prepare-only -silent
if %errorlevel% equ 0 (
    echo ✓ AS 6 configuration successful
    REM Add your AS 6 test commands here
) else (
    echo ✗ AS 6 configuration failed
    exit /b 1
)

echo.
echo ========================================
echo  All version tests passed!
echo ========================================
pause
```

### **Team Deployment Script**

**Deploy to team member's machines:**

```batch
@echo off
REM deploy_team_setup.bat

echo ========================================
echo  Team Member Setup
echo ========================================
echo.

REM Add your projects
echo Adding team projects...
python main.py -add-project -name "ProductionLine" -path "%SHARED_PROJECTS%\Production" -description "Main production system"
python main.py -add-project -name "Development" -path "%SHARED_PROJECTS%\Dev" -description "Development environment"
python main.py -add-project -name "Testing" -path "%SHARED_PROJECTS%\Test" -description "Test environment"

echo.
echo Preparing all projects for AS 6...
python main.py ProductionLine AS6 -prepare-only -silent
python main.py Development AS6 -prepare-only -silent
python main.py Testing AS6 -prepare-only -silent

echo.
echo ========================================
echo  Setup complete! Team member is ready.
echo ========================================
pause
```

---

## Project Management

### **Adding New Projects**

#### **Simple Form:**
```bash
python main.py -add-project MyProject C:\Projects\MyProject
```

#### **With Description:**
```bash
python main.py -add-project -name "TestProject" -path "C:\Projects\Test" -description "Testing environment"
```

**Output:**
```
✓ Project added: TestProject
  Path: C:\Projects\Test
```

### **Removing Projects**

#### **With Confirmation:**
```bash
python main.py -remove-project OldProject
```
**Prompts:**
```
Remove project 'OldProject'? (yes/no): yes
✓ Project removed: OldProject
```

#### **Force Remove (No Confirmation):**
```bash
python main.py -remove-project OldProject -force
```

**Important:** This only removes the project from the selector list. Your actual project files are **NOT deleted**.

---

## Advanced Usage

### **JSON Output for PowerShell**

```powershell
# Get projects as JSON
$json = python main.py -list-projects -json | ConvertFrom-Json

# Process each project
foreach ($project in $json) {
    Write-Host "Project: $($project.name)"
    Write-Host "Path: $($project.path)"
    Write-Host ""
}
```

### **Exit Code Checking**

```batch
@echo off
python main.py OCB AS45 -prepare-only -silent

if %errorlevel% equ 0 (
    echo Success
) else if %errorlevel% equ 1 (
    echo General error
) else if %errorlevel% equ 3 (
    echo Project not found
) else if %errorlevel% equ 4 (
    echo Studio not found
) else (
    echo Unknown error
)
```

### **Exit Codes Reference:**
- **0** = Success
- **1** = General error
- **2** = Configuration error
- **3** = Project not found
- **4** = Studio not found
- **130** = Cancelled by user (Ctrl+C)

---

## Troubleshooting

### **Common Issues**

#### **"Project not found: OCB"**

**Problem:** Project name doesn't match configured projects.

**Solutions:**
```bash
# List your projects to see exact names
python main.py -list-projects

# Use exact name from the list
python main.py "OCB" AS45
```

#### **"Studio not found: AS AS45"**

**Problem:** Version format issue (this was fixed).

**Solutions:**
```bash
# Use any of these formats (all work):
python main.py OCB AS45
python main.py OCB 4.5
python main.py OCB 45
```

#### **"Command not recognized"**

**Problem:** Python not in PATH or wrong directory.

**Solutions:**
```bash
# Use full Python path
C:\Python\python.exe main.py OCB AS45

# Or navigate to project directory first
cd C:\Work\Indigo\Python\Selector\Selector
python main.py OCB AS45
```

#### **QTimer Warnings**

**Problem:** "QObject::startTimer: Timers can only be used with threads started with QThread"

**Status:** These are harmless warnings in CLI mode. They don't affect functionality.

**Workaround:** Already fixed in the code - warnings should not appear anymore.

---

## Quick Reference Card

### **Essential Commands:**

| What You Want | Command |
|---------------|---------|
| Open with GUI | `AutomationStudioSelector.exe` |
| Open OCB with AS 4.5 | `python main.py OCB AS45` |
| Open OCB with AS 6 | `python main.py OCB AS6` |
| Prepare without launching | `python main.py OCB AS45 -prepare-only` |
| List all projects | `python main.py -list-projects` |
| List all studios | `python main.py -list-studios` |
| Show status | `python main.py -status` |
| Show help | `python main.py -help` |

### **Common Options:**

| Option | What It Does |
|--------|--------------|
| `-prepare-only` | Configure files but don't launch AS |
| `-wait` | Wait for AS to close before exiting |
| `-silent` | No output (automation mode) |
| `-verbose` | Detailed output (debugging) |
| `-json` | JSON output (for scripting) |
| `-force` | Skip confirmations |

### **Your Projects:**

Based on your screenshot:

| Project Name | Path | Command Example |
|--------------|------|-----------------|
| OCB | C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB | `python main.py OCB AS45` |
| As6 | C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\As6 | `python main.py As6 AS6` |
| AS45 | C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45 | `python main.py AS45 AS45` |

### **Your Studios:**

| Studio | Version Code | Command Example |
|--------|--------------|-----------------|
| Automation Studio 4.5 | AS45, 4.5, or 45 | `python main.py OCB AS45` |
| Automation Studio 6 | AS6, 6 | `python main.py OCB AS6` |

---

## Practical Batch Scripts

### **Script 1: Quick Project Launcher**

**File:** `launch.bat`
```batch
@echo off
REM Quick launcher for OCB project

:MENU
cls
echo ========================================
echo  OCB Project Launcher
echo ========================================
echo.
echo Select Automation Studio version:
echo.
echo 1. AS 4.5
echo 2. AS 6
echo 3. Prepare only (AS 4.5)
echo 4. Prepare only (AS 6)
echo 5. Exit
echo.
set /p choice=Enter choice (1-5): 

if "%choice%"=="1" goto AS45
if "%choice%"=="2" goto AS6
if "%choice%"=="3" goto PREP45
if "%choice%"=="4" goto PREP6
if "%choice%"=="5" goto EXIT

:AS45
echo Opening OCB with AS 4.5...
python main.py OCB AS45
pause
goto MENU

:AS6
echo Opening OCB with AS 6...
python main.py OCB AS6
pause
goto MENU

:PREP45
echo Preparing OCB for AS 4.5...
python main.py OCB AS45 -prepare-only
pause
goto MENU

:PREP6
echo Preparing OCB for AS 6...
python main.py OCB AS6 -prepare-only
pause
goto MENU

:EXIT
echo Goodbye!
```

### **Script 2: Project Status Checker**

**File:** `check_status.bat`
```batch
@echo off
cls
echo ========================================
echo  Automation Studio Selector Status
echo ========================================
echo.

echo CONFIGURED STUDIOS:
echo ----------------------------------------
python main.py -list-studios
echo.

echo CONFIGURED PROJECTS:
echo ----------------------------------------
python main.py -list-projects
echo.

echo APPLICATION STATUS:
echo ----------------------------------------
python main.py -status
echo.

pause
```

### **Script 3: All Projects to Same Version**

**File:** `sync_all_to_version.bat`
```batch
@echo off
echo ========================================
echo  Configure All Projects
echo ========================================
echo.

set /p version=Enter AS version (6 or 45): 

if "%version%"=="6" set AS_VER=AS6
if "%version%"=="45" set AS_VER=AS45

if not defined AS_VER (
    echo Invalid version
    pause
    exit /b 1
)

echo.
echo Preparing all projects for AS %version%...
echo.

for %%P in (OCB As6 AS45) do (
    echo [%%P] Preparing...
    python main.py %%P %AS_VER% -prepare-only -silent
    if errorlevel 1 (
        echo [%%P] ✗ FAILED
    ) else (
        echo [%%P] ✓ SUCCESS
    )
)

echo.
echo ========================================
echo  All projects configured for AS %version%
echo ========================================
pause
```

---

## Help System

### **General Help:**
```bash
python main.py -help
```

Shows all available commands and basic usage.

### **Command-Specific Help:**
```bash
python main.py -help open
python main.py -help sync
python main.py -help add-project
```

Shows detailed help for specific commands.

---

## Tips & Best Practices

### **✅ DO:**
- Use `-silent` in automated scripts
- Use `-verbose` when testing or debugging
- Use `-prepare-only` for batch operations
- Check exit codes in scripts
- Use `-list` to verify configuration before operations

### **❌ DON'T:**
- Don't run multiple AS versions on same project simultaneously
- Don't use prepare-only if you want AS to launch
- Don't ignore exit codes in automation scripts

### **💡 Pro Tips:**

1. **Create project-specific scripts**: Make `open_ocb_as45.bat`, `open_ocb_as6.bat`, etc.
2. **Use shortcuts**: Place batch scripts on desktop for one-click access
3. **Combine with Task Scheduler**: Automate morning preparation
4. **Check status first**: Run `-list` before complex operations
5. **Test in verbose mode**: Use `-verbose` first, then `-silent` in production

---

## Complete Working Example

**Scenario:** You work on OCB with AS 4.5 in the morning, switch to AS 6 in the afternoon.

**File:** `my_workflow.bat`
```batch
@echo off
title Automation Studio Workflow

:MENU
cls
echo ========================================
echo  My Daily Workflow
echo ========================================
echo.
echo Current Time: %TIME%
echo.
echo 1. Morning Setup (Prepare all for AS 4.5)
echo 2. Afternoon Setup (Prepare all for AS 6)
echo 3. Open OCB with AS 4.5
echo 4. Open OCB with AS 6
echo 5. Check Status
echo 6. Exit
echo.
set /p choice=Select option (1-6): 

if "%choice%"=="1" goto MORNING
if "%choice%"=="2" goto AFTERNOON
if "%choice%"=="3" goto OPEN_45
if "%choice%"=="4" goto OPEN_6
if "%choice%"=="5" goto STATUS
if "%choice%"=="6" goto END

:MORNING
echo.
echo Preparing all projects for AS 4.5...
python main.py OCB AS45 -prepare-only -silent
python main.py As6 AS45 -prepare-only -silent
python main.py AS45 AS45 -prepare-only -silent
echo ✓ Morning setup complete!
pause
goto MENU

:AFTERNOON
echo.
echo Preparing all projects for AS 6...
python main.py OCB AS6 -prepare-only -silent
python main.py As6 AS6 -prepare-only -silent
python main.py AS45 AS6 -prepare-only -silent
echo ✓ Afternoon setup complete!
pause
goto MENU

:OPEN_45
echo.
echo Opening OCB with AS 4.5...
python main.py OCB AS45
goto MENU

:OPEN_6
echo.
echo Opening OCB with AS 6...
python main.py OCB AS6
goto MENU

:STATUS
cls
echo ========================================
echo  Current Status
echo ========================================
echo.
python main.py -status
echo.
python main.py -list-projects
pause
goto MENU

:END
echo Goodbye!
```

---

## Summary

### **Key Points to Remember:**

1. **Simple Syntax**: `python main.py ProjectName ASVersion`
2. **Prepare-Only**: Add `-prepare-only` to configure without launching
3. **Silent Mode**: Add `-silent` for automation scripts
4. **Exit Codes**: Always check `%errorlevel%` in scripts
5. **Help Available**: Use `-help` for any command

### **Most Common Commands:**

```bash
# Open and launch AS
python main.py OCB AS45

# Prepare without launching
python main.py OCB AS45 -prepare-only

# Prepare silently (automation)
python main.py OCB AS45 -prepare-only -silent

# List everything
python main.py -list

# Get help
python main.py -help
```

---

**Created by Vitaly Grosman - Indigo R&D Division**  
**For support and questions, refer to the main USER_TUTORIAL.md**

