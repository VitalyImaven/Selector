# Automation Studio Selector - Complete Guide

**Professional Tool for Managing Multiple Automation Studio Installations**

**Version**: 1.3.0  
**Created by**: Vitaly Grosman  
**Organization**: Indigo R&D Division  
**© 2025**

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [First-Time Setup](#first-time-setup)
4. [User Interface Guide](#user-interface-guide)
5. [Daily Usage](#daily-usage)
6. [What Happens Behind the Scenes](#what-happens-behind-the-scenes)
7. [Auto-Sync System](#auto-sync-system)
8. [Command-Line Interface (CLI)](#command-line-interface-cli)
9. [Jenkins & CI/CD Integration](#jenkins--cicd-integration)
10. [Settings & Configuration](#settings--configuration)
11. [Troubleshooting](#troubleshooting)
12. [Tips & Best Practices](#tips--best-practices)

---

## Overview

### What is Automation Studio Selector?

The Automation Studio Selector solves a critical problem: managing multiple versions of Automation Studio (AS 4.5, AS 6, etc.) with a single project.

**The Problem:**
- Before: Separate project copies for each AS version
- Manual file copying between versions
- Risk of losing changes when switching
- Complex project management

**The Solution:**
- One project works with all AS versions
- Automatic file configuration and switching
- Never lose work with auto-sync
- Professional, enterprise-ready tool

### OCB Project Background - Moving to AS6

> **Why OCB Needs Dual AS4.5/AS6 Support**

**The Transition:**
- AS 4.5 is moving toward End of Life (EOL)
- Main PLC S4-5 configurations are transforming to AS6: **Hila_MR / Sufa (unified) / Ayala**
- However, most PLC configurations will remain with AS4.5 for compatibility reasons

**Configurations Remaining on AS4.5:**
- **Arad ECO/ECO** – Not supported by AS6
- **Stacker/Jigs/TBs** – Not supported by AS6
- **Eilat MR2 / Shani / Barak / Tamar** – Remaining on AS4.5

**Why One Unified OCB?**
- The alternative option of maintaining **two different OCBs** was declined
- Reason: Excessive maintenance overhead
- Solution: **OCB must support both AS4.5 and AS6 configurations** in a single project

> ✅ **The Automation Studio Selector** enables this unified approach by automatically switching between AS versions without maintaining separate OCB projects!

**Project Architecture:**
- **AS4.5 Libraries** → Libraries (switchable)
- **AS6 Libraries** → Libraries (switchable)
- **AS4.5 Physical**: Shani, Arad_ECO, TAMAR_MR, Physical.pkg
- **AS6 Physical**: AYALA, HILA_MR, SUFA, Physical.pkg
- **SLC Repository**: SLC_SHANI_MR, SLC_BARAK_SPARK, SLC_HILA_ORA2 projects
- **Unified OCB.apj** with both AS4.5 and AS6 variants

### Key Features

- ✅ Support for multiple AS versions (4.5, 6, and future versions)
- ✅ Multiple project management
- ✅ Automatic library and configuration switching
- ✅ Auto-sync system (every 5 minutes, on AS close, on app close)
- ✅ Command-line interface for automation
- ✅ **Smart project path auto-detection for scripts (v1.3.0)**
- ✅ **Simplified prepare-only mode - no studio path needed! (v1.3.0)**
- ✅ Jenkins/CI-CD ready
- ✅ Comprehensive logging
- ✅ Professional UI with modern design

---

## Installation

### System Requirements

- **OS**: Windows 10/11 (64-bit)
- **Privileges**: Administrator for installation
- **Disk Space**: ~200 MB
- **AS Versions**: Any (4.5, 6, or newer)

### Installation Steps

1. **Download**: [AutomationStudioSelector_Setup_v1.3.0.exe](https://hp-my.sharepoint.com/:u:/p/vitaly_grosman/EaOKnHUZ1tlKjZGlEk23kRkBwOyI8lmW6uF4e4jWWDVJzg?e=og2YzG)
2. Right-click → "Run as administrator"
3. Follow installation wizard
4. Launch from Start Menu or desktop shortcut

> 📥 **Download Link:**  
> https://hp-my.sharepoint.com/:u:/p/vitaly_grosman/EaOKnHUZ1tlKjZGlEk23kRkBwOyI8lmW6uF4e4jWWDVJzg?e=og2YzG

### Installation Locations

- **Application**: `C:\Program Files\Automation Studio Selector\`
- **User Settings**: `%USERPROFILE%\.automation_selector\`
- **Logs**: `%USERPROFILE%\.automation_selector\logs\`

---

## First-Time Setup

When you first launch the application, configure:

### 1. Automation Studio Paths

**Add AS 4.5:**
1. Click "Add AS 4.5"
2. Browse to: `C:\BrAutomation\AS45\Bin-en\`
3. Select `AutomationStudio.exe`

**Add AS 6:**
1. Click "Add AS 6"
2. Browse to: `C:\Program Files (x86)\BRAutomation\AS6\bin-en\`
3. Select `AutomationStudio.exe`

### 2. Add Your Projects

After setup closes:
1. Click "Add Project..." in main window
2. Browse to your project directory
3. Enter a friendly name
4. Optionally add description
5. Click OK

---

## User Interface Guide

### Header Section
- **Logo**: Your custom blue logo
- **Title**: "Automation Studio Selector"

### Project Selection
- **List**: Shows all your configured projects
- **Format**: `ProjectName - C:\Path\To\Project`
- **Selection**: Click to select (highlighted in teal)
- **Buttons**:
  - **Add Project...**: Add new project to list
  - **Remove Selected**: Remove project from list (files not deleted)

### Automation Studio Selection
- **List**: Shows configured AS versions
- **Format**: `Automation Studio X.X - C:\Path\To\Exe`
- **Selection**: Click to select (highlighted in teal)
- **Double-Click**: Select and immediately open project
- **Buttons**:
  - **Refresh List**: Reload AS configurations
  - **Open Project**: Launch selected AS with selected project

### Operation Progress
- **Progress Bar**: Shows during file operations
- **Steps**: Validating → Clearing → Copying → Updating → Opening
- **Hidden**: When no operations running

### Session Log
- **Format**: `[HH:MM:SS] Message`
- **Indicators**: `[OK]` for success, `[ERROR]` for failures
- **Auto-scroll**: Shows latest messages
- **Clear Log**: Button to clear display

### Menu System

**File Menu:**
- Setup Automation Studio Paths...
- Manual Sync Now
- Exit

**Settings Menu:**
- Sync → Auto-Sync Settings...
- Sync → View Sync Status

**Help Menu:**
- How To → Interactive Help...
- How To → Quick Start Guide
- About

---

## Daily Usage

### Quick Start with Scripts (NEW v1.3.0 - Recommended!)

> 🚀 **Fastest Way!** Your OCB project now includes ready-to-use scripts in the `\scripts` directory!

**In your project directory, you'll find:**

```
OCB/
├── scripts/
│   ├── prepare45.bat    ← Double-click for AS 4.5
│   └── prepare6.bat     ← Double-click for AS 6
├── Logical/
├── Physical/
└── OCB.apj
```

**How to use:**

1. **For AS 4.5**: Navigate to `OCB\scripts\` and double-click `prepare45.bat`
2. **For AS 6**: Navigate to `OCB\scripts\` and double-click `prepare6.bat`
3. The script automatically detects the project path and converts all files
4. Wait for "Project ready for AS X.X" message
5. Done! Your project is now configured

**What happens:**

- ✅ Automatically detects project path (parent directory of scripts)
- ✅ Copies correct libraries (Libraries_45 or Libraries_6)
- ✅ Updates Physical.pkg file
- ✅ Updates OCB.apj file
- ✅ Ready to open in Automation Studio!

> 💡 **Tip:** You can run these scripts anytime to switch between AS versions. No GUI needed!  
> This uses the new v1.3.0 smart path detection feature.

### Basic Workflow (Using GUI)

1. **Select Project**: Click on project in list
2. **Select AS Version**: Click on AS 4.5 or AS 6
3. **Click "Open Project"**: Green button
4. **Work Normally**: AS opens with your project
5. **Auto-Sync**: Changes saved automatically

### Switching Versions

**Method 1: Using Scripts (Quick!)**

1. Go to your project's `\scripts` directory
2. Double-click `prepare45.bat` or `prepare6.bat`
3. Done! Project converted

**Method 2: Using GUI**

1. Close Automation Studio
2. Select different AS version in Selector
3. Click "Open Project"
4. Your previous work is preserved!

---

## What Happens Behind the Scenes

### Complete Process (6 Steps)

**Step 1: Validate Project Structure**
- Checks Logical and Physical folders exist
- Validates project structure
- Stops if validation fails

**Step 2: Clear Libraries Directory**
- Goes to `Logical\Libraries\`
- Deletes ALL files inside
- Prepares for new version

**Step 3: Copy Version-Specific Libraries**
- **For AS 4.5**: `Libraries_45\` → `Libraries\`
- **For AS 6**: `Libraries_6\` → `Libraries\`
- Copies all files and subdirectories

**Step 4: Update Physical.pkg**
- **For AS 4.5**: `Physical_45.pkg` → `Physical.pkg`
- **For AS 6**: `Physical_6.pkg` → `Physical.pkg`
- Deletes old, copies new

**Step 5: Update OCB.apj**
- **For AS 4.5**: `OCB_as45.apj` → `OCB.apj`
- **For AS 6**: `OCB_as6.apj` → `OCB.apj`
- Main project file updated

**Step 6: Launch Automation Studio**
- Executes: `AutomationStudio.exe "ProjectPath\OCB.apj"`
- AS opens with configured project

### Required Project Structure

```
YourProject/
├── Logical/
│   ├── Libraries/          # Managed automatically
│   ├── Libraries_45/       # AS 4.5 source (never modified)
│   └── Libraries_6/        # AS 6 source (never modified)
├── Physical/
│   ├── Physical.pkg        # Managed automatically
│   ├── Physical_45.pkg     # AS 4.5 source (never modified)
│   └── Physical_6.pkg      # AS 6 source (never modified)
├── OCB.apj                # Managed automatically
├── OCB_as45.apj           # AS 4.5 source (never modified)
└── OCB_as6.apj            # AS 6 source (never modified)
```

**Important**: Version-specific files (with `_45` or `_6` suffixes) are your source templates and are NEVER modified by the Selector.

---

## Auto-Sync System

### How It Works

The auto-sync system automatically copies your changes from the active working directory back to the permanent version-specific storage.

**Example Flow:**
1. Select AS 6 → `Libraries_6` content copied to `Libraries`
2. Work in AS and modify files in `Libraries`
3. Auto-sync triggers → Changes copied from `Libraries` back to `Libraries_6`
4. Select AS 4.5 → `Libraries_45` content copied to `Libraries`
5. Your AS 6 work is safely stored in `Libraries_6`!

### Auto-Sync Triggers

**1. Automation Studio Closes** (Default: Enabled)
- When AS process ends
- Immediate sync of all changes
- Captures work session

**2. Selector Application Closes** (Default: Enabled)
- Final sync on exit
- Safety net for remaining changes

**3. Periodic Timer** (Default: Every 5 minutes)
- Regular background checking
- Syncs only if changes detected
- Configurable interval (1-60 minutes)

### Configuration

Access via **Settings → Sync → Auto-Sync Settings...**

**Options:**
- Enable/disable each trigger
- Adjust periodic interval
- Configure backup settings (keep 0-10 backups)
- Toggle detailed logging

---

## Command-Line Interface (CLI)

### Why Use CLI?

Perfect for:
- Jenkins/CI-CD pipelines
- Batch processing
- Automated testing
- Remote servers
- Scheduled tasks

### Basic Usage

**GUI Mode** (no arguments):
```bash
AutomationStudioSelector.exe
```

**CLI Mode** (with arguments):
```bash
python main.py -project-path "C:\Projects\MyProject" -studio-path "C:\AS45\exe" -as-version 45 -prepare-only
```

### Essential Commands

**Information:**
```bash
python main.py -list-projects      # List all projects
python main.py -list-studios       # List all AS versions
python main.py -status             # Show status
python main.py -version            # Show version
python main.py -help               # Show help
```

**With GUI Configuration:**
```bash
python main.py ProjectName AS45    # Open project with AS 4.5
python main.py ProjectName AS6     # Open project with AS 6
```

**Direct Paths (No GUI Config Needed):**
```bash
python main.py -project-path "C:\Path\To\Project" -studio-path "C:\AS45\exe" -as-version 45 -prepare-only
```

### The Prepare-Only Mode

**Critical Parameter**: `-prepare-only`

**What it does:**
1. ✓ Validates project structure
2. ✓ Clears Libraries directory
3. ✓ Copies version-specific libraries
4. ✓ Updates Physical.pkg
5. ✓ Updates OCB.apj
6. ✗ Does NOT launch Automation Studio

**Usage:**
```bash
python main.py -project-path "C:\Project" -studio-path "C:\AS45\exe" -as-version 45 -prepare-only -silent
```

**Perfect for:**
- Jenkins builds
- Batch processing
- Pre-configuration
- CI/CD pipelines

---

## Jenkins & CI/CD Integration

> **v1.3.0 Update:** Jenkins scripts are now simpler! No `-studio-path` needed for prepare-only mode.

### The Complete Jenkins Command (v1.3.0 - Simplified!)

```batch
python main.py ^
  -project-path "%WORKSPACE%" ^
  -as-version 45 ^
  -prepare-only ^
  -silent
```

### Critical Parameters

| Parameter | Description | Example | Required |
|-----------|-------------|---------|----------|
| `-project-path` | Where Git cloned your project | `%WORKSPACE%` | Yes |
| `-as-version` | `45` or `6` (which files to copy) | `45` | Yes |
| `-prepare-only` | Don't launch AS | (flag) | For Jenkins |
| `-silent` | No console output | (flag) | Recommended |
| ~~`-studio-path`~~ | ~~Full path to AS executable~~ | ~~(not needed for prepare-only!)~~ | **NO** |

### Complete Jenkins Script (v1.3.0)

```batch
@echo off
REM Jenkins Build Script for AS 4.5

echo Configuring AS project from Git...

python C:\Tools\Selector\main.py ^
  -project-path "%WORKSPACE%" ^
  -as-version 45 ^
  -prepare-only ^
  -silent

if %errorlevel% equ 0 (
    echo [OK] Project configured for AS 4.5
    REM Add your build commands here
    REM Example: call "C:\BrAutomation\AS45\Bin-en\BR.AS.Build.exe" "%WORKSPACE%\Project.apj"
) else (
    echo [ERROR] Configuration failed
    exit /b 1
)
```

### Running from Project \scripts Directory (v1.3.0)

**NEW in v1.3.0:** Place scripts inside your project for portability!

```
YourProject/
├── scripts/
│   ├── prepare_as45.bat
│   └── prepare_as6.bat
├── Logical/
│   ├── Libraries_45/
│   └── Libraries_6/
├── Physical/
└── Project.apj
```

**Example prepare_as45.bat:**

```batch
@echo off
REM Script automatically detects project path from parent directory

set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%\.."

python "C:\Tools\Selector\main.py" ^
  -project-path "%PROJECT_DIR%" ^
  -as-version 45 ^
  -prepare-only

if %errorlevel% equ 0 (
    echo Project ready for AS 4.5!
) else (
    echo Configuration failed!
    exit /b 1
)
```

**Benefits:**
- ✅ Scripts travel with your project in Git
- ✅ No path hardcoding needed
- ✅ Works on any developer's machine
- ✅ Perfect for team collaboration

### Why This Works Without GUI

- Uses direct paths - no project lookup needed
- Specifies AS version explicitly - no config lookup needed
- Self-contained - everything in the command
- Portable - same script works on any build server

### Multi-Version Testing

```batch
@echo off
REM Test with both AS versions

echo Testing with AS 4.5...
python main.py -project-path "%WORKSPACE%" -studio-path "C:\AS45\exe" -as-version 45 -prepare-only -silent
if errorlevel 1 exit /b 1

echo Testing with AS 6...
python main.py -project-path "%WORKSPACE%" -studio-path "C:\AS6\exe" -as-version 6 -prepare-only -silent
if errorlevel 1 exit /b 1

echo All tests passed!
```

---

## Settings & Configuration

### Auto-Sync Settings

**Access**: Settings → Sync → Auto-Sync Settings...

**Sync Triggers:**
- ☑ Sync when Automation Studio closes
- ☑ Sync when Selector closes

**Periodic Sync:**
- ☑ Enable periodic sync
- Interval: 1-60 minutes (default: 5)

**Safety & Logging:**
- ☑ Log sync operations
- ☑ Create backups before sync
- Max backups: 0-10 (default: 3)

### Sync Status

**Access**: Settings → Sync → View Sync Status

**Information Shown:**
- Active Studio version
- Files synced this session
- Total syncs performed
- Last sync timestamp
- Current configuration

---

## Troubleshooting

### Common Issues

**"Project structure validation failed"**
- Ensure Logical and Physical folders exist
- Check folder permissions
- Verify correct project root

**"Automation Studio executable not found"**
- Reconfigure in File → Setup Automation Studio Paths
- Verify AS installation
- Check path accessibility

**"Source libraries directory not found"**
- Create `Libraries_45` or `Libraries_6` in Logical folder
- Verify folder naming (exact match required)
- Check that source files exist

**Auto-sync not working**
- Check Settings → Sync → Auto-Sync Settings
- Enable sync triggers
- Check Session Log for errors
- Try Manual Sync Now

### Log Files

**Locations:**
- Application: `%USERPROFILE%\.automation_selector\logs\application.log`
- Sessions: `%USERPROFILE%\.automation_selector\logs\session_*.log`

**Contains:**
- All operations with timestamps
- Error details
- File operations
- Sync activities

---

## Tips & Best Practices

### Daily Workflow

✅ **DO:**
- Leave Selector open for auto-sync
- Check Session Log for confirmations
- Use double-click for faster opening
- Keep backups enabled

❌ **DON'T:**
- Edit active files directly (Libraries, Physical.pkg, OCB.apj)
- Delete version-specific directories while AS running
- Run multiple AS versions simultaneously
- Disable auto-sync without backup strategy

### Keyboard Shortcuts

- **F5**: Refresh studio list
- **Enter**: Open project (when selected)
- **Double-Click**: Select and open immediately
- **ESC**: Close dialogs

### Project Management

- Use descriptive project names
- Add descriptions to identify projects
- Test in both AS versions before deployment
- Regular manual sync before important work

### Performance Tips

**For Large Projects:**
- Increase periodic sync interval to 10-15 minutes
- Monitor disk space (backups accumulate)
- Use SSD storage for better performance

**For System Resources:**
- Close unused AS instances
- Clean old logs periodically
- Sufficient RAM for large projects

---

## CLI Quick Reference

### Essential Commands

```bash
# GUI mode
AutomationStudioSelector.exe

# Open with configured project
python main.py ProjectName AS45

# Jenkins mode (no GUI config)
python main.py -project-path "C:\Project" -studio-path "C:\AS45\exe" -as-version 45 -prepare-only -silent

# List projects
python main.py -list-projects

# Show help
python main.py -help
```

### Common Options

- `-prepare-only`: Configure files but don't launch AS
- `-silent`: No output (automation mode)
- `-verbose`: Detailed output (debugging)
- `-wait`: Wait for AS to close
- `-as-version`: `45` or `6` (required with `-studio-path`)

### Exit Codes

- `0` = Success
- `1` = General error
- `3` = Project not found
- `4` = Studio not found

---

## Advanced Features

### Multiple Projects

- Add unlimited projects
- Quick switching between projects
- Each project maintains separate version files
- Auto-sync tracks changes per project

### Manual Sync

**When to use:**
- Before switching AS versions
- After important changes
- Testing sync functionality
- Before closing application

**Access**: File → Manual Sync Now

### Configuration Backup

All settings stored in JSON:
- `%USERPROFILE%\.automation_selector\config.json`
- `%USERPROFILE%\.automation_selector\auto_sync_config.xml`

---

## Summary

### The Power of Automation Studio Selector

**Time Saving**: No more manual file copying  
**Error Prevention**: Auto-sync prevents data loss  
**Flexibility**: Switch AS versions instantly  
**Transparency**: Full logging of all operations  
**Automation**: CLI support for Jenkins/CI-CD  
**Professional**: Enterprise-ready solution  

### Getting Started Checklist

1. ☑ Install the application
2. ☑ Configure AS 4.5 and AS 6 paths
3. ☑ Add your first project
4. ☑ Select AS version and click "Open Project"
5. ☑ Work normally - auto-sync handles the rest!

---

**Created with ❤️ by Vitaly Grosman - Indigo R&D Division**

*For support, refer to the interactive help system: Help → How To → Interactive Help...*
