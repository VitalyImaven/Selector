"""
XML configuration service for auto-sync settings.
"""
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
from src.models.sync_settings import AutoSyncSettings


logger = logging.getLogger(__name__)


class SyncConfigService:
    """Manages auto-sync configuration via XML."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize sync configuration service."""
        self.config_path = config_path or Path.home() / ".automation_selector" / "auto_sync_config.xml"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._settings: Optional[AutoSyncSettings] = None
    
    def load_settings(self) -> AutoSyncSettings:
        """Load settings from XML file."""
        try:
            if self.config_path.exists():
                tree = ET.parse(self.config_path)
                root = tree.getroot()
                
                # Parse XML to settings
                settings = AutoSyncSettings()
                
                # Sync triggers
                studio_close_elem = root.find('SyncOnAutomationStudioClose')
                if studio_close_elem is not None:
                    settings.sync_on_automation_studio_close = studio_close_elem.get('enabled', 'true').lower() == 'true'
                
                selector_close_elem = root.find('SyncOnSelectorClose')
                if selector_close_elem is not None:
                    settings.sync_on_selector_close = selector_close_elem.get('enabled', 'true').lower() == 'true'
                
                periodic_elem = root.find('PeriodicSync')
                if periodic_elem is not None:
                    settings.periodic_sync_enabled = periodic_elem.get('enabled', 'true').lower() == 'true'
                    try:
                        settings.periodic_sync_interval_minutes = int(periodic_elem.get('intervalMinutes', '5'))
                    except ValueError:
                        settings.periodic_sync_interval_minutes = 5
                
                # Logging and backup
                logging_elem = root.find('LogSyncOperations')
                if logging_elem is not None:
                    settings.log_sync_operations = logging_elem.get('enabled', 'true').lower() == 'true'
                
                backup_elem = root.find('BackupBeforeSync')
                if backup_elem is not None:
                    settings.backup_before_sync = backup_elem.get('enabled', 'true').lower() == 'true'
                    try:
                        settings.max_backups = int(backup_elem.get('maxBackups', '3'))
                    except ValueError:
                        settings.max_backups = 3
                
                # Validate settings
                if not settings.validate():
                    logger.warning("Invalid settings found, using defaults")
                    settings = AutoSyncSettings()
                
                self._settings = settings
                logger.info(f"Auto-sync settings loaded from {self.config_path}")
                
            else:
                # Create default settings
                self._settings = AutoSyncSettings()
                self.save_settings()
                logger.info("Created default auto-sync settings")
                
        except Exception as e:
            logger.error(f"Error loading auto-sync settings: {e}")
            self._settings = AutoSyncSettings()
            
        return self._settings
    
    def save_settings(self) -> bool:
        """Save settings to XML file."""
        try:
            if self._settings is None:
                return False
            
            # Create XML structure
            root = ET.Element("AutoSyncSettings")
            
            # Add sync triggers
            studio_close = ET.SubElement(root, "SyncOnAutomationStudioClose")
            studio_close.set("enabled", str(self._settings.sync_on_automation_studio_close).lower())
            
            selector_close = ET.SubElement(root, "SyncOnSelectorClose") 
            selector_close.set("enabled", str(self._settings.sync_on_selector_close).lower())
            
            periodic = ET.SubElement(root, "PeriodicSync")
            periodic.set("enabled", str(self._settings.periodic_sync_enabled).lower())
            periodic.set("intervalMinutes", str(self._settings.periodic_sync_interval_minutes))
            
            # Add logging and backup settings
            log_ops = ET.SubElement(root, "LogSyncOperations")
            log_ops.set("enabled", str(self._settings.log_sync_operations).lower())
            
            backup = ET.SubElement(root, "BackupBeforeSync")
            backup.set("enabled", str(self._settings.backup_before_sync).lower())
            backup.set("maxBackups", str(self._settings.max_backups))
            
            # Write to file with proper formatting
            self._indent_xml(root)
            tree = ET.ElementTree(root)
            
            # Add XML declaration
            with open(self.config_path, 'wb') as f:
                f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
                tree.write(f, encoding='utf-8')
            
            logger.info(f"Auto-sync settings saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving auto-sync settings: {e}")
            return False
    
    def get_settings(self) -> AutoSyncSettings:
        """Get current settings."""
        if self._settings is None:
            return self.load_settings()
        return self._settings
    
    def update_settings(self, settings: AutoSyncSettings) -> bool:
        """Update and save settings."""
        if not settings.validate():
            logger.error("Invalid settings provided")
            return False
            
        self._settings = settings
        return self.save_settings()
    
    def _indent_xml(self, elem, level=0):
        """Add indentation to XML for pretty printing."""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent_xml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    def reset_to_defaults(self) -> bool:
        """Reset settings to defaults."""
        self._settings = AutoSyncSettings()
        return self.save_settings()
