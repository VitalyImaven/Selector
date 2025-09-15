# Automation Studio Selector

A professional Python application for managing multiple Automation Studio installations and seamlessly switching between project configurations.

## Features

- **Multi-Version Support**: Supports Automation Studio 4.5, 6, and easily extensible for future versions
- **Professional Architecture**: Clean separation between UI, business logic, and data models
- **Modern UI**: Beautiful PyQt6 interface with modern styling
- **Automatic File Management**: Handles library copying and Physical.pkg file updates automatically
- **Session Logging**: Comprehensive logging of all operations with timestamps
- **Error Handling**: Robust error handling with user-friendly messages
- **Configuration Persistence**: Remembers your settings and last selected studio

## Project Structure

```
Selector/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
└── src/
    ├── config/
    │   └── settings.py             # Configuration management
    ├── models/
    │   └── automation_studio.py    # Data models
    ├── services/
    │   └── project_service.py      # Business logic
    ├── ui/
    │   ├── main_window.py          # Main application window
    │   ├── setup_dialog.py         # Initial setup dialog
    │   └── styles.py               # UI styling
    └── utils/
        └── logger.py               # Logging utilities
```

## Installation

1. **Clone or download** this project to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## First-Time Setup

When you first run the application, you'll be prompted to configure:

1. **Automation Studio Installations**:
   - Add paths to your AS 4.5 and AS 6 executable files
   - You can add more versions later if needed

2. **Project Root Directory**:
   - Select the root directory of your project
   - This should contain the `Logical` and `Physical` folders

## Expected Project Structure

Your project should have the following structure:

```
YourProject/
├── Logical/
│   ├── Libraries/              # Will be managed automatically
│   ├── Libraries_45/           # Libraries for AS 4.5
│   └── Libraries_6/            # Libraries for AS 6
├── Physical/
│   ├── Physical.pkg            # Will be managed automatically
│   ├── Physical_45.pkg         # Physical config for AS 4.5
│   └── Physical_6.pkg          # Physical config for AS 6
├── OCB.apj                    # Main project file (managed automatically)
├── OCB_as45.apj               # AS 4.5 project template
└── OCB_as6.apj                # AS 6 project template
```

## How It Works

When you select an Automation Studio version and click "Open Project":

1. **Validates** your project structure
2. **Clears** the `Logical/Libraries` directory
3. **Copies** the appropriate version-specific libraries (e.g., `Libraries_6` → `Libraries`)
4. **Updates** the `Physical.pkg` file with the version-specific configuration
5. **Updates** the main project file (`OCB.apj`) from the version-specific template
6. **Opens** the project with the selected Automation Studio executable

This approach ensures that anyone can double-click on `OCB.apj` and it will open with the correctly configured Automation Studio version.

## Configuration Files

The application stores its configuration in:
- **Windows**: `%USERPROFILE%\.automation_selector\config.json`
- **Linux/Mac**: `~/.automation_selector/config.json`

## Logging

Session logs are automatically created in:
- **Windows**: `%USERPROFILE%\.automation_selector\logs\`
- **Linux/Mac**: `~/.automation_selector/logs/`

Each session creates a new log file with timestamp, containing:
- Studio selection events
- File operations performed
- Errors encountered
- Project opening activities

## Adding New Automation Studio Versions

To add support for new versions:

1. Use the **File → Setup Studios** menu
2. Click **Add AS X** (where X is your version)
3. Browse to the executable file
4. Ensure your project has the corresponding:
   - `Libraries_X` directory
   - `Physical_X.pkg` file  
   - `OCB_asX.apj` project template file

## Troubleshooting

### Common Issues

1. **"Project structure validation failed"**
   - Ensure your project has `Logical` and `Physical` directories
   - Check that version-specific files exist (e.g., `Libraries_45`, `Physical_45.pkg`)

2. **"Automation Studio executable not found"**
   - Verify the executable path in File → Setup Studios
   - Ensure the executable file exists and is accessible

3. **"Source libraries directory not found"**
   - Check that `Libraries_45` or `Libraries_6` directories exist in your project
   - Verify the directory names match exactly

### Log Files

Check the session logs for detailed error information:
- Application logs: `~/.automation_selector/logs/application.log`
- Session logs: `~/.automation_selector/logs/session_YYYYMMDD_HHMMSS.log`

## Requirements

- **Python 3.8+**
- **PyQt6** - Modern GUI framework
- **Pydantic** - Data validation and settings management

## Future Enhancements

This application is designed for easy extension. Planned features include:
- Support for additional Automation Studio versions
- Project templates and wizards
- Backup and restore functionality
- Integration with version control systems
- Custom build configurations

## License

This project is provided as-is for internal use. Modify and extend as needed for your organization's requirements.
