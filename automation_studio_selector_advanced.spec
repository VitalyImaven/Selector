# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# ========================================
# CONFIGURATION SECTION - MODIFY AS NEEDED
# ========================================

# Basic application info
APP_NAME = 'AutomationStudioSelector'
APP_VERSION = '1.0.0'
APP_AUTHOR = 'Vitaly Grosman - Indigo R&D Division'

# Build options
DEBUG_MODE = False          # Set to True for debugging
CONSOLE_MODE = False        # Set to True to show console window
UPX_COMPRESSION = True      # Set to False to disable UPX compression
OPTIMIZE_SIZE = True        # Set to False for faster builds
INCLUDE_MSVCRT = True       # Include Microsoft Visual C++ runtime

# Icon configuration (optional)
# ICON_FILE = 'assets/app_icon.ico'  # Uncomment and set path to .ico file
ICON_FILE = None

# Additional files to include
EXTRA_DATA_FILES = [
    ('MASTER_TUTORIAL.md', '.'),        # Include master tutorial
    ('MASTER_TUTORIAL_Confluence.html', '.'),  # Include HTML version
]

# Additional modules to include (if import detection fails)
EXTRA_HIDDEN_IMPORTS = [
    # Add any modules that PyInstaller misses
    # 'some_module',
]

# Modules/packages to exclude (reduces size)
EXCLUDED_MODULES = [
    'matplotlib',
    'numpy', 
    'pandas',
    'scipy',
    'PIL',
    'tkinter',
    'test',
    'unittest',
    'sqlite3',
    'ssl',
    'http',
    'urllib',
    'email',
]

# ========================================
# ADVANCED CONFIGURATION
# ========================================

# Get the project root directory
project_root = Path.cwd()

# Encryption (optional - set to None for no encryption)
block_cipher = None
# block_cipher = pyi_crypto.PyiBlockCipher(key='your-secret-key')

# Data files configuration
data_files = [
    ('assets/logo.png', 'assets'),
    ('assets/Star Wars- The Imperial March .mp3', 'assets'),
    ('assets/VALHALLA CALLING.mp4', 'assets'),
    ('auto_sync_config_example.xml', '.'),
] + EXTRA_DATA_FILES

# Hidden imports configuration
hidden_imports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.QtMultimedia',
    'psutil',
    'pydantic',
    'pydantic_settings',
    'xml.etree.ElementTree',
    'json',
    'pathlib',
    'datetime',
    'logging',
    'threading',
    'subprocess',
    'shutil',
    'time',
] + EXTRA_HIDDEN_IMPORTS

# ========================================
# BUILD CONFIGURATION
# ========================================

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=data_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDED_MODULES,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=not OPTIMIZE_SIZE,  # Archive for smaller size
)

# Remove duplicate files and optimize
if OPTIMIZE_SIZE:
    # Remove unnecessary files
    a.datas = [x for x in a.datas if not any(exclude in x[0].lower() for exclude in [
        'test', 'tests', '__pycache__', '.pyc', '.pyo', 'tcl', 'tk'
    ])]

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=DEBUG_MODE,
    bootloader_ignore_signals=False,
    strip=False,  # Disable strip to avoid Windows errors
    upx=UPX_COMPRESSION,
    console=CONSOLE_MODE,
    disable_windowed_traceback=not DEBUG_MODE,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_FILE,
    version='version_info.txt',
    # Additional EXE options
    uac_admin=False,         # Don't require admin to run
    uac_uiaccess=False,      # Don't require UI access
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,  # Disable strip to avoid Windows errors
    upx=UPX_COMPRESSION,
    upx_exclude=[
        # Exclude these files from UPX compression (can cause issues)
        'Qt6Core.dll',
        'Qt6Gui.dll', 
        'Qt6Widgets.dll',
        'python313.dll',
    ],
    name=APP_NAME,
)

# ========================================
# BUILD INFORMATION
# ========================================

print(f"""
========================================
BUILD CONFIGURATION SUMMARY
========================================
App Name: {APP_NAME}
Version: {APP_VERSION}
Author: {APP_AUTHOR}
Debug Mode: {DEBUG_MODE}
Console Mode: {CONSOLE_MODE}
UPX Compression: {UPX_COMPRESSION}
Optimize Size: {OPTIMIZE_SIZE}
Icon: {ICON_FILE or 'None'}
Extra Data Files: {len(EXTRA_DATA_FILES)}
Hidden Imports: {len(hidden_imports)}
Excluded Modules: {len(EXCLUDED_MODULES)}
========================================
""")

