# Feedback Feature - Implementation Summary

## Overview
A new "Send Feedback/Report Issue" feature has been added to the Help menu. This allows users to easily send feedback, suggestions, or report issues via email with automatically collected system information.

## What Was Changed

### 1. Main Window UI (src/ui/main_window.py)
- **Added import**: `QApplication` to the PyQt6.QtWidgets imports
- **Added menu item**: "Send Feedback/Report Issue..." in the Help menu (line 252-255)
- **Added method**: `send_feedback()` (line 1107-1175)
- **Updated version**: About dialog now shows v1.1.0 (line 1182)

## How It Works

### User Experience
1. User clicks **Help → Send Feedback/Report Issue...**
2. The default email application opens automatically
3. Email is pre-populated with:
   - **To**: vitaly.grosman@hp.com
   - **Subject**: "Automation Studio Selector - Feedback/Issue Report"
   - **Body**: Includes a template for the user to write their feedback and automatically collected system information

### System Information Collected
The feature automatically collects and includes:
- **Application Version**: Current version (1.1.0)
- **Windows Version**: OS name and release (e.g., Windows 11)
- **Windows Build**: Detailed build number (e.g., 10.0.26100)
- **Machine**: Architecture (e.g., AMD64)
- **Processor**: CPU information
- **Python Version**: Python runtime version
- **Active Project**: Current project path (if selected)
- **Selected AS Version**: Currently selected Automation Studio version (if any)

### Email Template
```
Hello,

Please describe your feedback, suggestion, or issue below:
============================================================




============================================================

System Information (automatically collected):
------------------------------------------------------------
Application Version: 1.1.0
Windows Version: Windows 11
Windows Build: 10.0.26100
Machine: AMD64
Processor: Intel64 Family 6 Model...
Python Version: 3.x.x
Active Project: C:\Path\To\Project
Selected AS Version: Automation Studio 4.5
------------------------------------------------------------
```

## Error Handling
- If the email client fails to open, a dialog shows:
  - Error message
  - Fallback instruction to manually email vitaly.grosman@hp.com
- All actions are logged in the session log

## Testing
To test the feature:
1. Run the application
2. Go to **Help → Send Feedback/Report Issue...**
3. Your default email client should open with the pre-populated email
4. Check that all system information is correctly included

## Technical Details

### Dependencies Used
- `platform`: For collecting system information
- `webbrowser`: For opening the mailto link in the default email client
- `urllib.parse.quote`: For URL-encoding the email subject and body

### Code Location
- File: `src/ui/main_window.py`
- Method: `send_feedback()` (lines 1107-1175)
- Menu setup: Lines 252-255

## Benefits
- ✅ **Easy for users**: One-click access to send feedback
- ✅ **Comprehensive**: Automatically includes helpful system information
- ✅ **Non-intrusive**: Uses the user's default email application
- ✅ **Fallback**: Clear instructions if email client fails to open
- ✅ **Logged**: All actions are logged for debugging

## Future Enhancements (Optional)
- Add screenshot capture capability
- Include log file excerpts
- Add issue categorization (Bug/Feature Request/Question)
- Support for alternative feedback methods (web form, GitHub issues)

