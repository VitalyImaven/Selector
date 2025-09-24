# Automation Studio Selector - Deployment Guide

## 🚀 Creating Standalone Installer

This guide explains how to create a Windows installer that can be installed on any computer without requiring Python.

### Prerequisites

1. **Python Environment** (development machine only)
2. **Inno Setup** - Download from [https://jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php)

### Quick Build Process

#### Option 1: Automated Build (Recommended)
```bash
# Run the automated build script
build_installer.bat
```

#### Option 2: Manual Build
```bash
# Step 1: Install PyInstaller
pip install pyinstaller

# Step 2: Build executable
pyinstaller automation_studio_selector.spec --clean

# Step 3: Create installer with Inno Setup
# Open installer_script.iss in Inno Setup and click "Compile"
```

### Output Files

After building, you'll have:

1. **Executable**: `dist/AutomationStudioSelector/AutomationStudioSelector.exe`
2. **Installer**: `installer/AutomationStudioSelector_Setup_v1.0.0.exe`

### Installation Features

The installer provides:

- ✅ **Professional Windows installer** with modern wizard
- ✅ **Program Files installation** (requires admin rights)
- ✅ **Start Menu shortcuts**
- ✅ **Desktop shortcut** (optional)
- ✅ **Automatic uninstaller**
- ✅ **Clean removal** of user data
- ✅ **64-bit Windows check**
- ✅ **Version information** embedded in executable

### File Structure After Installation

```
C:\Program Files\Automation Studio Selector\
├── AutomationStudioSelector.exe          # Main application
├── assets\
│   └── logo.png                          # Your logo
├── auto_sync_config_example.xml          # Configuration template
├── README.md                             # Documentation
└── [Python runtime files]               # All Python dependencies included
```

### User Data Locations

- **Configuration**: `%USERPROFILE%\.automation_selector\config.json`
- **Auto-sync settings**: `%USERPROFILE%\.automation_selector\auto_sync_config.xml`
- **Session logs**: `%USERPROFILE%\.automation_selector\logs\`

### Distribution

The final installer (`AutomationStudioSelector_Setup_v1.0.0.exe`) can be:

- ✅ **Distributed to any Windows 64-bit computer**
- ✅ **Installed without Python**
- ✅ **Installed without internet connection**
- ✅ **Run by end users with standard privileges** (after admin installation)

### File Size

- **Executable folder**: ~150-200 MB (includes Python runtime + PyQt6)
- **Installer**: ~50-70 MB (compressed)

### Testing Deployment

1. **Test on clean machine**: Install on a computer without Python
2. **Test user permissions**: Ensure application runs with standard user account
3. **Test uninstall**: Verify clean removal of all files

### Troubleshooting

#### Build Issues
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that logo.png exists in assets folder
- Verify Python 3.8+ is being used

#### Runtime Issues
- Check Windows Event Viewer for application errors
- Verify 64-bit Windows (32-bit not supported)
- Ensure user has read/write permissions to user profile folder

### Version Updates

To create new version:
1. Update version numbers in `version_info.txt`
2. Update version in `installer_script.iss`
3. Rebuild using `build_installer.bat`

---

**Created by**: Vitaly Grosman  
**Organization**: Indigo R&D Division  
**Version**: 1.0.0
