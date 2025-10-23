# ⚠️ IMPORTANT: Parameter Matching Guide

## 🎯 Critical Rule

**The `-as-version` parameter MUST match the intended AS version, not the project folder name!**

---

## ❌ Common Mistake

### **WRONG:**
```batch
REM DON'T do this - mismatch between project and AS version
python main.py ^
  -project-path "C:\...\AS45" ^     ← AS45 project directory
  -studio-path "C:\...\AS6\...exe" ^ ← AS 6 executable
  -as-version 6 ^                    ← Tells app to copy AS 6 files
  -prepare-only
```

**Problem:** This copies AS 6 files into the AS45 project directory!
- Copies `Libraries_6` instead of `Libraries_45`
- Copies `Physical_6.pkg` instead of `Physical_45.pkg`
- Copies `OCB_as6.apj` instead of `OCB_as45.apj`
- Result: AS45 project now has AS 6 configuration (wrong!)

---

## ✅ Correct Usage

### **Rule: Match AS Version to Project's Intended Version**

#### **For AS45 Project Directory:**
```batch
python main.py ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^    ← Use 45 for AS 4.5
  -prepare-only
```

**Result:**
- ✓ Copies `Libraries_45` → `Libraries`
- ✓ Copies `Physical_45.pkg` → `Physical.pkg`
- ✓ Copies `OCB_as45.apj` → `OCB.apj`
- ✓ Project configured correctly for AS 4.5

#### **For As6 Project Directory:**
```batch
python main.py ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\As6" ^
  -studio-path "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe" ^
  -as-version 6 ^     ← Use 6 for AS 6
  -prepare-only
```

**Result:**
- ✓ Copies `Libraries_6` → `Libraries`
- ✓ Copies `Physical_6.pkg` → `Physical.pkg`
- ✓ Copies `OCB_as6.apj` → `OCB.apj`
- ✓ Project configured correctly for AS 6

#### **For OCB Project Directory:**

**Option A: Configure for AS 4.5**
```batch
python main.py ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only
```

**Option B: Configure for AS 6**
```batch
python main.py ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB" ^
  -studio-path "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe" ^
  -as-version 6 ^
  -prepare-only
```

---

## 🔑 Understanding the Parameters

### **`-project-path`**
- **What it is**: Physical directory location on disk
- **What it's for**: Tells app WHERE to work
- **Can be anything**: Folder name doesn't matter
- **Examples**: `C:\Projects\Test`, `C:\Jenkins\Build`, `C:\MyProject`

### **`-studio-path`**
- **What it is**: Path to AutomationStudio.exe
- **What it's for**: Used ONLY if you want to launch AS (full mode)
- **In prepare-only**: Only used to identify AS version if auto-detection fails
- **Examples**: `C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe`

### **`-as-version`** ⚠️ **MOST IMPORTANT**
- **What it is**: Which AS version configuration to use
- **What it controls**: Which source files to copy
  - `45` = Copy from `Libraries_45`, `Physical_45.pkg`, `OCB_as45.apj`
  - `6` = Copy from `Libraries_6`, `Physical_6.pkg`, `OCB_as6.apj`
- **Must match**: Your intended AS version, NOT your folder name

---

## 📋 Decision Matrix

**Question: What `-as-version` should I use?**

| Scenario | Use `-as-version` |
|----------|-------------------|
| Want to use AS 4.5 | `45` |
| Want to use AS 6 | `6` |
| Project folder named "AS45" | **Doesn't matter** - use what AS version you want |
| Project folder named "As6" | **Doesn't matter** - use what AS version you want |
| Studio-path points to AS45 | Usually `45`, but can be `6` if needed |
| Studio-path points to AS6 | Usually `6`, but can be `45` if needed |

**The ONLY thing that matters: Which AS version do you want to run the project with?**

---

## 🎯 Your Three Projects - Correct Scripts

### **Script 1: Prepare AS45 Project**
```batch
@echo off
echo Preparing AS45 project for AS 4.5...

python "C:\Work\Indigo\Python\Selector\Selector\main.py" ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only

pause
```

### **Script 2: Prepare As6 Project**
```batch
@echo off
echo Preparing As6 project for AS 6...

python "C:\Work\Indigo\Python\Selector\Selector\main.py" ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\As6" ^
  -studio-path "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe" ^
  -as-version 6 ^
  -prepare-only

pause
```

### **Script 3: Prepare OCB Project (for AS 4.5)**
```batch
@echo off
echo Preparing OCB project for AS 4.5...

python "C:\Work\Indigo\Python\Selector\Selector\main.py" ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only

pause
```

---

## 💡 Key Takeaway

**Folder name ≠ AS version to use**

The `-as-version` parameter tells the application:
- **Which Libraries folder to copy from** (`Libraries_45` vs `Libraries_6`)
- **Which Physical.pkg to use** (`Physical_45.pkg` vs `Physical_6.pkg`)
- **Which project file to use** (`OCB_as45.apj` vs `OCB_as6.apj`)

**It does NOT**:
- Depend on your folder name
- Have to match the studio-path
- Change based on where the project is located

**Choose based on: Which Automation Studio version do you want to use?**

---

## 🧪 Test to Verify

Run this test to see the difference:

```batch
@echo off
echo TEST 1: AS45 project with AS 4.5 files
python "C:\Work\Indigo\Python\Selector\Selector\main.py" ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only

echo.
echo Now check OCB.apj - it should show "Version 4.5"
pause

echo.
echo TEST 2: AS45 project with AS 6 files (WRONG - but to see the difference)
python "C:\Work\Indigo\Python\Selector\Selector\main.py" ^
  -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45" ^
  -studio-path "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe" ^
  -as-version 6 ^
  -prepare-only

echo.
echo Now check OCB.apj - it should show "Version 6" (different!)
pause
```

This will clearly show how `-as-version` controls which files get copied!

---

**Remember: `-as-version` = Which AS version's files to use, regardless of folder names or paths!**
