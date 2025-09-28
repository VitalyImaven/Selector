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

The main window has several sections that work together to provide a seamless experience:

### 🏠 **Header Section**
- **Logo**: Your custom blue logo with checkmark and pointing hand design
- **Title**: "Automation Studio Selector" - clearly identifies the application

### 📁 **Project Root Directory Section**

This section shows and controls your current project location.

#### **What You'll See:**
- **Instructions Text**: "Select the root directory of your project (should contain Logical and Physical folders):"
- **Path Display Field**: Shows the currently selected project directory path
  - **Gray placeholder text**: "No project root selected..." when no path is set
  - **Black text**: Shows the actual path when a project is selected
- **Browse Button**: Blue button labeled "Browse..." for selecting a different project

#### **How to Use:**
- **View Current Path**: The text field shows your active project directory
- **Change Project**: Click "Browse..." to select a different project folder
- **Validation**: The application automatically checks that your selected folder contains "Logical" and "Physical" subdirectories
- **Auto-Save**: Your selection is automatically saved to configuration

#### **Requirements:**
The selected directory must contain:
- **Logical/** subdirectory (containing your AS libraries)
- **Physical/** subdirectory (containing your AS physical configurations)

### 🎯 **Select Automation Studio Section**

This is the main working area where you choose which AS version to use.

#### **What You'll See:**
- **Instructions Text**: "Choose which Automation Studio version to use for opening your project:"
- **Studio List**: A scrollable list showing all your configured Automation Studio versions
  - **Format**: "Automation Studio X.X" on the first line
  - **Path Info**: "Path: [executable location]" on the second line
  - **Selection Highlight**: Selected item appears with teal background and white text
- **Two Buttons**: 
  - **"Refresh List"** (blue button on the left)
  - **"Open Project"** (green button on the right)

#### **Studio List Details:**
- **No Studios Configured**: Shows "No Automation Studios configured" in gray text
- **Multiple Studios**: Each AS version appears as a separate item
- **Example Display**:
  ```
  Automation Studio 4.5
  Path: C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe
  
  Automation Studio 6
  Path: C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe
  ```

#### **How to Use:**
- **Select Version**: Click once on any AS version to select it
- **Double-Click Shortcut**: Double-click to select and immediately open project
- **Visual Feedback**: Selected item is highlighted in teal color
- **Button Activation**: "Open Project" button becomes active (green) when valid selection is made

#### **Button Functions:**

##### **"Refresh List" Button (Blue):**
- **Purpose**: Reload the list of configured Automation Studio installations
- **When to Use**: 
  - After adding new AS installations through the setup dialog
  - If the list appears outdated or empty
  - After modifying AS configurations
- **What It Does**: 
  - Re-reads your saved configuration
  - Updates the display with current AS installations
  - Preserves your last selected studio (auto-selects it)

##### **"Open Project" Button (Green, Primary Action):**
- **Purpose**: Execute the complete project setup and launch the selected AS
- **When Enabled**: Only when BOTH conditions are met:
  - A studio version is selected (highlighted in teal)
  - A valid project root directory is configured
- **When Disabled**: Button appears gray when conditions aren't met
- **What It Does**: 
  - Validates your project structure
  - Clears the active Libraries directory
  - Copies version-specific libraries to active location
  - Updates Physical.pkg with version-specific configuration
  - Updates project file (OCB.apj) with version-specific template
  - Launches the selected Automation Studio with your project

#### **Selection Behavior:**
- **Last Used**: Application remembers your last selected studio and pre-selects it
- **Visual Feedback**: Selected studio has teal background with white text
- **Hover Effect**: Items show light gray background when hovering
- **Keyboard**: You can use arrow keys to navigate and Enter to activate

### ⚙️ **Operation Progress Section**

This section provides real-time feedback during project setup operations.

#### **What You'll See:**
- **Group Title**: "Operation Progress"
- **Progress Bar**: Animated blue progress bar (appears only during operations)
- **Hidden by Default**: Section is compact when no operations are running

#### **During Operations:**
The progress bar shows six distinct phases:
1. **"Starting project setup..."** - Initialization
2. **"Validating project structure..."** - Checking project folders
3. **"Clearing Libraries directory..."** - Removing old active files
4. **"Copying version-specific libraries..."** - Installing AS-specific libraries
5. **"Updating Physical.pkg file..."** - Configuring physical settings
6. **"Updating project file..."** - Setting up main project file
7. **"Opening project..."** - Launching Automation Studio

#### **Visual Indicators:**
- **Blue Animated Bar**: Shows operation is in progress
- **Indeterminate Progress**: Bar moves continuously (operation time varies)
- **Disappears**: Progress bar hides when operation completes

### 📝 **Session Log Section**

The session log provides a detailed record of all application activities.

#### **What You'll See:**
- **Group Title**: "Session Log"
- **Log Display Area**: Scrollable text area showing timestamped messages
- **Clear Log Button**: Gray "Clear Log" button below the log area

#### **Log Message Format:**
- **Timestamp**: `[HH:MM:SS]` in 24-hour format
- **Status Icon**: 
  - **✓** for successful operations
  - **✗** for errors or failures
  - **No icon** for informational messages
- **Message Text**: Detailed description of what happened

#### **What Gets Logged:**
- **Application Startup**: Configuration loading, studio detection
- **User Actions**: Studio selection, project opening, manual sync
- **Auto-Sync Activities**: Background synchronization operations
- **File Operations**: Copying, deleting, updating files
- **Errors and Warnings**: Detailed error messages with context
- **Configuration Changes**: Settings updates, path changes

#### **Example Log Entries:**
```
[14:30:15] Loaded 2 studio configurations
[14:30:15] Project root: C:\MyProject
[14:30:20] User selected: AS 6 (Version 6)
[14:30:22] ✓ Auto-sync completed: 3 files synchronized
[14:30:25] Starting project setup for Automation Studio 6
[14:30:26] ✓ Project setup completed successfully
```

#### **Log Management:**
- **Auto-Scroll**: Automatically scrolls to show latest messages
- **Clear Display**: "Clear Log" button clears the visible log (doesn't affect log files)
- **Persistent Logs**: Detailed logs are also saved to files in your user directory

### 📊 **Status Bar**

The status bar at the bottom provides quick status information.

#### **What You'll See:**
- **Operation Status**: Current activity or last completed operation
- **Studio Count**: "Loaded X studio(s)" when studios are configured
- **Sync Status**: "Auto-sync: X files synchronized" during sync operations
- **Error Indicators**: Brief error messages when issues occur

#### **Status Examples:**
- **"Ready"** - Application idle, ready for user action
- **"Operation completed successfully"** - Project setup finished
- **"Auto-sync: 5 files synchronized"** - Background sync completed
- **"Project root set to: MyProject"** - Configuration updated

### 📋 **Menu System**

The application provides comprehensive menu access to all features.

#### **File Menu:**
- **"Setup Automation Studio Paths..."** - Configure AS installation locations
- **"Change Project Root..."** - Select different project directory
- **"Manual Sync Now"** - Immediate synchronization of current changes
- **"Exit"** - Close the application

#### **Settings Menu:**
- **Sync Submenu:**
  - **"Auto-Sync Settings..."** - Configure automatic synchronization behavior
  - **"View Sync Status"** - Display sync statistics and current status

#### **Help Menu:**
- **How To Submenu:**
  - **"Interactive Help..."** - Opens comprehensive help dialog with navigation
  - **"Quick Start Guide"** - Brief overview popup for immediate guidance
- **"About"** - Application information and credits

#### **Menu Shortcuts:**
- **Alt + F**: Open File menu
- **Alt + S**: Open Settings menu  
- **Alt + H**: Open Help menu
- **F1**: Quick access to help (standard Windows convention)

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

**Detailed Example Flow:**
1. You select **AS 6** → Libraries_6 content is copied to Libraries
2. You work in AS and modify files in Libraries
3. **Auto-sync triggers** → Your changes are copied from Libraries back to Libraries_6
4. Later, you select **AS 4.5** → Libraries_45 content is copied to Libraries
5. Your AS 6 work is safely stored in Libraries_6!

### ⚡ **Auto-Sync Triggers**

Auto-sync happens automatically in three different scenarios:

#### **1. 🔴 Automation Studio Closes (Default: Enabled)**
- **Trigger**: When you close any Automation Studio process
- **Action**: Immediately syncs all changes back to version-specific storage
- **Why**: Captures your work session changes the moment you finish working
- **Detection**: The application monitors AS processes and detects when they close
- **Timing**: Sync happens within seconds of AS closing

#### **2. 🚪 Selector Application Closes (Default: Enabled)**
- **Trigger**: When you close the Selector application
- **Action**: Final sync to ensure nothing is lost
- **Why**: Safety net for any remaining changes that might not have been synced
- **Timing**: Happens during application shutdown process

#### **3. ⏰ Periodic Timer (Default: Every 5 minutes)**
- **Trigger**: Regular interval while you work
- **Action**: Checks for changes and syncs if found
- **Why**: Continuous backup of your work while AS is running
- **Configurable**: Interval can be adjusted from 1-60 minutes
- **Smart**: Only syncs if actual changes are detected

### 📝 **Auto-Sync Logging and Monitoring**

#### **Session Log Display:**
All sync operations appear in the application's Session Log:
- **Success Messages**: "✓ Auto-sync completed: X files synchronized"
- **Error Messages**: "✗ Auto-sync error: [detailed error message]"
- **Timestamps**: Exact time when each sync occurred
- **File Counts**: Number of files that were synchronized

#### **Status Bar Updates:**
- **"Auto-sync: X files synchronized"** - Brief confirmation message
- **"Auto-sync error: [message]"** - Error notifications
- **Temporary Display**: Messages appear for 3-5 seconds

#### **Persistent Log Files:**
All sync activities are permanently recorded in:
- **Application Log**: `%USERPROFILE%\.automation_selector\logs\application.log`
- **Session Logs**: `%USERPROFILE%\.automation_selector\logs\session_YYYYMMDD_HHMMSS.log`

### 🛡️ **Safety Features**

#### **📦 Automatic Backups:**
- **Timestamped Backups**: Creates backups with format `Libraries_6_backup_YYYYMMDD_HHMMSS`
- **Default Retention**: Keeps the last 3 backup versions automatically
- **Before Overwriting**: Backup is created before any sync operation
- **Configurable**: Number of backups can be adjusted (0-10)
- **Cleanup**: Old backups are automatically removed when limit is exceeded

#### **🔍 Intelligent Change Detection:**
- **File Comparison**: Compares file size and modification time
- **Efficiency**: Only syncs files that actually changed
- **Tolerance**: 1-second timestamp tolerance to avoid false positives
- **Recursive**: Scans all subdirectories for changes
- **Performance**: Optimized to handle large library directories

#### **🛡️ Error Handling:**
- **Graceful Failures**: If one file fails, others continue to sync
- **Detailed Logging**: Full error details recorded in logs
- **User Notification**: Error messages shown in Session Log and status bar
- **Retry Logic**: Automatic retry for temporary failures
- **Rollback**: Can restore from backups if sync fails

### 📊 **Monitoring Auto-Sync Activity**

#### **Real-Time Monitoring:**
Use **Settings → Sync → View Sync Status** to see:
- **Active Studio**: Currently selected AS version being monitored
- **Files Synced This Session**: Count of files synchronized since application started
- **Total Syncs Performed**: Lifetime count of sync operations
- **Last Sync Time**: Timestamp of most recent sync operation
- **Last Check Time**: When the system last checked for changes
- **Current Configuration**: Periodic sync status and interval

#### **Log Analysis:**
- **Session Log**: Real-time display of sync activities
- **File Logs**: Permanent record for historical analysis
- **Error Tracking**: Detailed error information for troubleshooting
- **Performance Metrics**: Timing information for sync operations

### ⚙️ **Configuring Auto-Sync**

Access configuration through **Settings → Sync → Auto-Sync Settings...**

#### **Sync Triggers Configuration:**
- **☑️ Sync when Automation Studio closes**
  - **Default**: Enabled
  - **Recommendation**: Keep enabled for immediate change capture
  - **Impact**: Ensures work is saved the moment you finish

- **☑️ Sync when Selector application closes**
  - **Default**: Enabled  
  - **Recommendation**: Keep enabled as safety net
  - **Impact**: Final protection against data loss

#### **Periodic Sync Configuration:**
- **☑️ Enable periodic sync**
  - **Default**: Enabled
  - **Recommendation**: Keep enabled for continuous protection
  - **Impact**: Background protection while working

- **⏱️ Check interval: [X] minutes**
  - **Default**: 5 minutes
  - **Range**: 1-60 minutes
  - **Considerations**:
    - **Lower values (1-3 min)**: More protection, slightly higher CPU usage
    - **Higher values (10-30 min)**: Less frequent checking, lower resource usage
    - **For large projects**: Consider 10+ minutes
    - **For critical work**: Consider 2-3 minutes

#### **Safety & Logging Configuration:**
- **☑️ Log sync operations**
  - **Default**: Enabled
  - **Recommendation**: Keep enabled for troubleshooting
  - **Impact**: Detailed record of all sync activities

- **☑️ Create backups before sync**
  - **Default**: Enabled
  - **Recommendation**: Keep enabled for safety
  - **Impact**: Safety net in case of sync errors

- **🔢 Max backups: [X]**
  - **Default**: 3 backups
  - **Range**: 0-10 backups
  - **Considerations**:
    - **0**: Unlimited backups (uses more disk space)
    - **1-3**: Minimal disk usage, basic safety
    - **5-10**: High safety, more disk usage

### 🔄 **Manual Sync Operations**

Sometimes you want to synchronize immediately without waiting for automatic triggers.

#### **How to Perform Manual Sync:**
1. **Go to**: `File → Manual Sync Now`
2. **Wait**: Operation completes automatically
3. **Check Results**: Success/failure message appears
4. **Review Log**: Detailed results shown in Session Log

#### **When to Use Manual Sync:**
- **Before switching AS versions**: Ensure all changes are captured
- **After making important changes**: Immediate backup of critical work
- **Testing sync functionality**: Verify that auto-sync system is working
- **Before closing application**: Extra safety measure
- **After configuration changes**: Ensure new settings work correctly

#### **What Manual Sync Does:**
1. **Scans Libraries directory**: Checks all files for changes
2. **Compares with source**: Determines what has changed since last sync
3. **Creates backup**: (if enabled) Creates timestamped backup of destination
4. **Copies changes**: Transfers modified files to version-specific storage
5. **Updates logs**: Records all operations with timestamps
6. **Shows results**: Displays success message or error details

#### **Manual Sync Results:**
- **Success**: "✓ Manual sync completed: X files synchronized"
- **No Changes**: "Manual sync: No changes detected"
- **Error**: "✗ Manual sync error: [detailed error message]"

---

## Settings and Configuration

The application provides comprehensive configuration options to customize the auto-sync behavior to your specific needs.

### ⚙️ **Accessing Settings**

#### **Main Settings Access:**
1. Click **"Settings"** in the menu bar
2. Select **"Sync"** submenu
3. Choose your desired option:
   - **"Auto-Sync Settings..."** - Configure synchronization behavior
   - **"View Sync Status"** - Monitor current sync statistics and activity

#### **Alternative Access Methods:**
- **File Menu**: `File → Setup Automation Studio Paths...` for AS configuration
- **File Menu**: `File → Change Project Root...` for project location
- **File Menu**: `File → Manual Sync Now` for immediate synchronization

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

### 📋 **Detailed Error Messages and Solutions**

#### **"Source libraries directory not found"**
- **Full Message**: "Source libraries directory not found: [path]"
- **Meaning**: The version-specific library folder is missing from your project
- **Cause**: Libraries_45 or Libraries_6 folder doesn't exist in your Logical directory
- **Solutions**:
  1. Create the missing directory (e.g., `Logical/Libraries_45`)
  2. Copy your existing libraries to the version-specific folder
  3. Verify folder naming is exact (Libraries_45, not Libraries45 or libraries_45)
  4. Check that you have the correct project root selected

#### **"Auto-sync failed"**
- **Full Message**: "Auto-sync failed: [specific error]"
- **Meaning**: The automatic synchronization process encountered an error
- **Common Causes**:
  - File permission issues (read-only files)
  - Insufficient disk space
  - Files in use by another application
  - Network drive disconnection
- **Solutions**:
  1. Check file permissions (ensure files are not read-only)
  2. Verify sufficient disk space (check both source and target locations)
  3. Close any applications that might be using the files
  4. Retry with `File → Manual Sync Now`
  5. Check Session Log for specific error details

#### **"Invalid project root"**
- **Full Message**: "The selected directory does not appear to be a valid project root"
- **Meaning**: The chosen folder doesn't have the required structure
- **Solutions**:
  1. Ensure the folder contains both "Logical" and "Physical" subdirectories
  2. Check that subdirectory names are spelled correctly and match case
  3. Verify you selected the correct parent folder (not Logical or Physical itself)
  4. Ensure you have read permissions to the directory

#### **"Automation Studio executable not found"**
- **Full Message**: "Automation Studio executable not found: [path]"
- **Meaning**: The configured AS executable path is invalid or inaccessible
- **Solutions**:
  1. Go to `File → Setup Automation Studio Paths...`
  2. Remove the invalid entry and re-add it
  3. Browse to the correct AutomationStudio.exe location
  4. Verify AS installation is complete and functional
  5. Check file permissions and path accessibility

### 🔧 **Advanced Troubleshooting**

#### **Application Won't Start:**
- **Check Windows Event Viewer**: Look for application errors
- **Verify 64-bit Windows**: Application requires 64-bit OS
- **Run as Administrator**: Try right-click → "Run as administrator"
- **Check User Permissions**: Ensure write access to user profile folder
- **Reinstall**: Uninstall and reinstall the application

#### **Sync Operations Are Slow:**
- **Large Project**: Consider increasing periodic sync interval
- **Network Drives**: Move project to local drive for better performance
- **Antivirus**: Add application and project folders to antivirus exclusions
- **Disk Space**: Ensure sufficient free space on all drives

#### **Multiple AS Versions Interfering:**
- **Close All AS Instances**: Don't run multiple AS versions simultaneously
- **Check Process Monitor**: Use Task Manager to verify only one AS is running
- **Restart Selector**: Close and reopen Selector if AS detection seems stuck

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

### 💡 **Pro Tips and Advanced Usage**

#### **Keyboard Shortcuts and Quick Actions**:
- **F5**: Refresh studio list (same as clicking "Refresh List")
- **Enter**: Open project (when studio is selected in the list)
- **Escape**: Close any open dialog boxes
- **Double-Click**: Select and immediately open project with chosen AS version
- **Alt + F**: Open File menu quickly
- **Alt + S**: Open Settings menu quickly
- **Alt + H**: Open Help menu quickly

#### **Workflow Optimization Strategies**:

##### **For Daily Work:**
1. **Leave Selector Open**: Keep the application running in the background for continuous auto-sync
2. **Use Desktop Shortcut**: Quick access without navigating Start Menu
3. **Monitor Session Log**: Watch for sync confirmations to verify your work is protected
4. **Regular Manual Sync**: Use `File → Manual Sync Now` before important work sessions
5. **Pre-Select Version**: Application remembers last used AS version for faster workflow

##### **For Project Management:**
1. **Consistent Naming**: Use clear, descriptive names for your version-specific directories
2. **Regular Backups**: Let the backup system work (keep it enabled)
3. **Version Testing**: Test your project in both AS versions before deployment
4. **Documentation**: Keep notes about version-specific requirements or limitations

##### **For Team Environments:**
1. **Shared Projects**: Use network-accessible project roots for team collaboration
2. **Standardized Setup**: Ensure all team members use the same AS installation paths
3. **Regular Sync**: Encourage manual sync before committing changes to version control
4. **Log Monitoring**: Check logs for team-wide sync issues

#### **Performance Optimization**:

##### **For Large Projects:**
1. **Adjust Sync Frequency**: Increase periodic sync interval to 10-15 minutes
2. **Monitor Disk Space**: Large projects with frequent backups use more space
3. **Clean Old Logs**: Periodically clean log directories to free space
4. **SSD Storage**: Use solid-state drives for better file operation performance

##### **For System Resources:**
1. **Close Unused AS**: Don't run multiple AS versions simultaneously
2. **Background Monitoring**: The application uses minimal resources when idle
3. **Memory Usage**: Large projects may require more system RAM
4. **CPU Impact**: Frequent sync operations use minimal CPU time

#### **Troubleshooting Shortcuts and Quick Fixes**:

##### **First-Level Diagnostics:**
1. **Check Session Log First**: 90% of issues are visible in the log with clear error messages
2. **Try Manual Sync**: `File → Manual Sync Now` tests if the sync system is working correctly
3. **Restart Both Applications**: Close AS and Selector, then restart - resolves many temporary issues
4. **Check File Permissions**: Ensure write access to both project folders and user directory

##### **Second-Level Diagnostics:**
1. **Review Configuration**: Verify AS paths and project root are correct
2. **Test with Simple Project**: Use a minimal project to isolate configuration vs. project issues
3. **Check System Resources**: Verify disk space, memory, and file handles
4. **Examine Log Files**: Look at permanent log files for historical error patterns

##### **Advanced Diagnostics:**
1. **Process Monitoring**: Use Task Manager to verify AS processes are detected correctly
2. **File System Check**: Ensure project folders are accessible and not corrupted
3. **Network Issues**: If using network drives, check connectivity and permissions
4. **Antivirus Interference**: Add application and project folders to antivirus exclusions

### ⚠️ **Critical Safety Guidelines**

#### **Absolute Rules - Never Do These:**
- ❌ **Edit Active Files Directly**: Never manually modify Libraries/, Physical.pkg, or OCB.apj
  - **Why**: These files are automatically managed and will be overwritten
  - **Instead**: Always edit the version-specific files (Libraries_45, Libraries_6, etc.)

- ❌ **Delete Version-Specific Directories While AS Is Running**: Never remove Libraries_45, Libraries_6, etc. during active sessions
  - **Why**: Can cause sync failures and data loss
  - **Instead**: Close AS first, then make structural changes

- ❌ **Run Multiple AS Versions Simultaneously**: Don't open AS 4.5 and AS 6 at the same time on the same project
  - **Why**: Can cause file conflicts and sync confusion
  - **Instead**: Close one AS version before opening another

- ❌ **Disable Auto-Sync Without Backup Strategy**: Don't turn off auto-sync unless you have alternative data protection
  - **Why**: Risk of losing work when switching versions
  - **Instead**: Keep auto-sync enabled or implement manual backup procedures

#### **Always Follow These Practices:**
- ✅ **Let Auto-Sync Complete**: Wait for sync confirmation before switching AS versions
  - **How to Verify**: Check Session Log for "✓ Auto-sync completed" message

- ✅ **Monitor Session Log**: Regularly check for sync confirmations and error messages
  - **What to Look For**: Green checkmarks for success, red X marks for errors

- ✅ **Keep Backups Enabled**: Maintain the automatic backup system for safety
  - **Configuration**: Settings → Sync → Auto-Sync Settings → "Create backups before sync"

- ✅ **Test in Both Versions**: Verify your project works in all AS versions before deployment
  - **Process**: Test critical functionality in AS 4.5 and AS 6 separately

- ✅ **Regular Configuration Checks**: Periodically verify your AS paths and project root are correct
  - **When**: After AS updates, system changes, or moving project locations

#### **Emergency Procedures:**

##### **If Sync Fails:**
1. **Don't Panic**: Your work is likely still in the active Libraries directory
2. **Try Manual Sync**: Use `File → Manual Sync Now` to attempt immediate sync
3. **Check Backups**: Look for backup directories with timestamps
4. **Manual Copy**: As last resort, manually copy changed files to version-specific directories

##### **If Files Are Missing:**
1. **Check Backup Directories**: Look for folders like `Libraries_6_backup_YYYYMMDD_HHMMSS`
2. **Check Log Files**: Review session logs for sync history and error messages
3. **Verify Project Structure**: Ensure all required directories exist
4. **Restore from Version Control**: If using Git/SVN, restore from repository

##### **If AS Won't Start:**
1. **Verify Project Structure**: Check that all required files exist (OCB.apj, Physical.pkg)
2. **Check AS Installation**: Ensure AS itself is working by testing with another project
3. **Reset Project Files**: Use the Selector to re-setup the project files
4. **Contact Support**: If all else fails, gather log files and contact technical support

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
