# PyInstaller Configuration Guide

## 🔧 **How to Customize Your Installer Build**

This guide explains how to modify PyInstaller configurations for the Automation Studio Selector.

---

## 📝 **Configuration Files**

### **1. Basic Configuration**
- **File**: `automation_studio_selector.spec` (current simple version)
- **Use for**: Basic builds with minimal customization

### **2. Advanced Configuration** 
- **File**: `automation_studio_selector_advanced.spec` (enhanced version)
- **Use for**: Full control over build process

---

## ⚙️ **Common Configuration Changes**

### **🎯 Application Information**

```python
# In the advanced spec file, modify these variables:
APP_NAME = 'YourAppName'                    # Executable name
APP_VERSION = '2.0.0'                       # Version number
APP_AUTHOR = 'Your Name - Your Company'     # Author info
```

### **🐛 Debug and Console Options**

```python
DEBUG_MODE = True           # Enable for troubleshooting
CONSOLE_MODE = True         # Show console window for debugging
```

**When to use**:
- **DEBUG_MODE = True**: When you need to see detailed error messages
- **CONSOLE_MODE = True**: When you want to see print statements and errors

### **📦 Size Optimization**

```python
UPX_COMPRESSION = True      # Compress executable (smaller size)
OPTIMIZE_SIZE = True        # Remove unnecessary files
INCLUDE_MSVCRT = False      # Exclude runtime if not needed
```

**Trade-offs**:
- **UPX_COMPRESSION = True**: Smaller file, longer startup time
- **OPTIMIZE_SIZE = True**: Smaller file, might miss some dependencies

### **🎨 Icon Configuration**

```python
# Option 1: No icon
ICON_FILE = None

# Option 2: Use custom icon (must be .ico format)
ICON_FILE = 'assets/app_icon.ico'
```

**How to create .ico file**:
1. Convert your PNG logo to ICO format using online converter
2. Place in `assets/` folder
3. Update the path in spec file

### **📁 Additional Files**

```python
EXTRA_DATA_FILES = [
    ('your_file.txt', '.'),              # Include in root
    ('docs/manual.pdf', 'docs'),         # Include in subfolder
    ('config/default.ini', 'config'),    # Include config files
]
```

### **🔧 Module Configuration**

```python
# Include additional modules
EXTRA_HIDDEN_IMPORTS = [
    'your_custom_module',
    'third_party_library',
]

# Exclude unnecessary modules (reduces size)
EXCLUDED_MODULES = [
    'matplotlib',    # Don't include if not using plots
    'numpy',         # Don't include if not using math
    'pandas',        # Don't include if not using data analysis
]
```

---

## 🚀 **Build Commands**

### **Using Basic Configuration**
```bash
pyinstaller automation_studio_selector.spec --clean
```

### **Using Advanced Configuration**
```bash
pyinstaller automation_studio_selector_advanced.spec --clean
```

### **Command Line Options**
```bash
# Clean build (recommended)
pyinstaller your_spec.spec --clean

# No confirmation prompts
pyinstaller your_spec.spec --noconfirm

# Specify different output directory
pyinstaller your_spec.spec --distpath custom_dist

# Specify different build directory  
pyinstaller your_spec.spec --workpath custom_build

# Add debug output
pyinstaller your_spec.spec --log-level DEBUG
```

---

## 🛠️ **Advanced Configurations**

### **💾 Single File Executable**

Modify the EXE section in your spec file:

```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,    # Include binaries in exe
    a.zipfiles,    # Include zip files in exe
    a.datas,       # Include data files in exe
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    # Single file mode
    onefile=True,          # Create single executable
    icon=ICON_FILE,
)

# Remove COLLECT section for single file
# coll = COLLECT(...)  # Comment this out
```

**Pros**: Single file, easy distribution
**Cons**: Slower startup, larger memory usage

### **🔐 Encryption and Security**

```python
# Enable encryption
from PyInstaller.utils.cliutils import archive_viewer
block_cipher = pyi_crypto.PyiBlockCipher(key='your-secret-key-here')

# In Analysis section:
cipher=block_cipher,

# In PYZ section:
cipher=block_cipher
```

### **🖥️ Windows-Specific Options**

```python
exe = EXE(
    # ... other parameters ...
    
    # Windows UAC settings
    uac_admin=True,              # Require admin rights
    uac_uiaccess=False,          # UI access privilege
    
    # Windows manifest options
    manifest='app.manifest',     # Custom manifest file
    
    # Version information
    version='version_info.txt',  # Detailed version info
)
```

### **📋 Custom Version Information**

Edit `version_info.txt`:

```python
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2,0,0,0),          # File version
    prodvers=(2,0,0,0),          # Product version
    # ... other settings ...
  ),
  kids=[
    StringFileInfo([
      StringTable(u'040904B0', [
        StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'Your App Description'),
        StringStruct(u'FileVersion', u'2.0.0.0'),
        StringStruct(u'ProductName', u'Your Product Name'),
        StringStruct(u'ProductVersion', u'2.0.0.0'),
        StringStruct(u'LegalCopyright', u'© 2025 Your Company'),
      ])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

---

## 🎛️ **Build Profiles**

Create different spec files for different purposes:

### **Development Build** (`dev.spec`)
```python
DEBUG_MODE = True
CONSOLE_MODE = True
UPX_COMPRESSION = False
OPTIMIZE_SIZE = False
```

### **Release Build** (`release.spec`)
```python
DEBUG_MODE = False
CONSOLE_MODE = False
UPX_COMPRESSION = True
OPTIMIZE_SIZE = True
```

### **Testing Build** (`test.spec`)
```python
DEBUG_MODE = True
CONSOLE_MODE = False
UPX_COMPRESSION = False
OPTIMIZE_SIZE = False
```

---

## 🔍 **Troubleshooting Build Issues**

### **Missing Modules**
**Problem**: "ModuleNotFoundError" when running executable

**Solution**: Add to `hiddenimports`:
```python
hiddenimports=[
    'missing_module_name',
]
```

### **Large File Size**
**Problem**: Executable is too big

**Solutions**:
1. Add more modules to `excludes`
2. Enable UPX compression
3. Use single file mode
4. Remove unnecessary data files

### **Slow Startup**
**Problem**: Application takes long to start

**Solutions**:
1. Disable UPX compression
2. Use directory mode instead of single file
3. Reduce number of included modules
4. Use lazy imports in your code

### **Missing Data Files**
**Problem**: Logo or config files not found

**Solution**: Add to `datas`:
```python
datas=[
    ('path/to/file', 'destination/folder'),
]
```

### **DLL Issues**
**Problem**: Missing or conflicting DLLs

**Solution**: Add to `binaries`:
```python
binaries=[
    ('path/to/dll', '.'),
]
```

---

## 📊 **Build Optimization Tips**

### **Size Optimization**
1. **Exclude unused modules**: Add to `excludes` list
2. **Use UPX compression**: Enable in spec file
3. **Remove debug info**: Set `strip=True`
4. **Minimize data files**: Only include necessary files

### **Performance Optimization**
1. **Disable UPX for startup speed**: Set `upx=False`
2. **Use directory mode**: Faster than single file
3. **Lazy imports**: Import modules only when needed
4. **Reduce hidden imports**: Only include necessary modules

### **Security Optimization**
1. **Enable encryption**: Use block cipher
2. **Strip symbols**: Set `strip=True`
3. **Remove debug info**: Set `debug=False`
4. **Exclude development tools**: Add to excludes

---

## 🎯 **Example Build Scripts**

### **Quick Development Build**
```batch
@echo off
echo Building development version...
pyinstaller automation_studio_selector_advanced.spec --clean --noconfirm
echo Development build complete!
```

### **Release Build Script**
```batch
@echo off
echo Building release version...

REM Update version in spec file if needed
REM python update_version.py

REM Clean build
pyinstaller automation_studio_selector_advanced.spec --clean --noconfirm

REM Test the executable
echo Testing executable...
dist\AutomationStudioSelector\AutomationStudioSelector.exe --version

echo Release build complete!
```

---

## 📝 **Configuration Checklist**

Before building:

- [ ] Update version numbers in spec file and version_info.txt
- [ ] Verify all data files are included in `datas`
- [ ] Check that all required modules are in `hiddenimports`
- [ ] Set appropriate debug/console modes
- [ ] Choose optimization level (size vs speed)
- [ ] Test with clean Python environment
- [ ] Verify icon file exists (if using custom icon)
- [ ] Check exclusion list to avoid unnecessary modules

---

**Remember**: Always test your executable on a clean machine without Python installed to ensure it works standalone!

