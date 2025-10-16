# Automation Studio Selector - CLI Usage Guide

## 🖥️ Command-Line Interface

The Automation Studio Selector now supports command-line operations for automation, scripting, and advanced workflows.

---

## 🚀 Quick Start

### **Basic Usage:**
```bash
# Open GUI (no arguments)
AutomationStudioSelector.exe

# Open project with AS 6 (simple form)
AutomationStudioSelector.exe MyProject AS6

# Open project with AS 4.5
AutomationStudioSelector.exe MyProject AS45
```

---

## 📋 Complete Command Reference

### **Project Operations**

#### **Open Project:**
```bash
# Full form
AutomationStudioSelector.exe -open MyProject -studio AS6

# Short form
AutomationStudioSelector.exe MyProject AS6

# With options
AutomationStudioSelector.exe -open MyProject -studio AS6 -wait -verbose

# Use last selected studio
AutomationStudioSelector.exe -open MyProject
```

**Options:**
- `-studio` or `-s`: AS version (AS6, AS45, 6, 4.5)
- `-prepare-only`: Prepare files but DON'T launch Automation Studio
- `-wait`: Wait for AS to close before exiting
- `-silent`: Suppress output
- `-verbose`: Show detailed information

#### **List Projects:**
```bash
# Text format
AutomationStudioSelector.exe -list-projects

# JSON format (for scripting)
AutomationStudioSelector.exe -list-projects -json
```

**Output Example:**
```
Configured Projects:
--------------------------------------------------------------------------------
1. ProductionLine
   Path: C:\Projects\Production\MainLine
   Description: Main production control system

2. TestSystem
   Path: C:\Projects\Test\System
```

#### **List Studios:**
```bash
# Text format
AutomationStudioSelector.exe -list-studios

# JSON format
AutomationStudioSelector.exe -list-studios -json
```

#### **List Everything:**
```bash
# Show both projects and studios
AutomationStudioSelector.exe -list
```

---

### **Project Management**

#### **Add New Project:**
```bash
# Full form
AutomationStudioSelector.exe -add-project -name "NewProject" -path "C:\Projects\New"

# With description
AutomationStudioSelector.exe -add-project -name "TestProj" -path "C:\Test" -description "Test environment"

# Short form (name then path)
AutomationStudioSelector.exe -add-project MyProject C:\Projects\MyProject
```

**Requirements:**
- Path must exist
- Must contain Logical and Physical subdirectories

#### **Remove Project:**
```bash
# With confirmation prompt
AutomationStudioSelector.exe -remove-project MyOldProject

# Skip confirmation
AutomationStudioSelector.exe -remove-project MyOldProject -force
```

**Note:** This only removes from the selector list. Your actual project files are NOT deleted.

---

### **Synchronization**

#### **Manual Sync:**
```bash
# Sync current project
AutomationStudioSelector.exe -sync

# Sync specific project
AutomationStudioSelector.exe -sync MyProject

# Verbose sync
AutomationStudioSelector.exe -sync MyProject -verbose
```

#### **Sync Status:**
```bash
# Text format
AutomationStudioSelector.exe -sync-status

# JSON format
AutomationStudioSelector.exe -sync-status -json
```

---

### **Information & Status**

#### **Application Status:**
```bash
# General status
AutomationStudioSelector.exe -status

# JSON output
AutomationStudioSelector.exe -status -json
```

**Shows:**
- Number of configured studios
- Number of configured projects
- Last used studio
- Last used project

#### **Configuration:**
```bash
# Show complete configuration
AutomationStudioSelector.exe -show-config

# JSON format
AutomationStudioSelector.exe -show-config -json
```

#### **Version Information:**
```bash
AutomationStudioSelector.exe -version
```

**Output:**
```
Automation Studio Selector v1.1.0
Created by Vitaly Grosman - Indigo R&D Division
© 2025
```

#### **Help:**
```bash
# General help
AutomationStudioSelector.exe -help

# Help for specific command
AutomationStudioSelector.exe -help open
AutomationStudioSelector.exe -help sync
AutomationStudioSelector.exe -help add-project
```

---

## 🎯 Common Use Cases

### **Daily Workflow:**
```bash
# Morning: Open your main project
AutomationStudioSelector.exe ProductionLine AS6

# Check what's available
AutomationStudioSelector.exe -list

# Sync before going home
AutomationStudioSelector.exe -sync ProductionLine
```

### **Automation Script:**
```batch
@echo off
echo Opening project with AS 6...
AutomationStudioSelector.exe -open MyProject -studio AS6 -wait -silent

if %errorlevel% equ 0 (
    echo Project closed successfully
    AutomationStudioSelector.exe -sync MyProject -silent
    echo Sync completed
) else (
    echo Failed to open project
    exit /b 1
)
```

### **Build Pipeline:**
```batch
@echo off
REM Open project and wait for build
AutomationStudioSelector.exe %PROJECT_NAME% AS6 -wait -silent
if %errorlevel% neq 0 exit /b 1

REM Sync changes
AutomationStudioSelector.exe -sync %PROJECT_NAME% -silent
if %errorlevel% neq 0 exit /b 1

echo Build completed successfully
```

### **Multi-Project Workflow:**
```batch
@echo off
echo Syncing all projects before backup...

AutomationStudioSelector.exe -sync Project1 -silent
AutomationStudioSelector.exe -sync Project2 -silent
AutomationStudioSelector.exe -sync Project3 -silent

echo All projects synced
```

---

## 🎯 Prepare-Only Mode

### **What is Prepare-Only Mode?**

The `-prepare-only` flag performs all file preparation steps without launching Automation Studio. This is perfect for automation scenarios where you want to configure files but launch AS separately or manually.

### **Usage:**
```bash
# Simple form
AutomationStudioSelector.exe MyProject AS6 -prepare-only

# Full form
AutomationStudioSelector.exe -open MyProject -studio AS6 -prepare-only

# Silent mode for scripts
AutomationStudioSelector.exe MyProject AS6 -prepare-only -silent
```

### **What It Does:**
1. ✅ **Validates project structure** (checks for Logical & Physical folders)
2. ✅ **Clears Libraries directory** (removes old active files)
3. ✅ **Copies version-specific libraries** (e.g., Libraries_6 → Libraries)
4. ✅ **Updates Physical.pkg** (from Physical_6.pkg or Physical_45.pkg)
5. ✅ **Updates OCB.apj** (from OCB_as6.apj or OCB_as45.apj)
6. ❌ **Does NOT launch Automation Studio**

### **Use Cases:**

#### **Batch Preparation:**
```batch
@echo off
echo Preparing all projects for AS 6...
AutomationStudioSelector.exe Project1 AS6 -prepare-only -silent
AutomationStudioSelector.exe Project2 AS6 -prepare-only -silent
AutomationStudioSelector.exe Project3 AS6 -prepare-only -silent
echo All projects prepared!
```

#### **CI/CD Pipeline:**
```batch
@echo off
echo Configuring project for build server...
AutomationStudioSelector.exe %PROJECT% AS6 -prepare-only -silent
if %errorlevel% equ 0 (
    echo Project prepared - ready for automated build
) else (
    echo Failed to prepare project
    exit /b 1
)
```

#### **Pre-Configuration:**
```batch
@echo off
echo Pre-configuring projects before team arrives...
for %%P in (Project1 Project2 Project3) do (
    echo Preparing %%P...
    AutomationStudioSelector.exe %%P AS6 -prepare-only -silent
)
echo All projects ready for use!
```

#### **Manual Launch:**
```batch
@echo off
REM Prepare files
AutomationStudioSelector.exe MyProject AS6 -prepare-only

REM Launch AS manually (with custom parameters)
"C:\BrAutomation\AS6\bin-en\AutomationStudio.exe" "C:\Projects\MyProject\OCB.apj" /custom-args
```

### **Benefits:**
- **Automation**: Configure projects without GUI interaction
- **Batch Operations**: Prepare multiple projects quickly
- **Remote Operations**: Configure on servers without desktop access
- **Testing**: Verify file operations without launching AS
- **CI/CD**: Integrate into build pipelines
- **Scheduling**: Use with Task Scheduler for automated preparation

---

## 🔧 Advanced Features

### **JSON Output for Scripting:**
```bash
# Get project list as JSON
AutomationStudioSelector.exe -list-projects -json > projects.json

# Parse in PowerShell
$projects = AutomationStudioSelector.exe -list-projects -json | ConvertFrom-Json
foreach ($project in $projects) {
    Write-Host $project.name
}
```

### **Exit Codes:**
- `0` - Success
- `1` - General error
- `2` - Configuration error
- `3` - Project not found
- `4` - Studio not found
- `130` - Cancelled by user (Ctrl+C)

### **Error Handling in Scripts:**
```batch
@echo off
AutomationStudioSelector.exe MyProject AS6

if %errorlevel% equ 0 (
    echo Success
) else if %errorlevel% equ 3 (
    echo Project not found
) else if %errorlevel% equ 4 (
    echo Studio not found
) else (
    echo Unknown error: %errorlevel%
)
```

---

## 💡 Tips & Tricks

### **Shorthand Commands:**
```bash
# Instead of this:
AutomationStudioSelector.exe -open MyProject -studio AS6

# Use this:
AutomationStudioSelector.exe MyProject AS6
```

### **Silent Mode for Scripts:**
```bash
# No output, just exit codes
AutomationStudioSelector.exe MyProject AS6 -silent
```

### **Verbose for Debugging:**
```bash
# Detailed output for troubleshooting
AutomationStudioSelector.exe -open MyProject -studio AS6 -verbose
```

### **Wait for Completion:**
```bash
# Wait for AS to close before continuing
AutomationStudioSelector.exe MyProject AS6 -wait
```

---

## 📊 Logging

All CLI operations are logged to the same log files as GUI operations:
- **Application log**: `%USERPROFILE%\.automation_selector\logs\application.log`
- **Session logs**: `%USERPROFILE%\.automation_selector\logs\session_*.log`

---

## 🔍 Troubleshooting CLI

### **"Invalid command or arguments"**
- Check command spelling
- Use `-help` to see available commands
- Ensure proper syntax

### **"Project not found"**
- Use `-list-projects` to see available projects
- Check project name spelling (case-insensitive)
- Add project first with `-add-project`

### **"Studio not found"**
- Use `-list-studios` to see available studios
- Check version format (AS6, AS45, 6, 4.5 all work)
- Configure studio first in GUI or with `-add-studio`

---

**Created by**: Vitaly Grosman  
**Organization**: Indigo R&D Division  
**Version**: 1.1.0
