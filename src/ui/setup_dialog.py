"""
Setup dialog for configuring Automation Studio installations.
"""
import logging
from pathlib import Path
from typing import Optional, List
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QListWidget, QListWidgetItem, QFileDialog, QMessageBox,
    QGroupBox, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from src.models.automation_studio import AutomationStudio, AutomationStudioVersion
from src.config.settings import ConfigManager
from src.ui.styles import MAIN_STYLE


logger = logging.getLogger(__name__)


class SetupDialog(QDialog):
    """Dialog for initial setup of Automation Studio installations."""
    
    studios_configured = pyqtSignal()
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        """Initialize setup dialog."""
        super().__init__(parent)
        self.config_manager = config_manager
        self.configured_studios: List[AutomationStudio] = []
        
        self.setup_ui()
        self.load_existing_studios()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Automation Studio Selector - Initial Setup")
        self.setModal(True)
        self.resize(600, 500)
        
        # Apply styles
        self.setStyleSheet(MAIN_STYLE)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Setup Automation Studio Installations")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Configure the paths to your Automation Studio executable files")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Studio configuration group
        self.setup_studio_group(layout)
        
        # Project root configuration group
        self.setup_project_group(layout)
        
        # Buttons
        self.setup_buttons(layout)
        
    def setup_studio_group(self, parent_layout):
        """Setup the studio configuration group."""
        group = QGroupBox("Automation Studio Installations")
        layout = QVBoxLayout(group)
        
        # Instructions
        instructions = QLabel(
            "Add your Automation Studio installations. You need at least one to continue."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Studio list
        self.studio_list = QListWidget()
        self.studio_list.setMinimumHeight(150)
        layout.addWidget(self.studio_list)
        
        # Studio buttons
        button_layout = QHBoxLayout()
        
        self.add_as45_btn = QPushButton("Add AS 4.5")
        self.add_as45_btn.clicked.connect(lambda: self.add_studio(AutomationStudioVersion.AS_45))
        button_layout.addWidget(self.add_as45_btn)
        
        self.add_as6_btn = QPushButton("Add AS 6")
        self.add_as6_btn.clicked.connect(lambda: self.add_studio(AutomationStudioVersion.AS_6))
        button_layout.addWidget(self.add_as6_btn)
        
        self.remove_studio_btn = QPushButton("Remove Selected")
        self.remove_studio_btn.setObjectName("danger")
        self.remove_studio_btn.clicked.connect(self.remove_selected_studio)
        self.remove_studio_btn.setEnabled(False)
        button_layout.addWidget(self.remove_studio_btn)
        
        layout.addLayout(button_layout)
        
        # Connect selection change
        self.studio_list.itemSelectionChanged.connect(self.on_studio_selection_changed)
        
        parent_layout.addWidget(group)
    
    def setup_project_group(self, parent_layout):
        """Setup the project root configuration group."""
        group = QGroupBox("Project Root Directory")
        layout = QVBoxLayout(group)
        
        # Instructions
        instructions = QLabel(
            "Select the root directory of your project (should contain Logical and Physical folders)"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Path selection
        path_layout = QHBoxLayout()
        
        self.project_path_edit = QLineEdit()
        self.project_path_edit.setReadOnly(True)
        self.project_path_edit.setPlaceholderText("No project root selected...")
        path_layout.addWidget(self.project_path_edit)
        
        self.browse_project_btn = QPushButton("Browse...")
        self.browse_project_btn.clicked.connect(self.browse_project_root)
        path_layout.addWidget(self.browse_project_btn)
        
        layout.addLayout(path_layout)
        parent_layout.addWidget(group)
        
        # Load existing project root
        existing_root = self.config_manager.get_project_root()
        if existing_root and existing_root.exists():
            self.project_path_edit.setText(str(existing_root))
    
    def setup_buttons(self, parent_layout):
        """Setup dialog buttons."""
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("secondary")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        button_layout.addStretch()
        
        self.save_btn = QPushButton("Save & Continue")
        self.save_btn.setObjectName("primary")
        self.save_btn.clicked.connect(self.save_configuration)
        button_layout.addWidget(self.save_btn)
        
        parent_layout.addLayout(button_layout)
    
    def load_existing_studios(self):
        """Load existing studio configurations."""
        try:
            self.configured_studios = self.config_manager.get_automation_studios()
            self.update_studio_list()
        except Exception as e:
            logger.error(f"Error loading existing studios: {e}")
    
    def add_studio(self, version: AutomationStudioVersion):
        """Add a new automation studio configuration."""
        try:
            # Open file dialog to select executable
            file_dialog = QFileDialog(self)
            file_dialog.setWindowTitle(f"Select Automation Studio {version.value} Executable")
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            file_dialog.setNameFilter("Executable files (*.exe)")
            
            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    exe_path = Path(selected_files[0])
                    
                    # Check if this version is already configured
                    for studio in self.configured_studios:
                        if studio.version == version:
                            reply = QMessageBox.question(
                                self,
                                "Version Already Exists",
                                f"Automation Studio {version.value} is already configured. "
                                "Do you want to replace it?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
                            if reply == QMessageBox.StandardButton.No:
                                return
                            else:
                                # Remove existing studio
                                self.configured_studios = [
                                    s for s in self.configured_studios if s.version != version
                                ]
                                break
                    
                    # Create new studio configuration
                    if version == AutomationStudioVersion.AS_45:
                        studio = AutomationStudio.create_as45(exe_path)
                    else:
                        studio = AutomationStudio.create_as6(exe_path)
                    
                    self.configured_studios.append(studio)
                    self.update_studio_list()
                    
                    logger.info(f"Added studio configuration: {studio.display_name}")
                    
        except Exception as e:
            logger.error(f"Error adding studio: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to add Automation Studio configuration:\n{str(e)}"
            )
    
    def remove_selected_studio(self):
        """Remove the selected studio configuration."""
        try:
            current_item = self.studio_list.currentItem()
            if current_item:
                row = self.studio_list.row(current_item)
                if 0 <= row < len(self.configured_studios):
                    studio = self.configured_studios[row]
                    
                    reply = QMessageBox.question(
                        self,
                        "Confirm Removal",
                        f"Are you sure you want to remove {studio.display_name}?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        self.configured_studios.pop(row)
                        self.update_studio_list()
                        logger.info(f"Removed studio configuration: {studio.display_name}")
                        
        except Exception as e:
            logger.error(f"Error removing studio: {e}")
            QMessageBox.critical(
                self,
                "Error", 
                f"Failed to remove studio configuration:\n{str(e)}"
            )
    
    def browse_project_root(self):
        """Browse for project root directory."""
        try:
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Select Project Root Directory")
            dialog.setFileMode(QFileDialog.FileMode.Directory)
            
            if dialog.exec() == QFileDialog.DialogCode.Accepted:
                selected_dirs = dialog.selectedFiles()
                if selected_dirs:
                    project_root = Path(selected_dirs[0])
                    self.project_path_edit.setText(str(project_root))
                    logger.info(f"Project root selected: {project_root}")
                    
        except Exception as e:
            logger.error(f"Error browsing project root: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to select project root:\n{str(e)}"
            )
    
    def update_studio_list(self):
        """Update the studio list widget."""
        self.studio_list.clear()
        
        for studio in self.configured_studios:
            item_text = f"{studio.display_name}\n{studio.executable_path}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, studio)
            self.studio_list.addItem(item)
    
    def on_studio_selection_changed(self):
        """Handle studio selection changes."""
        has_selection = bool(self.studio_list.currentItem())
        self.remove_studio_btn.setEnabled(has_selection)
    
    def save_configuration(self):
        """Save the configuration and close dialog."""
        try:
            # Validate configuration
            if not self.configured_studios:
                QMessageBox.warning(
                    self,
                    "Configuration Incomplete",
                    "Please add at least one Automation Studio installation."
                )
                return
            
            project_root_text = self.project_path_edit.text().strip()
            if not project_root_text:
                QMessageBox.warning(
                    self,
                    "Configuration Incomplete", 
                    "Please select a project root directory."
                )
                return
            
            project_root = Path(project_root_text)
            if not project_root.exists():
                QMessageBox.warning(
                    self,
                    "Invalid Path",
                    "The selected project root directory does not exist."
                )
                return
            
            # Save studio configurations
            for studio in self.configured_studios:
                if not self.config_manager.add_automation_studio(studio):
                    raise Exception(f"Failed to save {studio.display_name}")
            
            # Save project root
            if not self.config_manager.set_project_root(project_root):
                raise Exception("Failed to save project root")
            
            logger.info("Configuration saved successfully")
            self.studios_configured.emit()
            self.accept()
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save configuration:\n{str(e)}"
            )
