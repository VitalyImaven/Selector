"""
Main window for the Automation Studio Selector application.
"""
import logging
from pathlib import Path
from typing import List, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QWidget, QMessageBox, QProgressBar,
    QTextEdit, QGroupBox, QStatusBar, QMenuBar, QMenu, QLineEdit, QFileDialog,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QFont, QIcon, QPixmap

from src.models.automation_studio import AutomationStudio
from src.config.settings import ConfigManager
from src.services.project_service import ProjectService, ProjectOperationError
from src.services.auto_sync_manager import AutoSyncManager
from src.utils.logger import SessionLogger
from src.ui.styles import MAIN_STYLE
from src.ui.setup_dialog import SetupDialog
from src.ui.sync_settings_dialog import SyncSettingsDialog


logger = logging.getLogger(__name__)


class ProjectWorker(QThread):
    """Worker thread for project operations."""
    
    progress_updated = pyqtSignal(str)
    operation_completed = pyqtSignal(bool, str)
    
    def __init__(self, project_service: ProjectService, project_root: Path, studio: AutomationStudio):
        """Initialize worker thread."""
        super().__init__()
        self.project_service = project_service
        self.project_root = project_root
        self.studio = studio
    
    def run(self):
        """Execute project setup in background thread."""
        try:
            self.progress_updated.emit("Starting project setup...")
            
            self.progress_updated.emit("Validating project structure...")
            self.project_service.validate_project_structure(self.project_root)
            
            self.progress_updated.emit("Clearing Libraries directory...")
            self.project_service.clear_libraries_directory(self.project_root)
            
            self.progress_updated.emit("Copying version-specific libraries...")
            self.project_service.copy_libraries_for_version(self.project_root, self.studio)
            
            self.progress_updated.emit("Updating Physical.pkg file...")
            self.project_service.update_physical_pkg(self.project_root, self.studio)
            
            self.progress_updated.emit("Updating project file...")
            self.project_service.update_project_file(self.project_root, self.studio)
            
            self.progress_updated.emit("Opening project...")
            self.project_service.open_project_file(self.project_root, self.studio)
            
            self.progress_updated.emit("Project setup completed successfully!")
            self.operation_completed.emit(True, "Project opened successfully!")
            
        except Exception as e:
            logger.error(f"Project setup failed: {e}")
            self.operation_completed.emit(False, str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        # Initialize components
        self.config_manager = ConfigManager()
        self.session_logger = SessionLogger()
        self.project_service = ProjectService(self.session_logger)
        self.auto_sync_manager = AutoSyncManager(self.session_logger)
        
        # UI components
        self.project_path_edit: Optional[QLineEdit] = None
        self.browse_project_btn: Optional[QPushButton] = None
        self.studio_list: Optional[QListWidget] = None
        self.select_button: Optional[QPushButton] = None
        self.progress_bar: Optional[QProgressBar] = None
        self.log_display: Optional[QTextEdit] = None
        self.status_bar: Optional[QStatusBar] = None
        
        # Data
        self.available_studios: List[AutomationStudio] = []
        self.project_root: Optional[Path] = None
        self.worker_thread: Optional[ProjectWorker] = None
        
        self.setup_ui()
        self.load_configuration()
        self.setup_auto_sync()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Automation Studio Selector")
        self.setMinimumSize(650, 650)
        self.resize(700, 900)
        
        # Apply styles
        self.setStyleSheet(MAIN_STYLE)
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Setup central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Logo and Title section
        logo_title_layout = QHBoxLayout()
        
        # Logo (image-based)
        logo = QLabel()
        try:
            # Get the correct path for the logo (works in both development and packaged app)
            import sys
            import os
            
            if getattr(sys, 'frozen', False):
                # Running in PyInstaller bundle
                base_path = sys._MEIPASS
            else:
                # Running in development
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            logo_path = os.path.join(base_path, 'assets', 'logo.png')
            
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                # Scale the logo to appropriate size
                scaled_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo.setPixmap(scaled_pixmap)
                logger.info(f"Logo loaded successfully from: {logo_path}")
            else:
                # Fallback to text if image fails to load
                logo.setText("🏭")
                logo.setStyleSheet("font-size: 48px; color: #3498db;")
                logger.warning(f"Logo image not found or invalid: {logo_path}")
        except Exception as e:
            # Fallback to text if image fails to load
            logo.setText("🏭")
            logo.setStyleSheet("font-size: 48px; color: #3498db;")
            logger.warning(f"Failed to load logo image: {e}")
        
        logo.setStyleSheet("""
            QLabel {
                padding: 10px;
                margin-right: 15px;
            }
        """)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_title_layout.addWidget(logo)
        
        # Title
        title = QLabel("Automation Studio Selector")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        logo_title_layout.addWidget(title)
        logo_title_layout.addStretch()
        
        # Add the logo and title layout to main layout
        layout.addLayout(logo_title_layout)
        
        # Project root selection group
        self.setup_project_root_group(layout)
        
        # Studio selection group
        self.setup_studio_selection_group(layout)
        
        # Progress section
        self.setup_progress_section(layout)
        
        # Log display
        self.setup_log_display(layout)
        
        # Status bar
        self.setup_status_bar()
        
    def setup_menu_bar(self):
        """Setup the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        setup_action = QAction("Setup Automation Studio Paths...", self)
        setup_action.triggered.connect(self.show_setup_dialog)
        file_menu.addAction(setup_action)
        
        change_project_action = QAction("Change Project Root...", self)
        change_project_action.triggered.connect(self.browse_project_root)
        file_menu.addAction(change_project_action)
        
        file_menu.addSeparator()
        
        # Manual sync action
        sync_now_action = QAction("Manual Sync Now", self)
        sync_now_action.triggered.connect(self.perform_manual_sync)
        file_menu.addAction(sync_now_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        
        # Sync submenu
        sync_menu = settings_menu.addMenu("Sync")
        
        sync_settings_action = QAction("Auto-Sync Settings...", self)
        sync_settings_action.triggered.connect(self.show_sync_settings)
        sync_menu.addAction(sync_settings_action)
        
        sync_status_action = QAction("View Sync Status", self)
        sync_status_action.triggered.connect(self.show_sync_status)
        sync_menu.addAction(sync_status_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_project_root_group(self, parent_layout):
        """Setup the project root selection group."""
        group = QGroupBox("Project Root Directory")
        layout = QVBoxLayout(group)
        
        # Instructions
        instructions = QLabel(
            "Select the root directory of your project (should contain Logical and Physical folders):"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Path selection layout
        path_layout = QHBoxLayout()
        
        self.project_path_edit = QLineEdit()
        self.project_path_edit.setReadOnly(True)
        self.project_path_edit.setPlaceholderText("No project root selected...")
        self.project_path_edit.textChanged.connect(self.on_project_path_changed)
        path_layout.addWidget(self.project_path_edit)
        
        self.browse_project_btn = QPushButton("Browse...")
        self.browse_project_btn.clicked.connect(self.browse_project_root)
        path_layout.addWidget(self.browse_project_btn)
        
        layout.addLayout(path_layout)
        parent_layout.addWidget(group)
    
    def setup_studio_selection_group(self, parent_layout):
        """Setup the studio selection group."""
        group = QGroupBox("Select Automation Studio")
        layout = QVBoxLayout(group)
        
        # Instructions
        instructions = QLabel(
            "Choose which Automation Studio version to use for opening your project:"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Studio list with proper sizing
        self.studio_list = QListWidget()
        self.studio_list.setMinimumHeight(140)
        self.studio_list.setMaximumHeight(180)
        self.studio_list.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.studio_list.itemSelectionChanged.connect(self.on_studio_selection_changed)
        self.studio_list.itemDoubleClicked.connect(self.open_selected_project)
        layout.addWidget(self.studio_list)
        
        # Add spacing between list and buttons
        layout.addSpacing(15)
        
        # Button layout with proper separation
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 0, 10, 10)  # Add margins all around
        
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.clicked.connect(self.refresh_studio_list)
        self.refresh_btn.setFixedHeight(40)  # Slightly larger buttons
        self.refresh_btn.setMinimumWidth(120)
        button_layout.addWidget(self.refresh_btn)
        
        button_layout.addStretch()
        
        self.select_button = QPushButton("Open Project")
        self.select_button.setObjectName("primary")
        self.select_button.clicked.connect(self.open_selected_project)
        self.select_button.setEnabled(False)
        self.select_button.setFixedHeight(40)  # Slightly larger buttons
        self.select_button.setMinimumWidth(140)
        button_layout.addWidget(self.select_button)
        
        layout.addLayout(button_layout)
        parent_layout.addWidget(group)
    
    def setup_progress_section(self, parent_layout):
        """Setup the progress section."""
        group = QGroupBox("Operation Progress")
        layout = QVBoxLayout(group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        parent_layout.addWidget(group)
    
    def setup_log_display(self, parent_layout):
        """Setup the log display section."""
        group = QGroupBox("Session Log")
        layout = QVBoxLayout(group)
        
        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(180)
        self.log_display.setMinimumHeight(140)
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)
        
        # Clear log button
        clear_btn = QPushButton("Clear Log")
        clear_btn.setObjectName("secondary")
        clear_btn.clicked.connect(self.clear_log)
        layout.addWidget(clear_btn)
        
        parent_layout.addWidget(group)
    
    def setup_status_bar(self):
        """Setup the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def load_configuration(self):
        """Load application configuration."""
        try:
            # Load studios
            self.available_studios = self.config_manager.get_automation_studios()
            
            # Load project root
            self.project_root = self.config_manager.get_project_root()
            
            if not self.available_studios or not self.project_root:
                # Show setup dialog if configuration is incomplete
                QTimer.singleShot(100, self.show_setup_dialog)
            else:
                self.refresh_studio_list()
                self.update_project_root_display()
                self.log_message(f"Loaded {len(self.available_studios)} studio configurations")
                self.log_message(f"Project root: {self.project_root}")
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.log_message(f"Error loading configuration: {e}")
            QTimer.singleShot(100, self.show_setup_dialog)
    
    def setup_auto_sync(self):
        """Setup auto-sync system."""
        try:
            # Set project root for auto-sync
            if self.project_root:
                self.auto_sync_manager.set_project_root(self.project_root)
            
            # Register all automation studios for process monitoring
            for studio in self.available_studios:
                self.auto_sync_manager.register_automation_studio(studio)
            
            # Connect signals
            self.auto_sync_manager.sync_completed.connect(self.on_sync_completed)
            self.auto_sync_manager.sync_error.connect(self.on_sync_error)
            
            self.log_message("Auto-sync system initialized")
            
        except Exception as e:
            logger.error(f"Error setting up auto-sync: {e}")
            self.log_message(f"Error setting up auto-sync: {e}")
    
    def show_setup_dialog(self):
        """Show the setup dialog."""
        try:
            dialog = SetupDialog(self.config_manager, self)
            dialog.studios_configured.connect(self.on_configuration_updated)
            dialog.exec()
        except Exception as e:
            logger.error(f"Error showing setup dialog: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to show setup dialog:\n{str(e)}"
            )
    
    def on_configuration_updated(self):
        """Handle configuration updates."""
        self.load_configuration()
        self.log_message("Configuration updated successfully")
    
    def update_project_root_display(self):
        """Update the project root display in the UI."""
        if self.project_root and self.project_path_edit:
            self.project_path_edit.setText(str(self.project_root))
        elif self.project_path_edit:
            self.project_path_edit.clear()
    
    def browse_project_root(self):
        """Browse for project root directory."""
        try:
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Select Project Root Directory")
            dialog.setFileMode(QFileDialog.FileMode.Directory)
            
            # Set initial directory to current project root if available
            if self.project_root and self.project_root.exists():
                dialog.setDirectory(str(self.project_root.parent))
            
            if dialog.exec() == QFileDialog.DialogCode.Accepted:
                selected_dirs = dialog.selectedFiles()
                if selected_dirs:
                    new_project_root = Path(selected_dirs[0])
                    
                    # Validate the selected directory
                    if self.validate_project_root(new_project_root):
                        self.project_root = new_project_root
                        self.project_path_edit.setText(str(new_project_root))
                        
                        # Save to configuration
                        if self.config_manager.set_project_root(new_project_root):
                            self.log_message(f"Project root updated: {new_project_root}")
                            self.status_bar.showMessage(f"Project root set to: {new_project_root.name}")
                        else:
                            self.log_message("Warning: Failed to save project root to configuration")
                    else:
                        QMessageBox.warning(
                            self,
                            "Invalid Project Directory",
                            "The selected directory does not appear to be a valid project root.\n\n"
                            "Please ensure the directory contains 'Logical' and 'Physical' subdirectories."
                        )
                        
        except Exception as e:
            logger.error(f"Error browsing project root: {e}")
            self.log_message(f"Error browsing project root: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to select project root:\n{str(e)}"
            )
    
    def validate_project_root(self, path: Path) -> bool:
        """Validate that the path is a valid project root."""
        try:
            if not path.exists() or not path.is_dir():
                return False
            
            # Check for required subdirectories
            logical_dir = path / "Logical"
            physical_dir = path / "Physical"
            
            return logical_dir.exists() and logical_dir.is_dir() and physical_dir.exists() and physical_dir.is_dir()
            
        except Exception as e:
            logger.error(f"Error validating project root: {e}")
            return False
    
    def on_project_path_changed(self):
        """Handle project path changes."""
        # Update the enabled state of the select button
        self.on_studio_selection_changed()
    
    def refresh_studio_list(self):
        """Refresh the studio list."""
        try:
            self.studio_list.clear()
            
            if not self.available_studios:
                item = QListWidgetItem("No Automation Studios configured")
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                self.studio_list.addItem(item)
                return
            
            # Add studios to list
            for studio in self.available_studios:
                item_text = f"{studio.display_name}\nPath: {studio.executable_path}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, studio)
                self.studio_list.addItem(item)
            
            # Select last used studio if available
            last_selected = self.config_manager.get_last_selected_studio()
            if last_selected:
                for i in range(self.studio_list.count()):
                    item = self.studio_list.item(i)
                    studio = item.data(Qt.ItemDataRole.UserRole)
                    if studio and studio.version.value == last_selected:
                        self.studio_list.setCurrentItem(item)
                        break
            
            self.status_bar.showMessage(f"Loaded {len(self.available_studios)} studio(s)")
            
        except Exception as e:
            logger.error(f"Error refreshing studio list: {e}")
            self.log_message(f"Error refreshing studio list: {e}")
    
    def on_studio_selection_changed(self):
        """Handle studio selection changes."""
        current_item = self.studio_list.currentItem()
        has_valid_selection = (
            current_item is not None and 
            current_item.data(Qt.ItemDataRole.UserRole) is not None
        )
        
        # Check if project root is set and valid
        has_valid_project_root = (
            self.project_root is not None and 
            self.project_root.exists() and
            self.validate_project_root(self.project_root)
        )
        
        self.select_button.setEnabled(has_valid_selection and has_valid_project_root)
    
    def open_selected_project(self):
        """Open project with selected automation studio."""
        try:
            current_item = self.studio_list.currentItem()
            if not current_item:
                return
            
            studio = current_item.data(Qt.ItemDataRole.UserRole)
            if not studio:
                return
            
            if not self.project_root:
                QMessageBox.warning(
                    self,
                    "Configuration Error",
                    "Project root is not configured. Please run setup first."
                )
                return
            
            # Disable UI during operation
            self.set_ui_enabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            
            # Save last selected studio
            self.config_manager.set_last_selected_studio(studio.version.value)
            
            # Start auto-sync session
            self.auto_sync_manager.start_session(studio)
            
            # Start worker thread
            self.worker_thread = ProjectWorker(self.project_service, self.project_root, studio)
            self.worker_thread.progress_updated.connect(self.on_progress_updated)
            self.worker_thread.operation_completed.connect(self.on_operation_completed)
            self.worker_thread.start()
            
            self.log_message(f"Starting project setup for {studio.display_name}")
            
        except Exception as e:
            logger.error(f"Error opening project: {e}")
            self.log_message(f"Error opening project: {e}")
            self.set_ui_enabled(True)
            self.progress_bar.setVisible(False)
    
    def on_progress_updated(self, message: str):
        """Handle progress updates."""
        self.status_bar.showMessage(message)
        self.log_message(message)
    
    def on_operation_completed(self, success: bool, message: str):
        """Handle operation completion."""
        try:
            self.set_ui_enabled(True)
            self.progress_bar.setVisible(False)
            
            if success:
                self.status_bar.showMessage("Operation completed successfully")
                self.log_message("✓ " + message)
            else:
                self.status_bar.showMessage("Operation failed")
                self.log_message("✗ " + message)
                
                # Show error message
                QMessageBox.critical(
                    self,
                    "Operation Failed",
                    f"Failed to open project:\n\n{message}"
                )
                
        except Exception as e:
            logger.error(f"Error handling operation completion: {e}")
    
    def set_ui_enabled(self, enabled: bool):
        """Enable or disable UI elements."""
        self.studio_list.setEnabled(enabled)
        self.browse_project_btn.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)
        
        # Only enable select button if all conditions are met
        if enabled:
            self.on_studio_selection_changed()
        else:
            self.select_button.setEnabled(False)
    
    def log_message(self, message: str):
        """Add message to log display."""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
            self.log_display.append(formatted_message)
            
            # Auto-scroll to bottom
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            
        except Exception as e:
            logger.error(f"Error logging message: {e}")
    
    def clear_log(self):
        """Clear the log display."""
        self.log_display.clear()
        self.log_message("Log cleared")
    
    def on_sync_completed(self, files_synced: int):
        """Handle auto-sync completion."""
        if files_synced > 0:
            self.log_message(f"✓ Auto-sync completed: {files_synced} files synchronized")
            self.status_bar.showMessage(f"Auto-sync: {files_synced} files synchronized", 3000)
    
    def on_sync_error(self, error_message: str):
        """Handle auto-sync error."""
        self.log_message(f"✗ Auto-sync error: {error_message}")
        self.status_bar.showMessage(f"Auto-sync error: {error_message}", 5000)
    
    def perform_manual_sync(self):
        """Perform manual synchronization."""
        try:
            files_synced = self.auto_sync_manager.perform_manual_sync()
            if files_synced > 0:
                self.log_message(f"✓ Manual sync completed: {files_synced} files synchronized")
                QMessageBox.information(
                    self,
                    "Manual Sync Complete",
                    f"Successfully synchronized {files_synced} files."
                )
            else:
                self.log_message("Manual sync: No changes detected")
                QMessageBox.information(
                    self,
                    "Manual Sync Complete", 
                    "No changes detected - all files are up to date."
                )
        except Exception as e:
            logger.error(f"Error in manual sync: {e}")
            self.log_message(f"✗ Manual sync error: {e}")
            QMessageBox.critical(
                self,
                "Manual Sync Error",
                f"Failed to perform manual sync:\n{str(e)}"
            )
    
    def show_sync_settings(self):
        """Show auto-sync settings dialog."""
        try:
            dialog = SyncSettingsDialog(self.auto_sync_manager.config_service, self)
            dialog.settings_changed.connect(self.on_sync_settings_changed)
            dialog.exec()
        except Exception as e:
            logger.error(f"Error showing sync settings dialog: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to show sync settings dialog:\n{str(e)}"
            )
    
    def show_sync_status(self):
        """Show sync status and statistics."""
        try:
            stats = self.auto_sync_manager.get_sync_statistics()
            
            # Format last sync time
            last_sync = "Never"
            if stats['last_sync_time']:
                import datetime
                last_sync = datetime.datetime.fromtimestamp(stats['last_sync_time']).strftime("%Y-%m-%d %H:%M:%S")
            
            # Format last check time
            last_check = "Never"
            if stats['last_check_time']:
                import datetime
                last_check = datetime.datetime.fromtimestamp(stats['last_check_time']).strftime("%Y-%m-%d %H:%M:%S")
            
            status_text = (
                f"Auto-Sync Status\n\n"
                f"Active Studio: {stats['active_studio'] or 'None'}\n"
                f"Files synced this session: {stats['files_synced_this_session']}\n"
                f"Total syncs performed: {stats['total_syncs_performed']}\n"
                f"Last sync: {last_sync}\n"
                f"Last check: {last_check}\n\n"
                f"Configuration:\n"
                f"Periodic sync: {'Enabled' if stats['periodic_sync_enabled'] else 'Disabled'}\n"
                f"Sync interval: {stats['sync_interval_minutes']} minutes\n\n"
                f"Config file location:\n"
                f"{self.auto_sync_manager.config_service.config_path}"
            )
            
            QMessageBox.information(
                self,
                "Auto-Sync Status",
                status_text
            )
            
        except Exception as e:
            logger.error(f"Error showing sync status: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to show sync status:\n{str(e)}"
            )
    
    def on_sync_settings_changed(self):
        """Handle sync settings changes."""
        try:
            # Reload settings in the auto-sync manager
            self.auto_sync_manager.reload_settings()
            self.log_message("Auto-sync settings updated")
        except Exception as e:
            logger.error(f"Error reloading sync settings: {e}")
            self.log_message(f"Error reloading sync settings: {e}")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Automation Studio Selector",
            "Automation Studio Selector v1.0\n\n"
            "A professional tool for managing multiple Automation Studio installations\n"
            "and seamlessly switching between project configurations.\n\n"
            "Features:\n"
            "• Support for multiple AS versions (4.5, 6, and more)\n"
            "• Automatic library and configuration management\n"
            "• Session logging and error handling\n"
            "• Modern, intuitive user interface\n\n"
            "Created by Vitaly Grosman\n\n"
            "Indigo R&D Division\n"
            "© 2025"
        )
    
    def closeEvent(self, event):
        """Handle application close event."""
        try:
            # Perform auto-sync on application close
            self.auto_sync_manager.sync_on_application_close()
            
            # Stop auto-sync manager
            self.auto_sync_manager.stop()
            
            # Stop worker thread if running
            if self.worker_thread and self.worker_thread.isRunning():
                self.worker_thread.terminate()
                self.worker_thread.wait(3000)  # Wait up to 3 seconds
            
            # Close session logger
            self.session_logger.close_session()
            
            logger.info("Application closing")
            event.accept()
            
        except Exception as e:
            logger.error(f"Error during application close: {e}")
            event.accept()
