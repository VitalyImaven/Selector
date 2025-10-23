"""
Secret admin panel for advanced configuration management.
Activated with Ctrl+Alt+Shift+P
"""
import logging
import random
import sys
import os
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QGroupBox, QCheckBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QFont

# Try to import multimedia support (may not be available)
try:
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
    MULTIMEDIA_AVAILABLE = True
except ImportError:
    MULTIMEDIA_AVAILABLE = False
    logger.warning("PyQt6.QtMultimedia not available - sound effects disabled")

from src.config.settings import ConfigManager
from src.ui.styles import MAIN_STYLE


logger = logging.getLogger(__name__)


# Funny messages for wrong password attempts
WRONG_PASSWORD_MESSAGES = [
    "🚨 Aaaah! You're trying to hack me!\nI'm calling the cyber police! 👮",
    "⚠️ ALERT! ALERT!\nUnauthorized access detected!\nInitiating self-destruct sequence... 💥\n\n(Just kidding 😄)",
    "🔥 Oh no! A hacker!\nPreparing to nuke your PC...\n\n(Relax, I'm just messing with you 😉)",
    "🤖 INTRUDER ALERT!\nActivating defense protocols!\nYour PC will explode in 3... 2... 1...\n\n(Not really though 😂)",
    "👾 Nice try, hackerman!\nBut I'm protected by Vitaly Grosman's secret password!\nBetter luck next time! 😎",
    "🎭 Wrong password, my friend!\nDid you really think it would be THAT easy?\nGo ask Vitaly! 😏",
    "🔐 Access DENIED!\nThis is a secure area!\nUnless you have the magic number... 🎩✨",
    "⚡ SECURITY BREACH DETECTED!\nDeploying defensive memes!\nPreparing to rickroll your entire network!\n\n(Just kidding, nice try though! 😄)",
    "🎪 Nope! Wrong code!\nThe secret password is guarded by dragons! 🐉\nAnd they're very hungry today...",
    "🌟 So close, yet so far!\nThe password is out there...\nSomewhere in the code... or in Vitaly's brain! 🧠"
]


class PasswordDialog(QDialog):
    """Password entry dialog for admin access."""
    
    def __init__(self, parent=None):
        """Initialize password dialog."""
        super().__init__(parent)
        self.password_correct = False
        self.imperial_march_player = None
        self.valhalla_player = None
        self.setup_audio()
        self.setup_ui()
        self.play_imperial_march()
    
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("🔐 Admin Access")
        self.setModal(True)
        self.setFixedSize(400, 180)
        self.setStyleSheet(MAIN_STYLE)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🔒 Secret Admin Panel")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Instruction
        instruction = QLabel("Enter the secret password:")
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("●●●●●")
        self.password_input.returnPressed.connect(self.check_password)
        layout.addWidget(self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setMinimumWidth(180)
        cancel_btn.setMinimumHeight(35)
        button_layout.addWidget(cancel_btn)
        
        submit_btn = QPushButton("Submit")
        submit_btn.setObjectName("primary")
        submit_btn.clicked.connect(self.check_password)
        submit_btn.setDefault(True)
        submit_btn.setMinimumWidth(180)
        submit_btn.setMinimumHeight(35)
        button_layout.addWidget(submit_btn)
        
        layout.addLayout(button_layout)
        
        # Focus on password input
        self.password_input.setFocus()
    
    def setup_audio(self):
        """Setup audio players for sound effects."""
        if not MULTIMEDIA_AVAILABLE:
            return
        
        try:
            # Get base path
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                current_file = os.path.abspath(__file__)
                ui_dir = os.path.dirname(current_file)
                src_dir = os.path.dirname(ui_dir)
                base_path = os.path.dirname(src_dir)
            
            # Imperial March for password entry
            imperial_path = os.path.join(base_path, 'assets', 'Star Wars- The Imperial March .mp3')
            if os.path.exists(imperial_path):
                self.imperial_march_player = QMediaPlayer()
                self.imperial_audio_output = QAudioOutput()
                self.imperial_march_player.setAudioOutput(self.imperial_audio_output)
                self.imperial_march_player.setSource(QUrl.fromLocalFile(imperial_path))
                self.imperial_audio_output.setVolume(0.5)  # 50% volume
            
            # Valhalla for success
            valhalla_path = os.path.join(base_path, 'assets', 'VALHALLA CALLING.mp4')
            if os.path.exists(valhalla_path):
                self.valhalla_player = QMediaPlayer()
                self.valhalla_audio_output = QAudioOutput()
                self.valhalla_player.setAudioOutput(self.valhalla_audio_output)
                self.valhalla_player.setSource(QUrl.fromLocalFile(valhalla_path))
                self.valhalla_audio_output.setVolume(0.6)  # 60% volume
                
        except Exception as e:
            logger.warning(f"Could not setup audio: {e}")
    
    def play_imperial_march(self):
        """Play Imperial March when dialog opens."""
        try:
            if self.imperial_march_player:
                self.imperial_march_player.play()
        except Exception as e:
            logger.warning(f"Could not play Imperial March: {e}")
    
    def play_valhalla(self):
        """Play Valhalla Calling when password is correct."""
        try:
            # Stop Imperial March
            if self.imperial_march_player:
                self.imperial_march_player.stop()
            
            # Play Valhalla
            if self.valhalla_player:
                self.valhalla_player.play()
        except Exception as e:
            logger.warning(f"Could not play Valhalla: {e}")
    
    def closeEvent(self, event):
        """Stop music immediately when dialog closes."""
        self.stop_all_music()
        event.accept()
    
    def reject(self):
        """Override reject to stop music when cancelled."""
        self.stop_all_music()
        super().reject()
    
    def check_password(self):
        """Check if the entered password is correct."""
        entered_password = self.password_input.text()
        
        if entered_password == "27787":
            # Correct password! Play victory music!
            self.play_valhalla()
            self.password_correct = True
            
            # Show epic success message
            QMessageBox.information(
                self,
                "🎉 ACCESS GRANTED!",
                "Welcome to the Secret Admin Panel, Vitaly!\n\n"
                "🔓 Password accepted!\n"
                "⚡ Admin powers activated!\n\n"
                "Enjoy your admin privileges! 😎"
            )
            
            # Stop Imperial March but keep Valhalla playing
            if self.imperial_march_player:
                self.imperial_march_player.stop()
            
            # Don't stop Valhalla - it will keep playing in admin panel
            self.accept()
        else:
            # Wrong password - show funny message
            funny_message = random.choice(WRONG_PASSWORD_MESSAGES)
            QMessageBox.warning(
                self,
                "🚫 Access Denied!",
                funny_message
            )
            self.password_input.clear()
            self.password_input.setFocus()
    
    def stop_all_music(self):
        """Stop all audio playback immediately."""
        try:
            if self.imperial_march_player:
                self.imperial_march_player.stop()
            if self.valhalla_player:
                self.valhalla_player.stop()
        except Exception as e:
            logger.warning(f"Error stopping music: {e}")


class AdminPanel(QDialog):
    """Secret admin panel for configuration management."""
    
    config_cleared = pyqtSignal()
    
    def __init__(self, config_manager: ConfigManager, valhalla_player=None, parent=None):
        """Initialize admin panel."""
        super().__init__(parent)
        self.config_manager = config_manager
        self.valhalla_player = valhalla_player
        self.setup_ui()
    
    def closeEvent(self, event):
        """Stop music when admin panel closes."""
        try:
            if self.valhalla_player:
                self.valhalla_player.stop()
        except:
            pass
        event.accept()
    
    def reject(self):
        """Stop music when cancelled."""
        try:
            if self.valhalla_player:
                self.valhalla_player.stop()
        except:
            pass
        super().reject()
    
    def accept(self):
        """Stop music when accepted."""
        try:
            if self.valhalla_player:
                self.valhalla_player.stop()
        except:
            pass
        super().accept()
    
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("🔧 Admin Panel - Configuration Manager")
        self.setModal(True)
        self.resize(500, 400)
        self.setStyleSheet(MAIN_STYLE)
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("⚙️ Secret Admin Panel")
        header.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #e74c3c;
                margin-bottom: 10px;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        subtitle = QLabel("🔐 You have entered the secret area!\nBe careful what you delete...")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        layout.addWidget(subtitle)
        
        # Configuration cleanup options
        self.setup_cleanup_options(layout)
        
        # Danger zone
        self.setup_danger_zone(layout)
        
        # Buttons
        self.setup_buttons(layout)
    
    def setup_cleanup_options(self, parent_layout):
        """Setup cleanup options."""
        group = QGroupBox("🗑️ Configuration Cleanup")
        layout = QVBoxLayout(group)
        
        # Project cleanup
        self.clear_projects_cb = QCheckBox("Clear all project configurations")
        self.clear_projects_cb.setToolTip("Remove all configured project paths from the application")
        layout.addWidget(self.clear_projects_cb)
        
        # Studio cleanup
        self.clear_studios_cb = QCheckBox("Clear all Automation Studio configurations")
        self.clear_studios_cb.setToolTip("Remove all configured AS installation paths")
        layout.addWidget(self.clear_studios_cb)
        
        # Sync settings cleanup
        self.clear_sync_cb = QCheckBox("Reset auto-sync settings to defaults")
        self.clear_sync_cb.setToolTip("Reset all auto-sync configuration to default values")
        layout.addWidget(self.clear_sync_cb)
        
        # Log cleanup
        self.clear_logs_cb = QCheckBox("Delete all log files")
        self.clear_logs_cb.setToolTip("Remove all session and application log files")
        layout.addWidget(self.clear_logs_cb)
        
        parent_layout.addWidget(group)
    
    def setup_danger_zone(self, parent_layout):
        """Setup danger zone section."""
        danger_frame = QFrame()
        danger_frame.setStyleSheet("""
            QFrame {
                background-color: #fadbd8;
                border: 2px solid #e74c3c;
                border-radius: 6px;
                padding: 10px;
                margin: 10px 0px;
            }
        """)
        danger_layout = QVBoxLayout(danger_frame)
        
        danger_title = QLabel("⚠️ DANGER ZONE")
        danger_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #c0392b;
            }
        """)
        danger_layout.addWidget(danger_title)
        
        self.delete_all_cb = QCheckBox("🔥 DELETE EVERYTHING (Complete Reset)")
        self.delete_all_cb.setStyleSheet("QCheckBox { color: #c0392b; font-weight: bold; }")
        self.delete_all_cb.setToolTip("Clear all configuration, logs, and settings - complete fresh start")
        self.delete_all_cb.toggled.connect(self.on_delete_all_toggled)
        danger_layout.addWidget(self.delete_all_cb)
        
        parent_layout.addWidget(danger_frame)
    
    def setup_buttons(self, parent_layout):
        """Setup dialog buttons."""
        button_layout = QHBoxLayout()
        
        close_btn = QPushButton("Close")
        close_btn.setObjectName("secondary")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        
        button_layout.addStretch()
        
        self.execute_btn = QPushButton("Execute Cleanup")
        self.execute_btn.setObjectName("danger")
        self.execute_btn.clicked.connect(self.execute_cleanup)
        button_layout.addWidget(self.execute_btn)
        
        parent_layout.addLayout(button_layout)
    
    def on_delete_all_toggled(self, checked):
        """Handle delete all checkbox toggle."""
        if checked:
            # Select all options
            self.clear_projects_cb.setChecked(True)
            self.clear_studios_cb.setChecked(True)
            self.clear_sync_cb.setChecked(True)
            self.clear_logs_cb.setChecked(True)
            
            # Disable individual checkboxes
            self.clear_projects_cb.setEnabled(False)
            self.clear_studios_cb.setEnabled(False)
            self.clear_sync_cb.setEnabled(False)
            self.clear_logs_cb.setEnabled(False)
        else:
            # Enable individual checkboxes
            self.clear_projects_cb.setEnabled(True)
            self.clear_studios_cb.setEnabled(True)
            self.clear_sync_cb.setEnabled(True)
            self.clear_logs_cb.setEnabled(True)
    
    def execute_cleanup(self):
        """Execute the selected cleanup operations."""
        try:
            # Check if anything is selected
            if not any([
                self.clear_projects_cb.isChecked(),
                self.clear_studios_cb.isChecked(),
                self.clear_sync_cb.isChecked(),
                self.clear_logs_cb.isChecked()
            ]):
                QMessageBox.information(
                    self,
                    "Nothing Selected",
                    "Please select at least one cleanup option."
                )
                return
            
            # Build confirmation message
            operations = []
            if self.clear_projects_cb.isChecked():
                operations.append("• Clear all project configurations")
            if self.clear_studios_cb.isChecked():
                operations.append("• Clear all Automation Studio configurations")
            if self.clear_sync_cb.isChecked():
                operations.append("• Reset auto-sync settings")
            if self.clear_logs_cb.isChecked():
                operations.append("• Delete all log files")
            
            operations_text = "\n".join(operations)
            
            # Confirm with user
            reply = QMessageBox.warning(
                self,
                "⚠️ Confirm Cleanup",
                f"Are you sure you want to perform these operations?\n\n"
                f"{operations_text}\n\n"
                f"This action cannot be undone!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
            
            # Perform cleanup operations
            results = []
            
            if self.clear_projects_cb.isChecked():
                success = self.clear_all_projects()
                results.append(("Projects", success))
            
            if self.clear_studios_cb.isChecked():
                success = self.clear_all_studios()
                results.append(("Studios", success))
            
            if self.clear_sync_cb.isChecked():
                success = self.reset_sync_settings()
                results.append(("Sync Settings", success))
            
            if self.clear_logs_cb.isChecked():
                success = self.delete_log_files()
                results.append(("Log Files", success))
            
            # Show results
            success_list = [name for name, success in results if success]
            failed_list = [name for name, success in results if not success]
            
            result_message = ""
            if success_list:
                result_message += "✓ Successful:\n" + "\n".join(f"  • {item}" for item in success_list)
            if failed_list:
                if result_message:
                    result_message += "\n\n"
                result_message += "✗ Failed:\n" + "\n".join(f"  • {item}" for item in failed_list)
            
            QMessageBox.information(
                self,
                "Cleanup Complete",
                result_message or "No operations performed"
            )
            
            if success_list:
                self.config_cleared.emit()
                self.accept()
                
        except Exception as e:
            logger.error(f"Error in admin cleanup: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to perform cleanup:\n{str(e)}"
            )
    
    def clear_all_projects(self) -> bool:
        """Clear all project configurations."""
        try:
            settings = self.config_manager.get_settings()
            settings.project_paths = []
            settings.last_selected_project = None
            settings.project_root_path = None
            self.config_manager.save_settings()
            logger.info("All projects cleared via admin panel")
            return True
        except Exception as e:
            logger.error(f"Error clearing projects: {e}")
            return False
    
    def clear_all_studios(self) -> bool:
        """Clear all studio configurations."""
        try:
            settings = self.config_manager.get_settings()
            settings.automation_studios = {}
            settings.last_selected_studio = None
            self.config_manager.save_settings()
            logger.info("All studios cleared via admin panel")
            return True
        except Exception as e:
            logger.error(f"Error clearing studios: {e}")
            return False
    
    def reset_sync_settings(self) -> bool:
        """Reset sync settings to defaults."""
        try:
            from src.services.sync_config_service import SyncConfigService
            sync_config = SyncConfigService()
            success = sync_config.reset_to_defaults()
            if success:
                logger.info("Sync settings reset via admin panel")
            return success
        except Exception as e:
            logger.error(f"Error resetting sync settings: {e}")
            return False
    
    def delete_log_files(self) -> bool:
        """Delete all log files."""
        try:
            import shutil
            log_dir = Path.home() / ".automation_selector" / "logs"
            
            if log_dir.exists():
                deleted_count = 0
                for log_file in log_dir.iterdir():
                    if log_file.is_file():
                        log_file.unlink()
                        deleted_count += 1
                
                logger.info(f"Deleted {deleted_count} log files via admin panel")
                return True
            return True
        except Exception as e:
            logger.error(f"Error deleting log files: {e}")
            return False


