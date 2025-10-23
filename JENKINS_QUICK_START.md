# Jenkins Quick Start Guide

**No GUI Configuration Needed!**

Created by: Vitaly Grosman - Indigo R&D Division

---

## 🎯 The Perfect Jenkins Command

```bash
python main.py -project-path "C:\Jenkins\workspace\MyProject" -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" -as-version 45 -prepare-only -silent
```

**That's it!** Fresh Git pull → Run command → Project ready!

---

## 📋 Required Parameters for Jenkins/QA

| Parameter | Value | Description |
|-----------|-------|-------------|
| `-project-path` | `C:\Jenkins\workspace\MyProject` | Where Git cloned your project |
| `-studio-path` | `C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe` | AS executable location |
| `-as-version` | `45` or `6` | Which AS version (determines which files to copy) |
| `-prepare-only` | (flag) | Don't launch AS, just configure files |
| `-silent` | (flag) | No output (clean Jenkins logs) |

---

## 🚀 Complete Jenkins Script

```batch
@echo off
REM jenkins_build.bat

echo ========================================
echo  Jenkins Build for AS Project
echo ========================================

REM Project pulled by Jenkins to %WORKSPACE%
set PROJECT=%WORKSPACE%
set AS45_EXE=C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe
set SELECTOR=python C:\Tools\Selector\main.py

echo Configuring project for AS 4.5...

%SELECTOR% ^
  -project-path "%PROJECT%" ^
  -studio-path "%AS45_EXE%" ^
  -as-version 45 ^
  -prepare-only ^
  -silent

if %errorlevel% equ 0 (
    echo ✓ Project configured successfully
    echo   Libraries copied from Libraries_45
    echo   Physical.pkg updated from Physical_45.pkg  
    echo   OCB.apj updated from OCB_as45.apj
    echo   Ready for build!
) else (
    echo ✗ Configuration FAILED - Error code: %errorlevel%
    exit /b 1
)

REM Add your build/test commands here
REM Example: Call AS command-line build tools

exit /b 0
```

---

## 🎯 Why Specify AS Version?

### **The Application Needs to Know:**

**For AS 4.5 (`-as-version 45`):**
- Copy from `Libraries_45` → `Libraries`
- Copy from `Physical_45.pkg` → `Physical.pkg`
- Copy from `OCB_as45.apj` → `OCB.apj`

**For AS 6 (`-as-version 6`):**
- Copy from `Libraries_6` → `Libraries`
- Copy from `Physical_6.pkg` → `Physical.pkg`
- Copy from `OCB_as6.apj` → `OCB.apj`

**Without the version, the app doesn't know which files to copy!**

---

## ✅ Project Structure Requirements

Your Git repository must contain:

```
MyProject/
├── Logical/
│   ├── Libraries/          (empty or will be overwritten)
│   ├── Libraries_45/       ← Source files for AS 4.5
│   └── Libraries_6/        ← Source files for AS 6
├── Physical/
│   ├── Physical.pkg        (empty or will be overwritten)
│   ├── Physical_45.pkg     ← Source file for AS 4.5
│   └── Physical_6.pkg      ← Source file for AS 6
├── OCB.apj                (empty or will be overwritten)
├── OCB_as45.apj           ← Source file for AS 4.5
└── OCB_as6.apj            ← Source file for AS 6
```

---

## 🔧 Different AS Versions

### **For AS 4.5:**
```bash
python main.py ^
  -project-path "C:\Jenkins\workspace\MyProject" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only ^
  -silent
```

### **For AS 6:**
```bash
python main.py ^
  -project-path "C:\Jenkins\workspace\MyProject" ^
  -studio-path "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe" ^
  -as-version 6 ^
  -prepare-only ^
  -silent
```

---

## 🎛️ Parameterized Jenkins Job

**Add Build Parameters in Jenkins:**
- **AS_VERSION**: Choice parameter (45 or 6)

**Build Script:**
```batch
@echo off

REM Set AS path based on parameter
if "%AS_VERSION%"=="45" (
    set AS_EXE=C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe
) else (
    set AS_EXE=C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe
)

echo Using AS version: %AS_VERSION%
echo AS executable: %AS_EXE%

REM Configure project
python C:\Tools\Selector\main.py ^
  -project-path "%WORKSPACE%" ^
  -studio-path "%AS_EXE%" ^
  -as-version %AS_VERSION% ^
  -prepare-only ^
  -silent

if %errorlevel% equ 0 (
    echo SUCCESS: Project ready for AS %AS_VERSION%
) else (
    echo FAILED: Configuration error
    exit /b 1
)
```

---

## 🎯 Real QA Workflow

### **Your Exact Scenario:**

```
1. Jenkins pulls from Git
   ↓
2. Project lands in: C:\Jenkins\workspace\MyBuild
   ↓
3. Run selector command:
   python main.py 
     -project-path "C:\Jenkins\workspace\MyBuild"
     -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe"
     -as-version 45
     -prepare-only
     -silent
   ↓
4. Project configured for AS 4.5
   ↓
5. Run your build/test tools
   ↓
6. Done!
```

**NO GUI EVER OPENED!**

---

## 💡 Key Points

### **✅ DO:**
- Always specify `-as-version` when using `-studio-path`
- Use `-prepare-only` for Jenkins (don't launch AS)
- Use `-silent` for clean Jenkins logs
- Check exit codes (`%errorlevel%`)

### **❌ DON'T:**
- Don't forget `-as-version` (app needs to know which files to copy)
- Don't launch AS on build servers (use `-prepare-only`)
- Don't use project names (use `-project-path` for fresh Git clones)

---

## 🧪 Test Your Setup

**Before using in Jenkins, test manually:**

```batch
@echo off
REM test_jenkins_command.bat

echo Testing Jenkins-style command...

python main.py ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only ^
  -verbose

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  TEST PASSED!
    echo ========================================
    echo Your Jenkins command will work!
) else (
    echo.
    echo ========================================
    echo  TEST FAILED!
    echo ========================================
    echo Fix errors before using in Jenkins
)

pause
```

---

## 📞 Quick Reference

### **Minimum Jenkins Command:**
```bash
python main.py -project-path PATH -studio-path AS_EXE -as-version 45 -prepare-only
```

### **Production Jenkins Command:**
```bash
python main.py -project-path "%WORKSPACE%" -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" -as-version 45 -prepare-only -silent
```

### **AS Version Values:**
- **AS 4.5**: Use `-as-version 45`
- **AS 6**: Use `-as-version 6`

---

**Ready for Jenkins!** 🚀
