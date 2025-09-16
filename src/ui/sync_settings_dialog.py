"""
Auto-sync settings dialog for configuring synchronization behavior.
"""
import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QCheckBox, QSpinBox, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.models.sync_settings import AutoSyncSettings
from src.services.sync_config_service import SyncConfigService
from src.ui.styles import MAIN_STYLE


logger = logging.getLogger(__name__)


class SyncSettingsDialog(QDialog):
    """Dialog for configuring auto-sync settings."""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, config_service: SyncConfigService, parent=None):
        """Initialize sync settings dialog."""
        super().__init__(parent)
        self.config_service = config_service
        self.current_settings = config_service.get_settings()
        
        # UI components
        self.sync_on_as_close_cb: Optional[QCheckBox] = None
        self.sync_on_selector_close_cb: Optional[QCheckBox] = None
        self.periodic_sync_enabled_cb: Optional[QCheckBox] = None
        self.periodic_interval_spin: Optional[QSpinBox] = None
        self.log_operations_cb: Optional[QCheckBox] = None
        self.backup_before_sync_cb: Optional[QCheckBox] = None
        self.max_backups_spin: Optional[QSpinBox] = None
        
        self.setup_ui()
        self.load_current_settings()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Auto-Sync Settings")
        self.setModal(True)
        self.resize(500, 400)
        
        # Apply styles
        self.setStyleSheet(MAIN_STYLE)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Auto-Sync Configuration")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Configure when and how files are automatically synchronized")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Sync triggers group
        self.setup_sync_triggers_group(layout)
        
        # Periodic sync group
        self.setup_periodic_sync_group(layout)
        
        # Safety and logging group
        self.setup_safety_logging_group(layout)
        
        # Buttons
        self.setup_buttons(layout)
        
    def setup_sync_triggers_group(self, parent_layout):
        """Setup the sync triggers configuration group."""
        group = QGroupBox("Sync Triggers")
        layout = QVBoxLayout(group)
        
        # Automation Studio close sync
        self.sync_on_as_close_cb = QCheckBox("Sync when Automation Studio closes")
        self.sync_on_as_close_cb.setToolTip(
            "Automatically sync files when any Automation Studio process closes"
        )
        layout.addWidget(self.sync_on_as_close_cb)
        
        # Selector close sync
        self.sync_on_selector_close_cb = QCheckBox("Sync when Selector application closes")
        self.sync_on_selector_close_cb.setToolTip(
            "Automatically sync files when the Selector application is closed"
        )
        layout.addWidget(self.sync_on_selector_close_cb)
        
        parent_layout.addWidget(group)
    
    def setup_periodic_sync_group(self, parent_layout):
        """Setup the periodic sync configuration group."""
        group = QGroupBox("Periodic Sync")
        layout = QFormLayout(group)
        
        # Enable periodic sync
        self.periodic_sync_enabled_cb = QCheckBox("Enable periodic sync")
        self.periodic_sync_enabled_cb.setToolTip(
            "Automatically check for changes and sync at regular intervals"
        )
        self.periodic_sync_enabled_cb.toggled.connect(self.on_periodic_sync_toggled)
        layout.addRow("", self.periodic_sync_enabled_cb)
        
        # Sync interval
        interval_layout = QHBoxLayout()
        
        self.periodic_interval_spin = QSpinBox()
        self.periodic_interval_spin.setMinimum(1)
        self.periodic_interval_spin.setMaximum(60)
        self.periodic_interval_spin.setSuffix(" minutes")
        self.periodic_interval_spin.setToolTip(
            "How often to check for changes (1-60 minutes)"
        )
        interval_layout.addWidget(self.periodic_interval_spin)
        interval_layout.addStretch()
        
        layout.addRow("Check interval:", interval_layout)
        
        parent_layout.addWidget(group)
    
    def setup_safety_logging_group(self, parent_layout):
        """Setup the safety and logging configuration group."""
        group = QGroupBox("Safety & Logging")
        layout = QFormLayout(group)
        
        # Log operations
        self.log_operations_cb = QCheckBox("Log sync operations")
        self.log_operations_cb.setToolTip(
            "Write detailed logs of all sync operations to the session log"
        )
        layout.addRow("", self.log_operations_cb)
        
        # Backup before sync
        self.backup_before_sync_cb = QCheckBox("Create backups before sync")
        self.backup_before_sync_cb.setToolTip(
            "Create timestamped backups of directories before overwriting"
        )
        self.backup_before_sync_cb.toggled.connect(self.on_backup_toggled)
        layout.addRow("", self.backup_before_sync_cb)
        
        # Max backups
        backup_layout = QHBoxLayout()
        
        self.max_backups_spin = QSpinBox()
        self.max_backups_spin.setMinimum(0)
        self.max_backups_spin.setMaximum(10)
        self.max_backups_spin.setToolTip(
            "Maximum number of backups to keep (0 = unlimited)"
        )
        backup_layout.addWidget(self.max_backups_spin)
        backup_layout.addStretch()
        
        layout.addRow("Max backups:", backup_layout)
        
        parent_layout.addWidget(group)
    
    def setup_buttons(self, parent_layout):
        """Setup dialog buttons."""
        button_layout = QHBoxLayout()
        
        # Reset to defaults button
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setObjectName("secondary")
        reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("primary")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        parent_layout.addLayout(button_layout)
    
    def load_current_settings(self):
        """Load current settings into the UI."""
        try:
            settings = self.current_settings
            
            # Sync triggers
            self.sync_on_as_close_cb.setChecked(settings.sync_on_automation_studio_close)
            self.sync_on_selector_close_cb.setChecked(settings.sync_on_selector_close)
            
            # Periodic sync
            self.periodic_sync_enabled_cb.setChecked(settings.periodic_sync_enabled)
            self.periodic_interval_spin.setValue(settings.periodic_sync_interval_minutes)
            
            # Safety and logging
            self.log_operations_cb.setChecked(settings.log_sync_operations)
            self.backup_before_sync_cb.setChecked(settings.backup_before_sync)
            self.max_backups_spin.setValue(settings.max_backups)
            
            # Update UI state
            self.on_periodic_sync_toggled()
            self.on_backup_toggled()
            
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
    
    def on_periodic_sync_toggled(self):
        """Handle periodic sync checkbox toggle."""
        enabled = self.periodic_sync_enabled_cb.isChecked()
        self.periodic_interval_spin.setEnabled(enabled)
    
    def on_backup_toggled(self):
        """Handle backup checkbox toggle."""
        enabled = self.backup_before_sync_cb.isChecked()
        self.max_backups_spin.setEnabled(enabled)
    
    def get_settings_from_ui(self) -> AutoSyncSettings:
        """Create AutoSyncSettings object from current UI values."""
        return AutoSyncSettings(
            sync_on_automation_studio_close=self.sync_on_as_close_cb.isChecked(),
            sync_on_selector_close=self.sync_on_selector_close_cb.isChecked(),
            periodic_sync_enabled=self.periodic_sync_enabled_cb.isChecked(),
            periodic_sync_interval_minutes=self.periodic_interval_spin.value(),
            log_sync_operations=self.log_operations_cb.isChecked(),
            backup_before_sync=self.backup_before_sync_cb.isChecked(),
            max_backups=self.max_backups_spin.value()
        )
    
    def save_settings(self):
        """Save settings and close dialog."""
        try:
            new_settings = self.get_settings_from_ui()
            
            # Validate settings
            if not new_settings.validate():
                QMessageBox.warning(
                    self,
                    "Invalid Settings",
                    "Please check your settings:\n\n"
                    "• Sync interval must be between 1-60 minutes\n"
                    "• Max backups must be between 0-10"
                )
                return
            
            # Save settings
            if self.config_service.update_settings(new_settings):
                self.current_settings = new_settings
                self.settings_changed.emit()
                
                QMessageBox.information(
                    self,
                    "Settings Saved",
                    "Auto-sync settings have been saved successfully.\n\n"
                    "Changes will take effect immediately."
                )
                
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Save Error",
                    "Failed to save settings to configuration file.\n\n"
                    "Please check file permissions and try again."
                )
                
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save settings:\n{str(e)}"
            )
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        try:
            reply = QMessageBox.question(
                self,
                "Reset to Defaults",
                "Are you sure you want to reset all auto-sync settings to their default values?\n\n"
                "This will:\n"
                "• Enable all sync triggers\n"
                "• Set periodic sync to 5 minutes\n"
                "• Enable logging and backups\n"
                "• Set max backups to 3",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                default_settings = AutoSyncSettings()
                
                # Update UI with defaults
                self.sync_on_as_close_cb.setChecked(default_settings.sync_on_automation_studio_close)
                self.sync_on_selector_close_cb.setChecked(default_settings.sync_on_selector_close)
                self.periodic_sync_enabled_cb.setChecked(default_settings.periodic_sync_enabled)
                self.periodic_interval_spin.setValue(default_settings.periodic_sync_interval_minutes)
                self.log_operations_cb.setChecked(default_settings.log_sync_operations)
                self.backup_before_sync_cb.setChecked(default_settings.backup_before_sync)
                self.max_backups_spin.setValue(default_settings.max_backups)
                
                # Update UI state
                self.on_periodic_sync_toggled()
                self.on_backup_toggled()
                
        except Exception as e:
            logger.error(f"Error resetting to defaults: {e}")
            QMessageBox.critical(
                self,
                "Reset Error",
                f"Failed to reset settings:\n{str(e)}"
            )
