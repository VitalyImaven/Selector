# PyInstaller Fix for Feedback Feature

## Problem
The "Send Feedback" feature works in development mode but fails in the packaged/installed version with the error:
```
Failed to open email client:
No module named 'urllib'
```

## Root Cause
In `automation_studio_selector_advanced.spec`, the `urllib` module was explicitly **EXCLUDED** from the build (line 52):
```python
EXCLUDED_MODULES = [
    ...
    'urllib',  # <-- This was causing the problem!
    'email',
]
```

This exclusion was likely done to reduce the executable size, but the new feedback feature requires `urllib.parse` for URL encoding.

## Solution Applied

### 1. Basic Spec File (`automation_studio_selector.spec`)
**Added to `hiddenimports`**:
```python
hiddenimports=[
    ...
    'urllib',
    'urllib.parse',
    'webbrowser',
    'platform',
],
```

### 2. Advanced Spec File (`automation_studio_selector_advanced.spec`)
**Removed from `EXCLUDED_MODULES`**:
```python
EXCLUDED_MODULES = [
    ...
    # 'urllib',  # REMOVED - needed for feedback feature
    # 'email',   # REMOVED - might be needed for future features
]
```

**Added to `hidden_imports`**:
```python
hidden_imports = [
    ...
    'urllib',
    'urllib.parse',
    'webbrowser',
    'platform',
]
```

## Modules Now Included
- `urllib` - For URL encoding
- `urllib.parse` - Specifically for the `quote()` function
- `webbrowser` - For opening the default email client
- `platform` - For collecting system information

## How to Rebuild the Executable

### Option 1: Using the Build Script (Recommended)
```batch
build_advanced.bat
```

### Option 2: Manual Build
```batch
pyinstaller automation_studio_selector_advanced.spec --clean
```

### Option 3: Basic Build (if not using advanced features)
```batch
pyinstaller automation_studio_selector.spec --clean
```

## Testing After Rebuild
1. Build the new executable
2. Run the installed version
3. Go to **Help → Send Feedback/Report Issue...**
4. Verify that your email client opens without errors
5. Check that all system information is included in the email

## Expected Result
After rebuilding, the feedback feature should work correctly in both:
- ✅ Development mode (`python main.py`)
- ✅ Installed/packaged version (`AutomationStudioSelector.exe`)

## Size Impact
Adding these modules may increase the executable size slightly:
- `urllib`: ~100-200 KB
- `webbrowser`: ~20-50 KB
- `platform`: ~10-20 KB

Total increase: approximately **130-270 KB** (negligible)

## Files Modified
1. `automation_studio_selector.spec` - Added hidden imports
2. `automation_studio_selector_advanced.spec` - Removed exclusions, added hidden imports

## Notes
- The `--clean` flag is recommended to ensure a fresh build
- The build will take a few minutes depending on your system
- The executable will be in `dist/AutomationStudioSelector/`
- You can create a new installer using `build_installer.bat` after rebuilding

## Verification Checklist
After rebuilding:
- [ ] Executable builds without errors
- [ ] Application starts correctly
- [ ] Help menu contains "Send Feedback/Report Issue..." option
- [ ] Clicking the menu item opens email client
- [ ] Email contains all system information
- [ ] No "urllib" error appears

## Future Considerations
If you need to reduce executable size in the future, DO NOT exclude:
- `urllib` - Required for feedback feature
- `webbrowser` - Required for feedback feature
- `platform` - Required for system information collection

