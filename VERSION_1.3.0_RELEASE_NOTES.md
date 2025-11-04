# Version 1.3.0 Release Notes
**Release Date:** October 28, 2025  
**Created by:** Vitaly Grosman - Indigo R&D Division

---

## 🎯 What's New in Version 1.3.0

### 📋 OCB Project Context

The OCB project requires dual AS4.5/AS6 support due to:
- **AS 4.5 moving toward EOL**, but many configurations cannot migrate
- **Main configurations moving to AS6**: Hila_MR, Sufa (unified), Ayala
- **Configurations staying on AS4.5**: Arad ECO, Stacker/Jigs/TBs, Eilat MR2, Shani, Barak, Tamar
- **Single unified OCB approach** chosen over maintaining two separate projects to reduce overhead

Version 1.3.0 makes this dual-version workflow seamless with smart scripts and simplified commands.

### 🚀 Major Feature: Smart Project Path Auto-Detection

Version 1.3.0 introduces **intelligent project path detection** for batch scripts, making it easier to use the tool in different environments without hardcoding paths.

#### Key Enhancement
- **Auto-Detection Logic**: Scripts now automatically detect the project path when run from the project's `\scripts` directory
- **Fallback Mechanism**: First tries the default hardcoded path, then auto-detects if not found
- **Error Handling**: Clear error messages guide users if neither method works
- **Validation**: Checks for `.apj` files to verify it's a valid project directory

---

## 📝 Detailed Changes

### OCB Project Ready-to-Use Scripts

Your OCB project now includes two convenient scripts in the `\scripts` directory:

**Location:** `OCB\scripts\`
- **prepare45.bat** - Double-click to convert project to AS 4.5
- **prepare6.bat** - Double-click to convert project to AS 6

**How it works:**
1. Navigate to your `OCB\scripts\` directory
2. Double-click `prepare45.bat` (for AS 4.5) or `prepare6.bat` (for AS 6)
3. The script automatically:
   - Detects the project path (parent directory)
   - Copies the correct libraries
   - Updates Physical.pkg
   - Updates OCB.apj
4. Wait for "Project ready!" message
5. Done! Your project is converted

**Benefits:**
- ✅ No need to specify project path - auto-detected!
- ✅ No need to specify studio path - prepare-only mode!
- ✅ Just double-click and go
- ✅ Scripts travel with your project in Git
- ✅ Works on any machine

### Enhanced Batch Scripts
Both `test45.bat` and `test6.bat` now include:

1. **Smart Path Detection**
   - Tries default path first: `C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB`
   - If not found, assumes script is in `<project>\scripts\` directory
   - Uses parent directory as project path
   - Validates by checking for `.apj` files

2. **Better User Feedback**
   - Shows which path method is being used
   - Displays current directory when auto-detecting
   - Clear error messages with actionable suggestions
   - Shows actual project path being used

3. **Improved Flexibility**
   - Works in any environment (development, CI/CD, different machines)
   - No need to modify scripts when copying to different projects
   - Supports both hardcoded and dynamic path scenarios

### Example Usage

#### Scenario 1: Running from Default Path
```batch
C:\MyScripts> test45.bat
Using default project path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB
Configuring AS45 project for AS 4.5...
```

#### Scenario 2: Running from Project's Scripts Directory
```batch
C:\Projects\MyProject\scripts> test45.bat
Default path not found, attempting auto-detection...
Auto-detected project path: C:\Projects\MyProject
Configuring AS45 project for AS 4.5...
Project path: C:\Projects\MyProject
```

#### Scenario 3: Path Not Found
```batch
========================================
  ERROR: Cannot detect project path
========================================

Neither the default path exists:
  C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB

Nor could we auto-detect a project in parent directory:
  C:\SomeOtherLocation

Please either:
  1. Update the DEFAULT_PROJECT_PATH in this script
  2. Run this script from your project's \scripts directory
```

---

## 🎨 UI Updates

### About Dialog
- Updated version display to v1.3.0
- Added new feature highlight: "Smart project path auto-detection for scripts"
- Maintains clean, professional appearance

---

## 📦 Technical Updates

### Files Modified (9 files)
1. ✅ `test45.bat` - Enhanced with auto-detection logic
2. ✅ `test6.bat` - Enhanced with auto-detection logic
3. ✅ `main.py` - Version updated to 1.3.0
4. ✅ `version_info.txt` - Version metadata updated
5. ✅ `src/ui/main_window.py` - About dialog updated
6. ✅ `src/cli/cli_commands.py` - CLI version updated
7. ✅ `automation_studio_selector_advanced.spec` - Build version updated
8. ✅ `installer_script.iss` - Installer version updated
9. ✅ `VERSION_1.3.0_RELEASE_NOTES.md` - This file (NEW)

---

## 🔧 How It Works

### Detection Algorithm
```batch
1. Check if DEFAULT_PROJECT_PATH exists
   ├─ YES → Use default path
   └─ NO → Continue to step 2

2. Get current script directory
   └─ Get parent directory (project root candidate)

3. Check parent directory for .apj files
   ├─ FOUND → Use parent directory as project path
   └─ NOT FOUND → Show error with instructions
```

### Benefits
- **Portability**: Copy scripts between projects without modification
- **CI/CD Ready**: Works in automated build environments
- **User Friendly**: Clear feedback at every step
- **Backward Compatible**: Still supports hardcoded paths
- **Safe**: Validates project structure before proceeding

---

## 📋 Upgrade Instructions

### For Existing Users
1. **No action required** - The tool is backward compatible
2. If you want to use auto-detection:
   - Place `test45.bat` or `test6.bat` in your project's `\scripts` directory
   - Update the `DEFAULT_PROJECT_PATH` variable if your path differs

### For New Users
1. **Download** the installer: [AutomationStudioSelector_Setup_v1.3.0.exe](https://hp-my.sharepoint.com/:u:/p/vitaly_grosman/EaOKnHUZ1tlKjZGlEk23kRkBwOyI8lmW6uF4e4jWWDVJzg?e=og2YzG)
2. Install version 1.3.0 using the installer
3. Copy the example scripts to your project's `\scripts` directory
4. Run them without any modifications!

> 📥 **Download Link:**  
> https://hp-my.sharepoint.com/:u:/p/vitaly_grosman/EaOKnHUZ1tlKjZGlEk23kRkBwOyI8lmW6uF4e4jWWDVJzg?e=og2YzG

---

## 🏗️ Building from Source

### Build the Application
```batch
build_advanced.bat
```

### Create the Installer
```batch
build_installer.bat
```

### Test the Scripts
```batch
test45.bat
test6.bat
```

---

## 🐛 Known Issues
None at this time.

---

## 💡 Tips & Best Practices

1. **Organize Your Projects**
   - Create a `\scripts` directory in each project
   - Place conversion scripts there for easy access

2. **Customize Default Paths**
   - Update `DEFAULT_PROJECT_PATH` for your environment
   - Keep the auto-detection as a fallback

3. **Version Control**
   - Commit the scripts with your project
   - Team members can run them without configuration

4. **Build Automation**
   - Use these scripts in your CI/CD pipeline
   - Auto-detection works great in containerized environments

---

## 🙏 Acknowledgments

Special thanks to the Indigo R&D Division team for their continued support and feedback.

---

## 📞 Support

**Created by:** Vitaly Grosman  
**Email:** vitaly.grosman@hp.com  
**Organization:** Indigo R&D Division  

For issues, feedback, or suggestions, use the **Help → Send Feedback/Report Issue** menu in the application.

---

**© 2025 Indigo R&D Division - All Rights Reserved**

