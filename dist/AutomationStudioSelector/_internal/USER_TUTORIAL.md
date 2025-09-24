# Automation Studio Selector - Complete User Tutorial

![Logo](assets/logo.png)

**Created by**: Vitaly Grosman  
**Organization**: Indigo R&D Division  
**Version**: 1.0.0

---

## 📋 Table of Contents

1. [What is Automation Studio Selector?](#what-is-automation-studio-selector)
2. [Installation Guide](#installation-guide)
3. [First-Time Setup](#first-time-setup)
4. [Understanding the Interface](#understanding-the-interface)
5. [How to Use the Application](#how-to-use-the-application)
6. [Auto-Sync System](#auto-sync-system)
7. [Settings and Configuration](#settings-and-configuration)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Features](#advanced-features)
10. [Tips and Best Practices](#tips-and-best-practices)

---

## What is Automation Studio Selector?

**Automation Studio Selector** is a professional tool designed to solve a common problem: managing multiple versions of Automation Studio (AS) with a single project.

### 🎯 **The Problem It Solves**

Before this tool, you needed:
- Separate project copies for each AS version (4.5, 6, etc.)
- Manual file copying between versions
- Risk of losing changes when switching versions
- Complex project management

### ✅ **The Solution**

With Automation Studio Selector:
- **One Project**: Keep all your work in one place
- **Smart Switching**: Automatically configure project for any AS version
- **Auto-Sync**: Never lose changes when switching versions
- **Professional**: Enterprise-ready with logging and error handling

---

## Installation Guide

### 📦 **System Requirements**

- **Operating System**: Windows 10/11 (64-bit)
- **Privileges**: Administrator rights for installation
- **Disk Space**: ~200 MB
- **Automation Studio**: Any version (4.5, 6, or newer)

### 🚀 **Installation Steps**

1. **Download** the installer: `AutomationStudioSelector_Setup_v1.0.0.exe`
2. **Right-click** and select "Run as administrator"
3. **Follow** the installation wizard:
   - Accept the license agreement
   - Choose installation directory (default: `C:\Program Files\Automation Studio Selector`)
   - Select additional tasks (desktop shortcut, etc.)
4. **Click** "Install" and wait for completion
5. **Launch** the application from Start Menu or desktop shortcut

### 📁 **Installation Locations**

After installation, you'll find:
- **Application**: `C:\Program Files\Automation Studio Selector\`
- **User Settings**: `%USERPROFILE%\.automation_selector\`
- **Logs**: `%USERPROFILE%\.automation_selector\logs\`

---

## First-Time Setup

When you first launch the application, you'll need to configure two things:

### 1. 🔧 **Automation Studio Paths**

The setup dialog will appear automatically:

#### **Adding AS 4.5:**
1. Click **"Add AS 4.5"**
2. Browse to your AS 4.5 installation
3. Select `AutomationStudio.exe` (usually in `C:\BrAutomation\AS45\Bin-en\`)
4. Click **"Open"**

#### **Adding AS 6:**
1. Click **"Add AS 6"**  
2. Browse to your AS 6 installation
3. Select `AutomationStudio.exe` (usually in `C:\Program Files (x86)\BRAutomation\AS6\bin-en\`)
4. Click **"Open"**

#### **Adding More Versions:**
- You can add as many AS versions as you have installed
- Each version gets its own button in the setup dialog

### 2. 📂 **Project Root Directory**

1. Click **"Browse..."** next to "Project Root Directory"
2. Navigate to your project's main folder
3. Select the folder that contains your `Logical` and `Physical` directories
4. Click **"Select Folder"**

### 3. ✅ **Save Configuration**

1. Review your settings
2. Click **"Save & Continue"**
3. The application will validate your configuration
4. Setup is complete!

---

## Understanding the Interface

The main window has several sections:

### 🏠 **Header Section**
- **Logo**: Indigo R&D Division branding
- **Title**: "Automation Studio Selector"

### 📁 **Project Root Directory Section**
- **Current Path**: Shows your selected project directory
- **Browse Button**: Change project location anytime

### 🎯 **Select Automation Studio Section**
- **Studio List**: Shows all configured AS versions
- **Selection**: Click to select which version to use
- **Buttons**: 
  - **Refresh List**: Reload AS configurations
  - **Open Project**: Start the selected AS with your project

### ⚙️ **Operation Progress Section**
- **Progress Bar**: Shows during project setup operations
- **Status Updates**: Real-time progress information

### 📝 **Session Log Section**
- **Activity Log**: Shows all operations and their results
- **Timestamps**: When each action occurred
- **Status Icons**: ✓ for success, ✗ for errors
- **Clear Log Button**: Clean the display

### 📊 **Status Bar**
- **Bottom Bar**: Shows current operation status
- **Quick Info**: Number of loaded studios, current operations

---

## How to Use the Application

### 🚀 **Basic Workflow**

#### **Step 1: Select Your Project**
1. Ensure the **Project Root Directory** shows your project path
2. If not, click **"Browse..."** and select your project folder

#### **Step 2: Choose Automation Studio Version**
1. Look at the **"Select Automation Studio"** section
2. You'll see all your configured AS versions (e.g., "Automation Studio 4.5", "Automation Studio 6")
3. **Click** on the version you want to use
4. The selected version will be highlighted in teal

#### **Step 3: Open Your Project**
1. Click the **"Open Project"** button (green button)
2. Watch the **Operation Progress** section for updates
3. The application will:
   - ✅ Validate your project structure
   - 🗑️ Clear the active Libraries directory
   - 📋 Copy libraries for your selected AS version
   - 📄 Update Physical.pkg file
   - 📁 Update project file (OCB.apj)
   - 🚀 Launch Automation Studio with your project

#### **Step 4: Work in Automation Studio**
1. Automation Studio will open with your project
2. Make your changes as normal
3. Save your work in AS
4. **The auto-sync system will automatically save your changes back to the correct version directories**

### 🔄 **Switching Between Versions**

To switch from AS 4.5 to AS 6 (or vice versa):

1. **Close Automation Studio** (if running)
2. **Select different version** in the Selector
3. **Click "Open Project"** again
4. **Your changes are preserved** - the auto-sync system handles everything!

### 📊 **Understanding Project Structure**

Your project should be organized like this:

```
YourProject/
├── Logical/
│   ├── Libraries/          # Active working directory (managed automatically)
│   ├── Libraries_45/       # AS 4.5 libraries (your permanent storage)
│   └── Libraries_6/        # AS 6 libraries (your permanent storage)
├── Physical/
│   ├── Physical.pkg        # Active config (managed automatically)
│   ├── Physical_45.pkg     # AS 4.5 config (your permanent storage)
│   └── Physical_6.pkg      # AS 6 config (your permanent storage)
├── OCB.apj                # Main project file (managed automatically)
├── OCB_as45.apj           # AS 4.5 project template (your permanent storage)
└── OCB_as6.apj            # AS 6 project template (your permanent storage)
```

**Key Points:**
- **Never edit** files without the suffix (Libraries, Physical.pkg, OCB.apj)
- **Always edit** the version-specific files (Libraries_45, Libraries_6, etc.)
- **The Selector manages** the active files automatically

---

## Auto-Sync System

The auto-sync system is one of the most powerful features - it ensures you never lose work when switching between AS versions.

### 🔄 **How Auto-Sync Works**

The system automatically copies your changes from the active working directory back to the permanent version-specific storage.

**Example Flow:**
1. You select **AS 6** → Libraries_6 content is copied to Libraries
2. You work in AS and modify files in Libraries
3. **Auto-sync triggers** → Your changes are copied from Libraries back to Libraries_6
4. Later, you select **AS 4.5** → Libraries_45 content is copied to Libraries
5. Your AS 6 work is safely stored in Libraries_6!

### ⚡ **Auto-Sync Triggers**

Auto-sync happens automatically when:

1. **Automation Studio Closes** (default: enabled)
   - When you close AS, changes are immediately synced
   
2. **Selector Application Closes** (default: enabled)
   - When you close the Selector, final sync is performed
   
3. **Periodic Timer** (default: every 5 minutes)
   - Regular checks for changes and syncs if found

### 📝 **Auto-Sync Logging**

All sync operations are logged:
- **Session Log**: Shows in the application window
- **Log Files**: Stored in `%USERPROFILE%\.automation_selector\logs\`
- **Timestamps**: When each sync occurred
- **File Counts**: How many files were synced

### 🛡️ **Safety Features**

- **Backups**: Creates timestamped backups before overwriting (default: keep 3)
- **Change Detection**: Only syncs files that actually changed
- **Error Handling**: Graceful handling of sync failures
- **Validation**: Ensures file integrity during operations

---

## Settings and Configuration

### ⚙️ **Accessing Settings**

1. Click **"Settings"** in the menu bar
2. Select **"Sync"** submenu
3. Choose your desired option:
   - **"Auto-Sync Settings..."** - Configure sync behavior
   - **"View Sync Status"** - See current sync statistics

### 🎛️ **Auto-Sync Settings Dialog**

#### **Sync Triggers Section:**
- **☑️ Sync when Automation Studio closes**
  - Automatically sync when any AS process ends
  - Recommended: **Enabled**

- **☑️ Sync when Selector application closes**
  - Final sync when you close the Selector
  - Recommended: **Enabled**

#### **Periodic Sync Section:**
- **☑️ Enable periodic sync**
  - Regular automatic checking for changes
  - Recommended: **Enabled**

- **⏱️ Check interval: [X] minutes**
  - How often to check for changes (1-60 minutes)
  - Default: **5 minutes**
  - Lower = more frequent syncing, higher CPU usage
  - Higher = less frequent syncing, risk of longer gaps

#### **Safety & Logging Section:**
- **☑️ Log sync operations**
  - Write detailed logs of all sync activities
  - Recommended: **Enabled** (helps with troubleshooting)

- **☑️ Create backups before sync**
  - Create timestamped backups before overwriting
  - Recommended: **Enabled** (safety net)

- **🔢 Max backups: [X]**
  - How many backup versions to keep (0-10)
  - Default: **3**
  - 0 = unlimited backups (uses more disk space)

### 💾 **Saving Settings**

1. **Adjust settings** as desired
2. **Click "Save Settings"**
3. **Settings apply immediately** - no restart required
4. **Confirmation message** appears when saved successfully

### 🔄 **Reset to Defaults**

1. **Click "Reset to Defaults"**
2. **Confirm** the reset operation
3. **All settings return** to recommended values
4. **Click "Save Settings"** to apply

---

## Troubleshooting

### ❌ **Common Issues and Solutions**

#### **"Project structure validation failed"**

**Problem**: The Selector can't find required directories.

**Solutions**:
1. **Check project structure**: Ensure you have `Logical` and `Physical` folders
2. **Verify path**: Make sure Project Root Directory points to the correct folder
3. **Check permissions**: Ensure you have read access to the project directory

#### **"Automation Studio executable not found"**

**Problem**: The configured AS path is invalid.

**Solutions**:
1. **Reconfigure paths**: Go to `File → Setup Automation Studio Paths...`
2. **Browse to correct location**: Find the actual `AutomationStudio.exe` file
3. **Check installation**: Verify AS is properly installed

#### **"Source libraries directory not found"**

**Problem**: Version-specific directories are missing.

**Solutions**:
1. **Create missing directories**: Create `Libraries_45`, `Libraries_6`, etc. in your `Logical` folder
2. **Copy existing libraries**: Copy your current libraries to the version-specific folders
3. **Check naming**: Ensure folder names match exactly (Libraries_45, not Libraries45)

#### **Auto-sync not working**

**Problem**: Changes aren't being synced automatically.

**Solutions**:
1. **Check settings**: Go to `Settings → Sync → Auto-Sync Settings...`
2. **Enable triggers**: Ensure sync triggers are enabled
3. **Check logs**: Look in Session Log for error messages
4. **Manual sync**: Try `File → Manual Sync Now` to test

#### **Application won't start**

**Problem**: The Selector doesn't launch.

**Solutions**:
1. **Run as administrator**: Right-click and "Run as administrator"
2. **Check Windows version**: Requires Windows 10/11 64-bit
3. **Reinstall**: Uninstall and reinstall the application
4. **Check logs**: Look in `%USERPROFILE%\.automation_selector\logs\`

### 🔍 **Getting More Help**

#### **Log Files Location**:
- **Application logs**: `%USERPROFILE%\.automation_selector\logs\application.log`
- **Session logs**: `%USERPROFILE%\.automation_selector\logs\session_YYYYMMDD_HHMMSS.log`

#### **Configuration Files**:
- **Main config**: `%USERPROFILE%\.automation_selector\config.json`
- **Auto-sync config**: `%USERPROFILE%\.automation_selector\auto_sync_config.xml`

#### **Diagnostic Steps**:
1. **Check logs** for error messages
2. **Test manual sync** with `File → Manual Sync Now`
3. **Verify project structure** manually
4. **Test with simple project** to isolate issues

---

## Advanced Features

### 🔧 **Manual Sync**

Sometimes you want to sync immediately without waiting:

1. **Go to**: `File → Manual Sync Now`
2. **Wait for completion**: Progress shown in status bar
3. **Check results**: Success message or error details
4. **View log**: See exactly what was synced

### 📊 **Sync Status Monitoring**

To see detailed sync information:

1. **Go to**: `Settings → Sync → View Sync Status`
2. **Review information**:
   - Active Studio version
   - Files synced this session
   - Last sync timestamp
   - Configuration summary
   - Config file location

### 🎯 **Project Root Management**

You can work with multiple projects:

1. **Change project**: `File → Change Project Root...`
2. **Browse to new project**: Select different project folder
3. **Automatic validation**: Ensures new project is valid
4. **Settings preserved**: AS configurations remain the same

### 📁 **Multiple Project Workflow**

For users managing multiple projects:

1. **Project A**: Set root to `C:\Projects\ProjectA`
2. **Work in AS**: Make changes, auto-sync handles storage
3. **Switch to Project B**: Change root to `C:\Projects\ProjectB`
4. **Work in AS**: Completely separate library storage
5. **Switch back**: Return to Project A with all changes preserved

### ⚙️ **Custom Configuration**

Advanced users can edit XML configuration directly:

**File**: `%USERPROFILE%\.automation_selector\auto_sync_config.xml`

```xml
<AutoSyncSettings>
  <SyncOnAutomationStudioClose enabled="true" />
  <SyncOnSelectorClose enabled="true" />
  <PeriodicSync enabled="true" intervalMinutes="5" />
  <LogSyncOperations enabled="true" />
  <BackupBeforeSync enabled="true" maxBackups="3" />
</AutoSyncSettings>
```

**Note**: Changes take effect when you restart the application or reload settings.

---

## Tips and Best Practices

### 🏆 **Best Practices**

#### **Project Organization**:
1. **Use descriptive names**: Name your version-specific folders clearly
2. **Keep backups**: The auto-backup feature is your friend
3. **Regular commits**: If using version control, commit frequently
4. **Document changes**: Use meaningful commit messages

#### **Version Management**:
1. **Test thoroughly**: Test your project in each AS version before deployment
2. **Version-specific features**: Be aware of features that don't work across versions
3. **Library compatibility**: Some libraries may not work in all AS versions
4. **Documentation**: Keep notes about version-specific requirements

#### **Performance Optimization**:
1. **Adjust sync frequency**: Longer intervals for large projects
2. **Monitor disk space**: Backups can accumulate over time
3. **Clean old logs**: Periodically clean log directories
4. **Close unused AS**: Don't run multiple AS versions simultaneously

### 💡 **Pro Tips**

#### **Keyboard Shortcuts**:
- **F5**: Refresh studio list (same as clicking "Refresh List")
- **Enter**: Open project (when studio is selected)
- **Escape**: Close dialogs

#### **Workflow Optimization**:
1. **Leave Selector open**: Keep it running for automatic sync
2. **Use desktop shortcut**: Quick access to the application
3. **Monitor session log**: Watch for sync confirmations
4. **Regular manual sync**: Use before important work sessions

#### **Troubleshooting Shortcuts**:
1. **Check session log first**: Most issues show up here
2. **Try manual sync**: Tests if sync system is working
3. **Restart both applications**: Often resolves temporary issues
4. **Check file permissions**: Ensure write access to project folders

### ⚠️ **Important Warnings**

#### **Do NOT**:
- ❌ **Edit active files directly** (Libraries, Physical.pkg, OCB.apj)
- ❌ **Delete version-specific directories** while AS is running
- ❌ **Run multiple AS versions** on the same project simultaneously
- ❌ **Disable auto-sync** unless you have a backup strategy

#### **Always**:
- ✅ **Let auto-sync complete** before switching versions
- ✅ **Check session log** for sync confirmations
- ✅ **Keep backups enabled** for safety
- ✅ **Test in both versions** before deploying

---

## Conclusion

**Automation Studio Selector** transforms how you work with multiple AS versions. By automating the complex file management and providing intelligent sync capabilities, it lets you focus on your automation projects instead of managing files.

### 🎯 **Key Benefits**

- **⏱️ Time Saving**: No more manual file copying
- **🛡️ Error Prevention**: Automatic sync prevents data loss
- **🔄 Flexibility**: Switch between AS versions instantly
- **📊 Transparency**: Full logging of all operations
- **🎛️ Control**: Configurable to match your workflow

### 🚀 **Getting Started**

1. **Install** the application
2. **Configure** your AS paths and project root
3. **Select** your desired AS version
4. **Click** "Open Project"
5. **Work normally** - auto-sync handles the rest!

### 📞 **Support**

For additional support or feature requests, refer to your system administrator or the development team.

---

**Created with ❤️ by Vitaly Grosman - Indigo R&D Division**

*This tutorial covers version 1.0.0 of Automation Studio Selector. Features and interface may vary in future versions.*
