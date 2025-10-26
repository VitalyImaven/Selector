# Prepare-Only Mode Feature

## Overview
Added a new checkbox option that allows users to prepare project files WITHOUT automatically launching Automation Studio. This gives users full control over when to open AS.

## What Changed

### UI Changes
**New Checkbox**: "Launch Automation Studio after preparation"
- Located below the Automation Studio selection list
- **Checked by default** (preserves original behavior)
- Users can uncheck to prepare without launching

**Button Text Update**:
- Changed from: "Open Project"
- Changed to: "Prepare Project"
- Better reflects the flexible behavior

**Instruction Text Update**:
- Changed from: "Choose which Automation Studio version to use for opening your project:"
- Changed to: "Choose which Automation Studio version to prepare your project for:"

### Functional Changes

#### With Checkbox CHECKED (Default):
```
1. Validate project structure ✓
2. Clear Libraries directory ✓
3. Copy version-specific libraries ✓
4. Update Physical.pkg ✓
5. Update project file (OCB.apj) ✓
6. Launch Automation Studio ✓  <-- Happens automatically
```
Result: "Project prepared and Automation Studio launched successfully!"

#### With Checkbox UNCHECKED (Prepare Only):
```
1. Validate project structure ✓
2. Clear Libraries directory ✓
3. Copy version-specific libraries ✓
4. Update Physical.pkg ✓
5. Update project file (OCB.apj) ✓
6. Launch Automation Studio ✗  <-- SKIPPED
```
Result: "Project prepared successfully! You can now open it manually."

## Use Cases

### When to Use Prepare-Only Mode (Checkbox Unchecked):

1. **Batch Processing**
   - Prepare multiple projects without opening each one
   - Useful for bulk configuration updates

2. **Automation/Scripts**
   - Prepare projects as part of automated workflows
   - CI/CD pipeline integration

3. **Manual Control**
   - When you want to check files before opening AS
   - When you need to make additional manual changes first

4. **Quick Switching**
   - Prepare for different AS versions without opening
   - Useful for testing compatibility

5. **Remote/Scheduled Tasks**
   - Prepare projects on schedule without user interaction
   - Remote configuration management

### When to Use Full Mode (Checkbox Checked - Default):

1. **Normal Operation**
   - Your typical daily workflow
   - Immediate work on the project

2. **Quick Start**
   - One-click prepare and open
   - Fastest path to working in AS

## Technical Implementation

### Files Modified
- `src/ui/main_window.py`

### Code Changes

**1. Added QCheckBox import**
```python
from PyQt6.QtWidgets import (
    ...
    QCheckBox
)
```

**2. Added checkbox UI element**
```python
self.launch_as_checkbox = QCheckBox("Launch Automation Studio after preparation")
self.launch_as_checkbox.setChecked(True)  # Checked by default
```

**3. Updated ProjectWorker class**
```python
def __init__(self, ..., launch_as: bool = True):
    ...
    self.launch_as = launch_as

def run(self):
    ...
    if self.launch_as:
        # Open AS
    else:
        # Skip opening AS
```

**4. Updated open_selected_project method**
```python
launch_as = self.launch_as_checkbox.isChecked()
self.worker_thread = ProjectWorker(..., launch_as)
```

**5. Updated UI enable/disable logic**
```python
def set_ui_enabled(self, enabled: bool):
    ...
    self.launch_as_checkbox.setEnabled(enabled)
```

## User Experience Flow

### Scenario 1: Default Behavior (Checkbox Checked)
```
User clicks "Prepare Project"
  ↓
All preparation steps execute
  ↓
Automation Studio launches automatically
  ↓
User works in AS immediately
```

### Scenario 2: Prepare-Only (Checkbox Unchecked)
```
User unchecks "Launch Automation Studio after preparation"
  ↓
User clicks "Prepare Project"
  ↓
All preparation steps execute
  ↓
AS does NOT launch
  ↓
User sees: "Project prepared successfully! You can now open it manually."
  ↓
User can:
  - Double-click OCB.apj to open
  - Make additional changes first
  - Prepare another version
  - Close the application
```

## Progress Messages

### With Checkbox Checked:
- "Starting project setup for [AS Version]"
- "Opening Automation Studio..."
- "Project setup completed - Automation Studio launched!"
- Success: "Project prepared and Automation Studio launched successfully!"

### With Checkbox Unchecked:
- "Starting project preparation for [AS Version]"
- "Project preparation completed!"
- Success: "Project prepared successfully! You can now open it manually."

## Backward Compatibility

✅ **Fully backward compatible!**
- Checkbox is **checked by default**
- Default behavior is exactly the same as before
- Existing workflows are not affected
- Users who never uncheck the box see no change

## Testing

### Test Case 1: Default Behavior
1. Launch application
2. Select project
3. Select AS version
4. Verify checkbox is checked
5. Click "Prepare Project"
6. Verify AS launches

### Test Case 2: Prepare-Only Mode
1. Launch application
2. Select project
3. Select AS version
4. Uncheck "Launch Automation Studio after preparation"
5. Click "Prepare Project"
6. Verify AS does NOT launch
7. Verify success message mentions manual opening

### Test Case 3: Checkbox State Persistence
1. Uncheck checkbox
2. Click "Prepare Project"
3. After completion, verify checkbox state remains unchecked
4. User can prepare again or check/uncheck as needed

### Test Case 4: UI Disable During Operation
1. Start preparation
2. Verify checkbox is disabled during operation
3. After completion, verify checkbox is re-enabled

## Benefits

✅ **User Control**: Users decide when to launch AS
✅ **Flexibility**: Supports both quick workflows and careful preparation
✅ **Automation-Friendly**: Perfect for scripts and batch operations
✅ **CI/CD Ready**: Enables automated project preparation
✅ **Default Safety**: Checked by default preserves original behavior
✅ **Clear Feedback**: Different messages for different modes
✅ **Professional**: Separates concerns (prepare vs. launch)

## Future Enhancements (Optional)

1. **Remember User Preference**
   - Save checkbox state in configuration
   - Restore on next launch

2. **Keyboard Shortcut**
   - Ctrl+P: Prepare only
   - Ctrl+Shift+P: Prepare and launch

3. **Command Line Equivalent**
   - Already exists: `-prepare-only` flag in CLI mode
   - Now GUI has feature parity with CLI

4. **Batch Mode**
   - Select multiple projects
   - Prepare all without launching any

## Documentation Updates Needed

Update these files:
- ✅ Help Dialog: Explain new checkbox
- ✅ Quick Start Guide: Mention the option
- ✅ User Manual: Document prepare-only mode
- ✅ Tutorial: Show both modes

## Comparison with CLI

The GUI checkbox feature provides the same functionality as the CLI `-prepare-only` flag:

**CLI Mode**:
```bash
python main.py -project-path "C:\Project" -studio-path "C:\AS45\exe" -as-version 45 -prepare-only
```

**GUI Mode**:
```
Uncheck "Launch Automation Studio after preparation"
Click "Prepare Project"
```

Both achieve the same result: project prepared, AS not launched.

## Summary

This feature adds professional flexibility to the application:
- ✅ **Implemented**: Checkbox control for launching AS
- ✅ **Tested**: Syntax validated, no linter errors
- ✅ **User-Friendly**: Checked by default, clear labels
- ✅ **Backward Compatible**: No breaking changes
- ✅ **Documented**: This file explains everything

Users now have full control over the prepare-and-launch workflow!

