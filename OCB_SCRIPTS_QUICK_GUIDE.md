# OCB Project - Quick Start Guide
**Version 1.3.0 - Smart Project Conversion**

> 📥 **Download Automation Studio Selector v1.3.0:**  
> [AutomationStudioSelector_Setup_v1.3.0.exe](https://hp-my.sharepoint.com/:u:/p/vitaly_grosman/EaOKnHUZ1tlKjZGlEk23kRkBwOyI8lmW6uF4e4jWWDVJzg?e=og2YzG)

---

## 🚀 The Fastest Way to Convert Your Project

Your **OCB** project now includes ready-to-use scripts that make converting between AS versions incredibly simple!

---

## 📋 Why OCB Supports Both AS4.5 and AS6

**Background:**
- AS 4.5 is moving toward End of Life (EOL)
- Main configurations transitioning to AS6: **Hila_MR, Sufa (unified), Ayala**
- Many configurations staying on AS4.5: **Arad ECO, Stacker/Jigs/TBs, Eilat MR2, Shani, Barak, Tamar**

**The Challenge:**
- Some PLCs need AS6 (Hila_MR, Sufa, Ayala)
- Others must stay on AS4.5 (not supported by AS6)
- Maintaining two separate OCBs creates excessive overhead

**The Solution:**
- **One unified OCB** that works with both AS versions
- **Automation Studio Selector** handles the switching automatically
- These scripts make it as simple as double-clicking!

---

## 📁 What's in Your Project

```
OCB/
├── scripts/
│   ├── prepare45.bat    ← Double-click for AS 4.5
│   └── prepare6.bat     ← Double-click for AS 6
├── Logical/
│   ├── Libraries/       (managed automatically)
│   ├── Libraries_45/    (AS 4.5 source)
│   └── Libraries_6/     (AS 6 source)
├── Physical/
│   ├── Physical.pkg     (managed automatically)
│   ├── Physical_45.pkg  (AS 4.5 source)
│   └── Physical_6.pkg   (AS 6 source)
├── OCB.apj             (managed automatically)
├── OCB_as45.apj        (AS 4.5 source)
└── OCB_as6.apj         (AS 6 source)
```

---

## 🎯 How to Use (3 Simple Steps!)

### For AS 4.5:

1. **Navigate** to `OCB\scripts\` directory
2. **Double-click** `prepare45.bat`
3. **Wait** for "Project ready for AS 4.5!" message

### For AS 6:

1. **Navigate** to `OCB\scripts\` directory
2. **Double-click** `prepare6.bat`
3. **Wait** for "Project ready for AS 6!" message

**That's it!** Your project is now converted and ready to open in Automation Studio.

---

## ✨ What Happens Automatically

When you double-click a script:

1. ✅ **Auto-detects project path** - No configuration needed!
2. ✅ **Clears Libraries directory** - Removes old version files
3. ✅ **Copies correct libraries** - From Libraries_45 or Libraries_6
4. ✅ **Updates Physical.pkg** - From Physical_45.pkg or Physical_6.pkg
5. ✅ **Updates OCB.apj** - From OCB_as45.apj or OCB_as6.apj
6. ✅ **Shows success message** - Confirms project is ready

---

## 💡 Example Workflow

### Switching from AS 6 to AS 4.5:

1. Close Automation Studio (if open)
2. Go to `C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB\scripts\`
3. Double-click `prepare45.bat`
4. See output:
   ```
   ========================================
    Configuring AS45 Project
   ========================================

   Default path not found or not set, attempting auto-detection...
   Current directory: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB\scripts\
   Auto-detected project path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB

   Configuring AS45 project for AS 4.5...
   Project path: C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB

   Starting project setup...
   [1/5] Validating project structure...
   [2/5] Clearing Libraries directory...
   [3/5] Copying version-specific libraries...
   [4/5] Updating Physical.pkg file...
   [5/5] Updating project file...

   ========================================
     Project ready for AS 4.5
   ========================================

   Files updated:
     - Libraries copied from Libraries_45
     - Physical.pkg from Physical_45.pkg
     - Project .apj from _as45.apj

   Project ready at:
     C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB
   ```

5. Open your project in AS 4.5!

---

## 🎨 Benefits

### For You:
- **No typing** - Just double-click
- **No paths to configure** - Auto-detected
- **No mistakes** - Automated process
- **Fast** - Takes seconds

### For Your Team:
- **Same scripts everywhere** - Scripts in Git with project
- **Works on any machine** - No configuration needed
- **Easy onboarding** - New team members just double-click
- **Consistent** - Everyone uses same process

### For CI/CD:
- **Same scripts in Jenkins** - Can be called from command line
- **No environment setup** - Just works
- **Reliable** - Tested and proven
- **Portable** - Works across build servers

---

## 🔧 Advanced: Command Line Usage

You can also call these scripts from command line or other scripts:

```batch
REM From any location
cd C:\Work\Indigo\CrossPlatformAS\Br_MultiAS_OCB\OCB\scripts
call prepare45.bat

REM Or from the scripts directory
cd scripts
prepare6.bat

REM Check exit code
if %errorlevel% equ 0 (
    echo Success!
) else (
    echo Failed!
)
```

---

## ❓ Troubleshooting

### Error: "Cannot detect project path"

**Problem:** Script can't find `.apj` files in parent directory

**Solution:** 
- Make sure you're running the script from `OCB\scripts\` directory
- Verify that `OCB.apj` file exists in the parent directory
- Check that the project structure is correct

### Error: "Source libraries directory not found"

**Problem:** Missing `Libraries_45` or `Libraries_6` directory

**Solution:**
- Verify `Logical\Libraries_45\` exists (for AS 4.5)
- Verify `Logical\Libraries_6\` exists (for AS 6)
- Check that these directories contain the library files

### Script shows old path

**Problem:** Default path is hardcoded in script

**Solution:**
- Either: Update the `DEFAULT_PROJECT_PATH` variable in the script
- Or: Comment it out with `REM` to force auto-detection
- Auto-detection will work when run from `\scripts` directory

---

## 📋 Quick Reference

| Task | Script | Location |
|------|--------|----------|
| Convert to AS 4.5 | `prepare45.bat` | `OCB\scripts\` |
| Convert to AS 6 | `prepare6.bat` | `OCB\scripts\` |
| Check if it worked | Look for success message | Console output |
| Use in Jenkins | Call from command line | Works anywhere |

---

## 🎓 What's New in v1.3.0?

1. **Smart Path Detection** - Scripts auto-detect project location
2. **No Studio Path Needed** - Prepare-only mode doesn't need AS path
3. **Simplified Scripts** - Just 3 parameters instead of 5
4. **Portable** - Scripts work on any machine without configuration

**Before v1.3.0:**
```batch
python main.py -project-path "C:\OCB" -studio-path "C:\AS45\exe" -as-version 45 -prepare-only
```

**Now (v1.3.0):**
```batch
python main.py -project-path "C:\OCB" -as-version 45 -prepare-only
```

And when in `\scripts` directory:
```batch
python main.py -project-path "%~dp0\.." -as-version 45 -prepare-only
```
*(Auto-detects parent directory!)*

---

## 🎉 Summary

**The new workflow is:**
1. Double-click `prepare45.bat` or `prepare6.bat`
2. Wait for success message
3. Done!

No configuration, no typing, no mistakes. Just works! 🚀

---

**Created by:** Vitaly Grosman  
**Organization:** Indigo R&D Division  
**Version:** 1.3.0  
**© 2025**

---

**For more information, see:**
- `MASTER_TUTORIAL.md` - Complete user guide
- `VERSION_1.3.0_RELEASE_NOTES.md` - What's new in v1.3.0
- `test45.bat` and `test6.bat` - Example scripts with comments

