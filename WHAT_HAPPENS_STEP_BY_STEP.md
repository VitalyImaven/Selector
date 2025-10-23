# What Happens Step-by-Step - Complete Process Explanation

**Understanding Prepare-Only vs Full Procedure**

Created by: Vitaly Grosman - Indigo R&D Division

---

## 🎯 Overview

The Automation Studio Selector performs file operations to configure your project for a specific AS version. There are **TWO modes**:

1. **Full Procedure** (with AS launch)
2. **Prepare-Only** (without AS launch)

---

## 📋 Complete Step-by-Step Process

### **STEP 1: Validate Project Structure** ✅
**What Happens:**
- Checks if the project directory exists
- Verifies `Logical` folder exists
- Verifies `Physical` folder exists
- Ensures folders are accessible

**Example Check:**
```
Project Root: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45
  ✓ Logical folder exists: C:\...\AS45\Logical
  ✓ Physical folder exists: C:\...\AS45\Physical
```

**If This Fails:**
- Error: "Project structure validation failed"
- Process stops immediately
- No files are modified

---

### **STEP 2: Clear Libraries Directory** 🗑️
**What Happens:**
- Goes to: `Logical\Libraries\` directory
- Deletes **ALL** files and subdirectories inside
- Leaves the `Libraries` folder itself (just empties it)

**Before:**
```
Logical/
├── Libraries/
│   ├── OldFile1.fun
│   ├── OldFile2.typ
│   ├── SubFolder/
│   │   └── OldFile3.xml
│   └── ...
```

**After:**
```
Logical/
├── Libraries/           ← Empty!
```

**Why This is Done:**
- Removes old files from previous AS version
- Prevents mixing files from different AS versions
- Ensures clean configuration

**Log Entry:**
```
Libraries directory cleared
```

---

### **STEP 3: Copy Version-Specific Libraries** 📋
**What Happens:**
- Identifies which AS version you selected (4.5 or 6)
- Finds the corresponding source directory
- Copies **ALL** contents to active Libraries folder

**For AS 4.5:**
```
Source: Logical\Libraries_45\
Target: Logical\Libraries\

Copies:
  Libraries_45/Config.xml        → Libraries/Config.xml
  Libraries_45/UserLib.fun       → Libraries/UserLib.fun
  Libraries_45/Subfolder/...     → Libraries/Subfolder/...
  (entire directory structure)
```

**For AS 6:**
```
Source: Logical\Libraries_6\
Target: Logical\Libraries\

Copies:
  Libraries_6/Config.xml         → Libraries/Config.xml
  Libraries_6/UserLib.fun        → Libraries/UserLib.fun
  Libraries_6/Subfolder/...      → Libraries/Subfolder/...
  (entire directory structure)
```

**File Operations:**
- Preserves file timestamps
- Maintains directory structure
- Copies all file types (*.fun, *.typ, *.xml, etc.)
- Recursive copy (includes all subdirectories)

**Log Entry:**
```
Libraries copied from Libraries_45 to Libraries
  - 15 files copied
  - 3 directories created
```

**If This Fails:**
- Error: "Source libraries directory not found"
- Check that `Libraries_45` or `Libraries_6` exists
- Process stops

---

### **STEP 4: Update Physical.pkg File** 📄
**What Happens:**
- Goes to: `Physical\` directory
- If `Physical.pkg` exists, **deletes** it
- Creates new `Physical.pkg` by copying from version-specific file

**For AS 4.5:**
```
Source: Physical\Physical_45.pkg
Target: Physical\Physical.pkg

Actions:
  1. Delete: Physical\Physical.pkg (if exists)
  2. Copy: Physical_45.pkg → Physical.pkg
```

**For AS 6:**
```
Source: Physical\Physical_6.pkg
Target: Physical\Physical.pkg

Actions:
  1. Delete: Physical\Physical.pkg (if exists)
  2. Copy: Physical_6.pkg → Physical.pkg
```

**Before:**
```
Physical/
├── Physical.pkg           ← Old file (maybe for AS 6)
├── Physical_45.pkg        ← AS 4.5 template
└── Physical_6.pkg         ← AS 6 template
```

**After (if AS 4.5 selected):**
```
Physical/
├── Physical.pkg           ← NEW! Copied from Physical_45.pkg
├── Physical_45.pkg        ← Unchanged (kept as backup)
└── Physical_6.pkg         ← Unchanged (kept as backup)
```

**Why This is Done:**
- Physical.pkg contains hardware configuration
- Different AS versions may have different format
- Ensures compatibility with selected AS version

**Log Entry:**
```
File deleted: Physical\Physical.pkg
File copied: Physical_45.pkg → Physical.pkg
Physical.pkg updated for Automation Studio 4.5
```

**If This Fails:**
- Error: "Source Physical.pkg not found"
- Check that `Physical_45.pkg` or `Physical_6.pkg` exists
- Process stops

---

### **STEP 5: Update Project File (OCB.apj)** 📁
**What Happens:**
- Goes to: Project root directory
- If `OCB.apj` exists, **deletes** it
- Creates new `OCB.apj` by copying from version-specific template

**For AS 4.5:**
```
Source: OCB_as45.apj
Target: OCB.apj

Actions:
  1. Delete: OCB.apj (if exists)
  2. Copy: OCB_as45.apj → OCB.apj
```

**For AS 6:**
```
Source: OCB_as6.apj
Target: OCB.apj

Actions:
  1. Delete: OCB.apj (if exists)
  2. Copy: OCB_as6.apj → OCB.apj
```

**Before:**
```
ProjectRoot/
├── OCB.apj                ← Old file (maybe for AS 6)
├── OCB_as45.apj           ← AS 4.5 template
└── OCB_as6.apj            ← AS 6 template
```

**After (if AS 4.5 selected):**
```
ProjectRoot/
├── OCB.apj                ← NEW! Copied from OCB_as45.apj
├── OCB_as45.apj           ← Unchanged (kept as template)
└── OCB_as6.apj            ← Unchanged (kept as template)
```

**Why This is Done:**
- Main project file format differs between AS versions
- OCB.apj is what you double-click to open the project
- Now anyone can double-click OCB.apj and it opens with correct AS version
- Project file contains AS version-specific settings

**Log Entry:**
```
File deleted: OCB.apj
File copied: OCB_as45.apj → OCB.apj
Project file updated for Automation Studio 4.5
```

**If This Fails:**
- Error: "Source project file not found"
- Check that `OCB_as45.apj` or `OCB_as6.apj` exists
- Process stops

---

### **STEP 6: Open Project with Automation Studio** 🚀

**This step ONLY happens in FULL mode, NOT in prepare-only mode!**

#### **Full Procedure Mode:**
**What Happens:**
- Locates the AS executable (e.g., `C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe`)
- Launches AS with the project file: `AutomationStudio.exe "C:\...\OCB.apj"`
- AS starts and opens your project
- Process continues running AS

**Log Entry:**
```
Project opened: OCB.apj with Automation Studio 4.5
```

**If This Fails:**
- Error: "Automation Studio executable not found"
- Check AS installation path
- Verify AS is properly installed

#### **Prepare-Only Mode:**
**What Happens:**
- **NOTHING** - Step is skipped
- Process completes after Step 5
- Files are ready but AS is NOT launched

**Log Entry:**
```
Project prepared successfully (no launch)
```

---

## 🔄 Side-by-Side Comparison

### **Prepare-Only Mode** (`-prepare-only` flag)

| Step | Action | Result |
|------|--------|--------|
| 1 | ✅ Validate project structure | Folders checked |
| 2 | ✅ Clear Libraries directory | Old files removed |
| 3 | ✅ Copy version-specific libraries | New libraries installed |
| 4 | ✅ Update Physical.pkg | Physical config updated |
| 5 | ✅ Update OCB.apj | Project file updated |
| 6 | ❌ **NOT DONE** | AS **NOT** launched |

**Result:** Project is ready, but you must open it manually

**Use When:**
- Jenkins/CI builds
- Batch processing multiple projects
- Pre-configuration before manual work
- Remote server configuration
- Automated testing setup

---

### **Full Procedure Mode** (default, no `-prepare-only`)

| Step | Action | Result |
|------|--------|--------|
| 1 | ✅ Validate project structure | Folders checked |
| 2 | ✅ Clear Libraries directory | Old files removed |
| 3 | ✅ Copy version-specific libraries | New libraries installed |
| 4 | ✅ Update Physical.pkg | Physical config updated |
| 5 | ✅ Update OCB.apj | Project file updated |
| 6 | ✅ **LAUNCH AS** | AS **STARTS** with project |

**Result:** Project is ready AND Automation Studio is running

**Use When:**
- Normal daily work
- Interactive development
- Immediate project access needed
- GUI workflow

---

## 📊 Detailed File Changes

### **For AS 4.5 Configuration:**

#### **Files Modified:**
```
Logical/Libraries/                   ← ENTIRE CONTENTS REPLACED
  All files deleted and replaced with contents from Libraries_45/

Physical/Physical.pkg                ← FILE REPLACED
  Old file deleted
  New file copied from Physical_45.pkg
  
ProjectRoot/OCB.apj                  ← FILE REPLACED
  Old file deleted
  New file copied from OCB_as45.apj
```

#### **Files NOT Modified (Kept as Templates):**
```
Logical/Libraries_45/                ← UNCHANGED (source template)
Logical/Libraries_6/                 ← UNCHANGED (other version)
Physical/Physical_45.pkg             ← UNCHANGED (source template)
Physical/Physical_6.pkg              ← UNCHANGED (other version)
ProjectRoot/OCB_as45.apj             ← UNCHANGED (source template)
ProjectRoot/OCB_as6.apj              ← UNCHANGED (other version)
```

### **For AS 6 Configuration:**

#### **Files Modified:**
```
Logical/Libraries/                   ← ENTIRE CONTENTS REPLACED
  All files deleted and replaced with contents from Libraries_6/

Physical/Physical.pkg                ← FILE REPLACED
  Old file deleted
  New file copied from Physical_6.pkg
  
ProjectRoot/OCB.apj                  ← FILE REPLACED
  Old file deleted
  New file copied from OCB_as6.apj
```

#### **Files NOT Modified:**
```
Logical/Libraries_45/                ← UNCHANGED (other version)
Logical/Libraries_6/                 ← UNCHANGED (source template)
Physical/Physical_45.pkg             ← UNCHANGED (other version)
Physical/Physical_6.pkg              ← UNCHANGED (source template)
ProjectRoot/OCB_as45.apj             ← UNCHANGED (other version)
ProjectRoot/OCB_as6.apj              ← UNCHANGED (source template)
```

---

## 🎯 Visual Flowchart

### **Prepare-Only Process:**

```
START
  ↓
[Step 1] Validate Structure
  ↓
  ✓ Logical & Physical exist?
  ↓
[Step 2] Clear Libraries
  ↓
  Delete all files in Logical/Libraries/
  ↓
[Step 3] Copy Libraries
  ↓
  AS 4.5 selected? → Copy Libraries_45/ to Libraries/
  AS 6 selected?   → Copy Libraries_6/ to Libraries/
  ↓
[Step 4] Update Physical.pkg
  ↓
  AS 4.5 selected? → Copy Physical_45.pkg to Physical.pkg
  AS 6 selected?   → Copy Physical_6.pkg to Physical.pkg
  ↓
[Step 5] Update OCB.apj
  ↓
  AS 4.5 selected? → Copy OCB_as45.apj to OCB.apj
  AS 6 selected?   → Copy OCB_as6.apj to OCB.apj
  ↓
COMPLETE - Project Ready
(You can now manually open OCB.apj)
```

### **Full Procedure Process:**

```
START
  ↓
[Steps 1-5] Same as Prepare-Only
  (Validate, Clear, Copy Libraries, Update Physical.pkg, Update OCB.apj)
  ↓
[Step 6] Launch Automation Studio
  ↓
  Execute: AutomationStudio.exe "ProjectPath\OCB.apj"
  ↓
  AS Opens with Your Project
  ↓
COMPLETE - AS Running
(You can now work in Automation Studio)
```

---

## 🔄 Real Example with Your Project

### **Example: Configuring AS45 Project for AS 4.5**

**Command:**
```bash
python main.py -project-path "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45" -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" -as-version 45 -prepare-only
```

**Detailed Execution:**

#### **Step 1: Validate**
```
Checking: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45
  ✓ Logical folder exists
  ✓ Physical folder exists
  ✓ Structure valid
```

#### **Step 2: Clear**
```
Clearing: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\Logical\Libraries
  Deleted: Libraries\OldFile1.fun
  Deleted: Libraries\OldFile2.typ
  Deleted: Libraries\Subfolder\OldFile3.xml
  ... (all files removed)
  ✓ Libraries directory empty
```

#### **Step 3: Copy Libraries**
```
Source: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\Logical\Libraries_45
Target: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\Logical\Libraries

Copying:
  Libraries_45\Config.xml           → Libraries\Config.xml
  Libraries_45\AsArSdm.fun          → Libraries\AsArSdm.fun
  Libraries_45\Standard.fun         → Libraries\Standard.fun
  Libraries_45\Subfolder\File.typ   → Libraries\Subfolder\File.typ
  ... (all files and folders)
  
  ✓ Copied 47 files
  ✓ Created 8 directories
```

#### **Step 4: Update Physical.pkg**
```
Target: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\Physical\Physical.pkg
Source: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\Physical\Physical_45.pkg

Actions:
  1. Delete existing: Physical\Physical.pkg
  2. Copy: Physical_45.pkg → Physical.pkg
  
  ✓ Physical.pkg updated for AS 4.5
```

#### **Step 5: Update OCB.apj**
```
Target: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\OCB.apj
Source: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\OCB_as45.apj

Actions:
  1. Delete existing: OCB.apj
  2. Copy: OCB_as45.apj → OCB.apj
  
  ✓ Project file updated for AS 4.5
```

#### **Step 6: Launch (Prepare-Only = NO, Full = YES)**

**Prepare-Only Mode:**
```
  ⏸️ SKIPPED - AS NOT launched
  ✓ Project preparation complete
  
  You can now:
    - Double-click: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\OCB.apj
    - Or run AS manually
```

**Full Procedure Mode:**
```
  🚀 Launching AS...
  
  Execute:
    "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
    "C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\OCB.apj"
  
  ✓ Automation Studio 4.5 launched with project
  (AS window opens on your screen)
```

---

## 🎯 Key Differences Summary

### **Prepare-Only Mode:**
- ✅ Does Steps 1-5 (all file operations)
- ❌ Skips Step 6 (no AS launch)
- ⏱️ Faster (no waiting for AS to start)
- 🤖 Perfect for automation (Jenkins, scripts)
- 🔇 Can run silently in background
- 💻 No GUI interaction needed
- 🏃 Script completes and exits quickly

### **Full Procedure Mode:**
- ✅ Does ALL Steps 1-6 (file operations + launch)
- ✅ Includes Step 6 (launches AS)
- ⏱️ Slower (waits for AS to load)
- 👤 For interactive work
- 🖥️ Opens AS window on screen
- ⏸️ Process waits while AS is running

---

## 📝 What Files Are Affected

### **Always Modified (Both Modes):**
```
✏️ Logical/Libraries/           (entire contents replaced)
✏️ Physical/Physical.pkg        (file replaced)
✏️ ProjectRoot/OCB.apj          (file replaced)
```

### **Never Modified (Always Preserved):**
```
🔒 Logical/Libraries_45/        (AS 4.5 source - never touched)
🔒 Logical/Libraries_6/         (AS 6 source - never touched)
🔒 Physical/Physical_45.pkg     (AS 4.5 source - never touched)
🔒 Physical/Physical_6.pkg      (AS 6 source - never touched)
🔒 ProjectRoot/OCB_as45.apj     (AS 4.5 source - never touched)
🔒 ProjectRoot/OCB_as6.apj      (AS 6 source - never touched)
```

### **Important:**
The version-specific files (with `_45` or `_6` suffixes) are **NEVER modified** by the Selector. They are your **source templates** and are always preserved.

---

## 🔍 Logging and Verification

### **Console Output (Verbose Mode):**
```
Preparing project: AS45
Using AS: Automation Studio 4.5
Project path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45

Step 1: Validating project structure... ✓
Step 2: Clearing Libraries directory... ✓
Step 3: Copying version-specific libraries... ✓
  - Copied 47 files from Libraries_45
Step 4: Updating Physical.pkg file... ✓
  - Updated from Physical_45.pkg
Step 5: Updating project file... ✓
  - Updated from OCB_as45.apj

✓ Project prepared successfully for Automation Studio 4.5
  Files configured but Automation Studio NOT launched
  You can now manually open: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\AS45\OCB.apj
```

### **Log Files:**
All operations are logged to:
- `%USERPROFILE%\.automation_selector\logs\application.log`
- `%USERPROFILE%\.automation_selector\logs\session_YYYYMMDD_HHMMSS.log`

**Log Contents:**
```
2025-10-23 10:45:30 - Project operation: Libraries directory cleared
2025-10-23 10:45:30 - File operation: Directory copied - Source: ...\Libraries_45 - Target: ...\Libraries
2025-10-23 10:45:30 - File operation: File copied - Source: ...\Physical_45.pkg - Target: ...\Physical.pkg
2025-10-23 10:45:30 - File operation: File copied - Source: ...\OCB_as45.apj - Target: ...\OCB.apj
2025-10-23 10:45:30 - Project operation: Project prepared successfully (no launch)
```

---

## ⚡ Performance

### **Typical Execution Time:**

**Prepare-Only:**
- **Step 1-2**: < 1 second
- **Step 3**: 2-10 seconds (depends on library size)
- **Step 4-5**: < 1 second
- **Total**: ~5-15 seconds for average project

**Full Procedure:**
- **Steps 1-5**: Same as above (~5-15 seconds)
- **Step 6**: 10-30 seconds (AS startup time)
- **Total**: ~15-45 seconds until AS is ready

---

## 🎯 Conclusion

### **Prepare-Only = File Configuration Only**
- Does everything EXCEPT launch AS
- Perfect for automation
- Fast and scriptable
- Exit code 0 = files ready

### **Full Procedure = File Configuration + AS Launch**
- Does everything INCLUDING launch AS
- Perfect for interactive work
- Slower but convenient
- Exit code 0 = AS is running

### **The Choice:**

**Use Prepare-Only** (`-prepare-only`) when:
- Running in Jenkins/CI
- Batch processing projects
- You'll open AS manually later
- No GUI/desktop available
- Speed is important

**Use Full Procedure** (default) when:
- Working interactively
- Want AS to open automatically
- Using the GUI application
- Normal daily workflow

---

**Created by Vitaly Grosman - Indigo R&D Division**
