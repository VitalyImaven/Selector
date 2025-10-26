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
    QSizePolicy, QInputDialog, QDialog, QApplication, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QFont, QIcon, QPixmap, QKeySequence, QShortcut

from src.models.automation_studio import AutomationStudio
from src.config.settings import ConfigManager
from src.services.project_service import ProjectService, ProjectOperationError
from src.services.auto_sync_manager import AutoSyncManager
from src.utils.logger import SessionLogger
from src.ui.styles import MAIN_STYLE
from src.ui.setup_dialog import SetupDialog
from src.ui.sync_settings_dialog import SyncSettingsDialog
from src.ui.help_dialog import HelpDialog
from src.ui.admin_panel import PasswordDialog, AdminPanel


logger = logging.getLogger(__name__)


class ProjectWorker(QThread):
    """Worker thread for project operations."""
    
    progress_updated = pyqtSignal(str)
    operation_completed = pyqtSignal(bool, str)
    
    def __init__(self, project_service: ProjectService, project_root: Path, studio: AutomationStudio, launch_as: bool = True):
        """Initialize worker thread."""
        super().__init__()
        self.project_service = project_service
        self.project_root = project_root
        self.studio = studio
        self.launch_as = launch_as
    
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
            
            if self.launch_as:
                self.progress_updated.emit("Opening Automation Studio...")
                self.project_service.open_project_file(self.project_root, self.studio)
                self.progress_updated.emit("Project setup completed - Automation Studio launched!")
                self.operation_completed.emit(True, "Project prepared and Automation Studio launched successfully!")
            else:
                self.progress_updated.emit("Project preparation completed!")
                self.operation_completed.emit(True, "Project prepared successfully! You can now open it manually.")
            
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
        self.project_list: Optional[QListWidget] = None
        self.add_project_btn: Optional[QPushButton] = None
        self.remove_project_btn: Optional[QPushButton] = None
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
        self.setup_secret_shortcuts()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Automation Studio Selector")
        self.setMinimumSize(800, 550)
        self.resize(800, 920)  # Start at optimal size
        
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
                # Running in development - go up to project root
                current_file = os.path.abspath(__file__)
                ui_dir = os.path.dirname(current_file)
                src_dir = os.path.dirname(ui_dir)
                base_path = os.path.dirname(src_dir)
            
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
        
        # How To submenu
        how_to_menu = help_menu.addMenu("How To")
        
        interactive_help_action = QAction("Interactive Help...", self)
        interactive_help_action.triggered.connect(self.show_interactive_help)
        how_to_menu.addAction(interactive_help_action)
        
        quick_start_action = QAction("Quick Start Guide", self)
        quick_start_action.triggered.connect(self.show_quick_start)
        how_to_menu.addAction(quick_start_action)
        
        help_menu.addSeparator()
        
        # Send Feedback action
        feedback_action = QAction("Send Feedback/Report Issue...", self)
        feedback_action.triggered.connect(self.send_feedback)
        help_menu.addAction(feedback_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_project_root_group(self, parent_layout):
        """Setup the project selection group with multiple projects support."""
        group = QGroupBox("Project Selection")
        layout = QVBoxLayout(group)
        
        # Instructions
        instructions = QLabel(
            "Select a project to work with. You can add multiple projects and switch between them:"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Project list
        self.project_list = QListWidget()
        self.project_list.setMinimumHeight(80)
        self.project_list.setMaximumHeight(130)
        self.project_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.project_list.itemSelectionChanged.connect(self.on_project_selection_changed)
        layout.addWidget(self.project_list)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.add_project_btn = QPushButton("Add Project...")
        self.add_project_btn.clicked.connect(self.add_new_project)
        button_layout.addWidget(self.add_project_btn)
        
        self.remove_project_btn = QPushButton("Remove Selected")
        self.remove_project_btn.setObjectName("danger")
        self.remove_project_btn.clicked.connect(self.remove_selected_project)
        self.remove_project_btn.setEnabled(False)
        button_layout.addWidget(self.remove_project_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        parent_layout.addWidget(group)
    
    def setup_studio_selection_group(self, parent_layout):
        """Setup the studio selection group."""
        group = QGroupBox("Select Automation Studio")
        layout = QVBoxLayout(group)
        
        # Instructions
        instructions = QLabel(
            "Choose which Automation Studio version to prepare your project for:"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Studio list with proper sizing
        self.studio_list = QListWidget()
        self.studio_list.setMinimumHeight(100)
        self.studio_list.setMaximumHeight(130)
        self.studio_list.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.studio_list.itemSelectionChanged.connect(self.on_studio_selection_changed)
        self.studio_list.itemDoubleClicked.connect(self.open_selected_project)
        layout.addWidget(self.studio_list)
        
        # Add spacing between list and buttons
        layout.addSpacing(15)
        
        # Button row
        button_row_layout = QHBoxLayout()
        button_row_layout.setContentsMargins(10, 10, 10, 5)
        
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.clicked.connect(self.refresh_studio_list)
        button_row_layout.addWidget(self.refresh_btn)
        
        button_row_layout.addStretch()
        
        self.select_button = QPushButton("Prepare Project")
        self.select_button.setObjectName("primary")
        self.select_button.clicked.connect(self.open_selected_project)
        self.select_button.setEnabled(False)
        button_row_layout.addWidget(self.select_button)
        
        layout.addLayout(button_row_layout)
        
        # Add checkbox below buttons
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setContentsMargins(10, 5, 10, 10)
        
        self.launch_as_checkbox = QCheckBox("Launch Automation Studio after preparation")
        self.launch_as_checkbox.setChecked(True)  # Checked by default
        self.launch_as_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        checkbox_layout.addWidget(self.launch_as_checkbox)
        checkbox_layout.addStretch()
        
        layout.addLayout(checkbox_layout)
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
        self.log_display.setMaximumHeight(130)
        self.log_display.setMinimumHeight(90)
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
            
            # Migrate old single project to new list format
            self.config_manager.migrate_single_project_to_list()
            
            # Load project paths
            self.load_project_list()
            
            if not self.available_studios:
                # Show setup dialog if no studios configured
                QTimer.singleShot(100, self.show_setup_dialog)
            else:
                self.refresh_studio_list()
                self.log_message(f"Loaded {len(self.available_studios)} studio configurations")
                
                # Set project root from last selected project
                last_project = self.config_manager.get_last_selected_project()
                if last_project and last_project.exists():
                    self.project_root = last_project
                    self.log_message(f"Active project: {self.project_root}")
                else:
                    self.project_root = None
                
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
    
    def setup_secret_shortcuts(self):
        """Setup secret keyboard shortcuts."""
        try:
            # Secret admin panel: Ctrl+Alt+Shift+P
            admin_shortcut = QShortcut(QKeySequence("Ctrl+Alt+Shift+P"), self)
            admin_shortcut.activated.connect(self.show_secret_admin_panel)
            logger.info("Secret shortcuts initialized")
        except Exception as e:
            logger.error(f"Error setting up secret shortcuts: {e}")
    
    def show_secret_admin_panel(self):
        """Show the secret admin panel (after password check)."""
        try:
            # Show password dialog first
            password_dialog = PasswordDialog(self)
            if password_dialog.exec() == QDialog.DialogCode.Accepted and password_dialog.password_correct:
                # Password correct - show admin panel
                logger.info("Admin panel accessed successfully")
                # Pass the valhalla player to admin panel so it can stop the music
                admin_panel = AdminPanel(self.config_manager, password_dialog.valhalla_player, self)
                admin_panel.config_cleared.connect(self.on_admin_config_cleared)
                admin_panel.exec()
            
        except Exception as e:
            logger.error(f"Error showing admin panel: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to show admin panel:\n{str(e)}"
            )
    
    def on_admin_config_cleared(self):
        """Handle configuration cleanup from admin panel."""
        try:
            self.log_message("Configuration cleared via admin panel - reloading...")
            
            # Reload configuration
            self.load_configuration()
            
            QMessageBox.information(
                self,
                "Configuration Cleared",
                "Configuration has been cleared.\n\n"
                "The application will now reload with default settings.\n"
                "You may need to reconfigure your Automation Studios and projects."
            )
            
        except Exception as e:
            logger.error(f"Error handling admin config clear: {e}")
            self.log_message(f"Error handling admin config clear: {e}")
    
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
    
    def load_project_list(self):
        """Load and display the list of configured projects."""
        try:
            self.project_list.clear()
            project_paths = self.config_manager.get_project_paths()
            
            if not project_paths:
                item = QListWidgetItem("No projects configured - click 'Add Project...' to add one")
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                self.project_list.addItem(item)
                return
            
            # Add projects to list
            for project_data in project_paths:
                project_name = project_data.get('name', 'Unknown Project')
                project_path = project_data.get('path', '')
                project_desc = project_data.get('description', '')
                
                # Create compact display text on one line
                if project_desc:
                    display_text = f"{project_name} - {project_path} ({project_desc})"
                else:
                    display_text = f"{project_name} - {project_path}"
                
                item = QListWidgetItem(display_text)
                item.setData(Qt.ItemDataRole.UserRole, project_data)
                self.project_list.addItem(item)
            
            # Select last used project
            last_project_path = self.config_manager.get_last_selected_project()
            if last_project_path:
                for i in range(self.project_list.count()):
                    item = self.project_list.item(i)
                    project_data = item.data(Qt.ItemDataRole.UserRole)
                    if project_data and project_data.get('path') == str(last_project_path):
                        self.project_list.setCurrentItem(item)
                        break
            
        except Exception as e:
            logger.error(f"Error loading project list: {e}")
            self.log_message(f"Error loading project list: {e}")
    
    def on_project_selection_changed(self):
        """Handle project selection changes."""
        try:
            current_item = self.project_list.currentItem()
            has_selection = current_item is not None
            
            # Enable/disable remove button
            project_data = None
            if has_selection:
                project_data = current_item.data(Qt.ItemDataRole.UserRole)
            
            self.remove_project_btn.setEnabled(has_selection and project_data is not None)
            
            # Update active project root
            if project_data:
                project_path = Path(project_data['path'])
                if project_path.exists() and self.validate_project_root(project_path):
                    self.project_root = project_path
                    self.config_manager.set_last_selected_project(project_path)
                    self.log_message(f"Selected project: {project_data['name']}")
                else:
                    self.project_root = None
                    self.log_message(f"Warning: Selected project path is invalid: {project_path}")
            else:
                self.project_root = None
            
            # Update studio selection state
            self.on_studio_selection_changed()
            
        except Exception as e:
            logger.error(f"Error handling project selection: {e}")
            self.log_message(f"Error handling project selection: {e}")
    
    def add_new_project(self):
        """Add a new project to the list."""
        try:
            # Get project directory
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Select Project Directory")
            dialog.setFileMode(QFileDialog.FileMode.Directory)
            
            if dialog.exec() == QFileDialog.DialogCode.Accepted:
                selected_dirs = dialog.selectedFiles()
                if selected_dirs:
                    project_path = Path(selected_dirs[0])
                    
                    # Validate project structure
                    if not self.validate_project_root(project_path):
                        QMessageBox.warning(
                            self,
                            "Invalid Project Directory",
                            "The selected directory does not appear to be a valid project root.\n\n"
                            "Please ensure the directory contains 'Logical' and 'Physical' subdirectories."
                        )
                        return
                    
                    # Get project name from user
                    from PyQt6.QtWidgets import QInputDialog
                    project_name = project_path.name  # Default to folder name
                    
                    name, ok = QInputDialog.getText(
                        self,
                        "Project Name",
                        "Enter a name for this project:",
                        text=project_name
                    )
                    
                    if ok and name.strip():
                        # Get optional description
                        description, ok = QInputDialog.getText(
                            self,
                            "Project Description",
                            "Enter a description (optional):",
                            text=""
                        )
                        
                        if not ok:
                            description = ""
                        
                        # Add to configuration
                        if self.config_manager.add_project_path(name.strip(), project_path, description.strip()):
                            self.load_project_list()
                            self.log_message(f"Added project: {name.strip()}")
                            
                            # Select the newly added project
                            for i in range(self.project_list.count()):
                                item = self.project_list.item(i)
                                project_data = item.data(Qt.ItemDataRole.UserRole)
                                if project_data and project_data.get('path') == str(project_path):
                                    self.project_list.setCurrentItem(item)
                                    break
                        else:
                            QMessageBox.warning(
                                self,
                                "Add Project Failed",
                                "Failed to add project to configuration.\n\n"
                                "The project may already exist in the list."
                            )
                            
        except Exception as e:
            logger.error(f"Error adding new project: {e}")
            self.log_message(f"Error adding new project: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to add new project:\n{str(e)}"
            )
    
    def remove_selected_project(self):
        """Remove the selected project from the list."""
        try:
            current_item = self.project_list.currentItem()
            if not current_item:
                return
            
            project_data = current_item.data(Qt.ItemDataRole.UserRole)
            if not project_data:
                return
            
            project_name = project_data.get('name', 'Unknown Project')
            project_path = Path(project_data.get('path', ''))
            
            # Confirm removal
            reply = QMessageBox.question(
                self,
                "Remove Project",
                f"Are you sure you want to remove this project from the list?\n\n"
                f"Project: {project_name}\n"
                f"Path: {project_path}\n\n"
                f"Note: This only removes it from the selector list.\n"
                f"Your actual project files will not be deleted.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if self.config_manager.remove_project_path(project_path):
                    self.load_project_list()
                    self.project_root = None  # Clear current selection
                    self.log_message(f"Removed project: {project_name}")
                    self.on_studio_selection_changed()  # Update button states
                else:
                    QMessageBox.warning(
                        self,
                        "Remove Failed",
                        "Failed to remove project from configuration."
                    )
                    
        except Exception as e:
            logger.error(f"Error removing project: {e}")
            self.log_message(f"Error removing project: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to remove project:\n{str(e)}"
            )
    
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
                # Show full text without truncation
                item_text = f"{studio.display_name} - {studio.executable_path}"
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
            
            # Get checkbox state
            launch_as = self.launch_as_checkbox.isChecked()
            
            # Disable UI during operation
            self.set_ui_enabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            
            # Save last selected studio
            self.config_manager.set_last_selected_studio(studio.version.value)
            
            # Start auto-sync session
            self.auto_sync_manager.start_session(studio)
            
            # Start worker thread with launch_as parameter
            self.worker_thread = ProjectWorker(self.project_service, self.project_root, studio, launch_as)
            self.worker_thread.progress_updated.connect(self.on_progress_updated)
            self.worker_thread.operation_completed.connect(self.on_operation_completed)
            self.worker_thread.start()
            
            action = "Starting project preparation" if not launch_as else "Starting project setup"
            self.log_message(f"{action} for {studio.display_name}")
            
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
        self.project_list.setEnabled(enabled)
        self.add_project_btn.setEnabled(enabled)
        self.remove_project_btn.setEnabled(enabled and self.project_list.currentItem() is not None)
        self.refresh_btn.setEnabled(enabled)
        self.launch_as_checkbox.setEnabled(enabled)
        
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
    
    def show_interactive_help(self):
        """Show the interactive help dialog."""
        try:
            help_dialog = HelpDialog(self)
            help_dialog.exec()
        except Exception as e:
            logger.error(f"Error showing interactive help: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to show interactive help:\n{str(e)}"
            )
    
    def show_quick_start(self):
        """Show quick start guide."""
        try:
            quick_start_text = """
            <h2>🚀 Quick Start Guide</h2>
            
            <h3>1. First-Time Setup</h3>
            <p>When you first open the application:</p>
            <ul>
                <li><strong>Add AS 4.5:</strong> Click "Add AS 4.5" and browse to your AutomationStudio.exe</li>
                <li><strong>Add AS 6:</strong> Click "Add AS 6" and browse to your AutomationStudio.exe</li>
                <li><strong>Set Project Root:</strong> Browse to your project folder (contains Logical & Physical)</li>
                <li><strong>Save:</strong> Click "Save & Continue"</li>
            </ul>
            
            <h3>2. Using the Application</h3>
            <ol>
                <li><strong>Select Version:</strong> Click on "Automation Studio 4.5" or "Automation Studio 6"</li>
                <li><strong>Open Project:</strong> Click the green "Open Project" button</li>
                <li><strong>Work Normally:</strong> Use Automation Studio as usual</li>
                <li><strong>Auto-Sync:</strong> Your changes are automatically saved when you close AS</li>
            </ol>
            
            <h3>3. Switching Versions</h3>
            <ul>
                <li><strong>Close AS</strong> (your work is auto-synced)</li>
                <li><strong>Select different version</strong> in the Selector</li>
                <li><strong>Click "Open Project"</strong> again</li>
                <li><strong>Your previous work is preserved!</strong></li>
            </ul>
            
            <h3>4. Key Benefits</h3>
            <ul>
                <li>✅ <strong>Never lose work</strong> when switching AS versions</li>
                <li>✅ <strong>One project</strong> works with multiple AS versions</li>
                <li>✅ <strong>Automatic sync</strong> every 5 minutes and when AS closes</li>
                <li>✅ <strong>Safe backups</strong> before any file operations</li>
            </ul>
            
            <div style="background-color: #e8f6f3; padding: 15px; border-left: 4px solid #16a085; margin: 15px 0;">
                <strong>💡 Need More Help?</strong><br>
                Use <strong>Help → How To → Interactive Help</strong> for detailed explanations of every feature.
            </div>
            """
            
            QMessageBox.information(
                self,
                "Quick Start Guide",
                quick_start_text
            )
            
        except Exception as e:
            logger.error(f"Error showing quick start guide: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to show quick start guide:\n{str(e)}"
            )
    
    def send_feedback(self):
        """Open user's email application to send feedback with system and application information."""
        try:
            import platform
            import webbrowser
            from urllib.parse import quote
            
            # Get application version
            app_version = QApplication.instance().applicationVersion()
            
            # Collect system information
            system_info = []
            system_info.append(f"Application Version: {app_version}")
            system_info.append(f"Windows Version: {platform.system()} {platform.release()}")
            system_info.append(f"Windows Build: {platform.version()}")
            system_info.append(f"Machine: {platform.machine()}")
            system_info.append(f"Processor: {platform.processor()}")
            system_info.append(f"Python Version: {platform.python_version()}")
            
            # Collect application configuration
            app_config = []
            app_config.append("")
            app_config.append("APPLICATION CONFIGURATION:")
            app_config.append("-" * 60)
            
            # Current active selections
            if self.project_root and self.project_root.exists():
                app_config.append(f"Active Project: {self.project_root}")
            else:
                app_config.append("Active Project: None")
            
            current_item = self.studio_list.currentItem()
            if current_item:
                studio = current_item.data(Qt.ItemDataRole.UserRole)
                if studio:
                    app_config.append(f"Selected AS Version: {studio.display_name} ({studio.version.value})")
            else:
                app_config.append("Selected AS Version: None")
            
            # Launch AS checkbox state
            launch_as_checked = self.launch_as_checkbox.isChecked()
            app_config.append(f"Launch AS after preparation: {'Yes' if launch_as_checked else 'No'}")
            
            # All configured projects
            app_config.append("")
            app_config.append("CONFIGURED PROJECTS:")
            project_paths = self.config_manager.get_project_paths()
            if project_paths:
                for i, project_data in enumerate(project_paths, 1):
                    name = project_data.get('name', 'Unknown')
                    path = project_data.get('path', 'Unknown')
                    desc = project_data.get('description', '')
                    app_config.append(f"  {i}. {name}")
                    app_config.append(f"     Path: {path}")
                    if desc:
                        app_config.append(f"     Description: {desc}")
            else:
                app_config.append("  No projects configured")
            
            # All configured Automation Studios
            app_config.append("")
            app_config.append("CONFIGURED AUTOMATION STUDIOS:")
            if self.available_studios:
                for i, studio in enumerate(self.available_studios, 1):
                    app_config.append(f"  {i}. {studio.display_name}")
                    app_config.append(f"     Version: {studio.version.value}")
                    app_config.append(f"     Path: {studio.executable_path}")
                    app_config.append(f"     Libraries Suffix: {studio.libraries_suffix}")
                    app_config.append(f"     Physical PKG Suffix: {studio.physical_pkg_suffix}")
                    app_config.append(f"     Project File Suffix: {studio.project_file_suffix}")
            else:
                app_config.append("  No Automation Studios configured")
            
            # Auto-sync configuration
            app_config.append("")
            app_config.append("AUTO-SYNC SETTINGS:")
            try:
                sync_settings = self.auto_sync_manager.config_service.load_settings()
                app_config.append(f"  Sync on AS close: {sync_settings.sync_on_as_close}")
                app_config.append(f"  Sync on app close: {sync_settings.sync_on_app_close}")
                app_config.append(f"  Periodic sync enabled: {sync_settings.periodic_sync_enabled}")
                app_config.append(f"  Sync interval: {sync_settings.sync_interval_minutes} minutes")
                app_config.append(f"  Create backups: {sync_settings.create_backups}")
                app_config.append(f"  Max backups: {sync_settings.max_backups}")
                app_config.append(f"  Log sync operations: {sync_settings.log_sync_operations}")
            except Exception as e:
                app_config.append(f"  Unable to load sync settings: {e}")
            
            # Sync statistics
            app_config.append("")
            app_config.append("AUTO-SYNC STATISTICS:")
            try:
                stats = self.auto_sync_manager.get_sync_statistics()
                app_config.append(f"  Active Studio: {stats.get('active_studio', 'None')}")
                app_config.append(f"  Files synced this session: {stats.get('files_synced_this_session', 0)}")
                app_config.append(f"  Total syncs performed: {stats.get('total_syncs_performed', 0)}")
                if stats.get('last_sync_time'):
                    import datetime
                    last_sync = datetime.datetime.fromtimestamp(stats['last_sync_time']).strftime("%Y-%m-%d %H:%M:%S")
                    app_config.append(f"  Last sync: {last_sync}")
                else:
                    app_config.append(f"  Last sync: Never")
            except Exception as e:
                app_config.append(f"  Unable to load sync statistics: {e}")
            
            # Configuration file location
            app_config.append("")
            app_config.append("CONFIGURATION FILES:")
            app_config.append(f"  Main config: {self.config_manager.config_path}")
            try:
                app_config.append(f"  Sync config: {self.auto_sync_manager.config_service.config_path}")
            except:
                pass
            
            # Create email subject
            subject = "Automation Studio Selector - Feedback/Issue Report"
            
            # Create email body
            body_lines = [
                "Hello,",
                "",
                "Please describe your feedback, suggestion, or issue below:",
                "=" * 60,
                "",
                "",
                "",
                "=" * 60,
                "",
                "SYSTEM & APPLICATION INFORMATION (automatically collected):",
                "=" * 60,
                "",
                "SYSTEM INFORMATION:",
                "-" * 60,
            ]
            body_lines.extend(system_info)
            body_lines.extend(app_config)
            body_lines.append("=" * 60)
            
            body = "\n".join(body_lines)
            
            # Create mailto link
            mailto_link = f"mailto:vitaly.grosman@hp.com?subject={quote(subject)}&body={quote(body)}"
            
            # Open in default email client
            webbrowser.open(mailto_link)
            
            self.log_message("Opening email client for feedback with full application configuration...")
            self.status_bar.showMessage("Email client opened for feedback", 3000)
            
        except Exception as e:
            logger.error(f"Error opening email client: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to open email client:\n{str(e)}\n\n"
                f"Please manually email vitaly.grosman@hp.com with your feedback."
            )
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Automation Studio Selector",
            "Automation Studio Selector v1.2.0\n\n"
            "A professional tool for managing multiple Automation Studio installations\n"
            "and seamlessly switching between project configurations.\n\n"
            "Features:\n"
            "• Support for multiple AS versions (4.5, 6, and more)\n"
            "• Automatic library and configuration management\n"
            "• Prepare-only mode for flexible workflows\n"
            "• Comprehensive feedback system\n"
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
