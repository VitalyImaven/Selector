"""
Configuration management for the Automation Studio Selector.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from src.models.automation_studio import AutomationStudio, AutomationStudioVersion


logger = logging.getLogger(__name__)


@dataclass
class AppSettings:
    """Application settings."""
    automation_studios: Dict[str, Dict] = None
    project_root_path: Optional[str] = None
    last_selected_studio: Optional[str] = None
    
    def __post_init__(self):
        if self.automation_studios is None:
            self.automation_studios = {}


class ConfigManager:
    """Manages application configuration and persistence."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager."""
        self.config_path = config_path or Path.home() / ".automation_selector" / "config.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._settings: Optional[AppSettings] = None
        
    def load_settings(self) -> AppSettings:
        """Load settings from file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._settings = AppSettings(**data)
                    logger.info(f"Settings loaded from {self.config_path}")
            else:
                self._settings = AppSettings()
                logger.info("Created new settings - config file not found")
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            self._settings = AppSettings()
            
        return self._settings
    
    def save_settings(self) -> bool:
        """Save current settings to file."""
        try:
            if self._settings is None:
                return False
                
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._settings), f, indent=2, ensure_ascii=False)
            
            logger.info(f"Settings saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def get_settings(self) -> AppSettings:
        """Get current settings."""
        if self._settings is None:
            return self.load_settings()
        return self._settings
    
    def add_automation_studio(self, studio: AutomationStudio) -> bool:
        """Add or update an automation studio configuration."""
        try:
            settings = self.get_settings()
            studio_data = {
                'name': studio.name,
                'version': studio.version.value,
                'executable_path': str(studio.executable_path),
                'libraries_suffix': studio.libraries_suffix,
                'physical_pkg_suffix': studio.physical_pkg_suffix,
                'project_file_suffix': studio.project_file_suffix
            }
            
            settings.automation_studios[studio.version.value] = studio_data
            self.save_settings()
            logger.info(f"Added automation studio: {studio.display_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding automation studio: {e}")
            return False
    
    def get_automation_studios(self) -> List[AutomationStudio]:
        """Get list of configured automation studios."""
        studios = []
        try:
            settings = self.get_settings()
            for version_key, studio_data in settings.automation_studios.items():
                version = AutomationStudioVersion(studio_data['version'])
                studio = AutomationStudio(
                    name=studio_data['name'],
                    version=version,
                    executable_path=Path(studio_data['executable_path']),
                    libraries_suffix=studio_data['libraries_suffix'],
                    physical_pkg_suffix=studio_data['physical_pkg_suffix'],
                    project_file_suffix=studio_data['project_file_suffix']
                )
                studios.append(studio)
        except Exception as e:
            logger.error(f"Error loading automation studios: {e}")
            
        return studios
    
    def set_project_root(self, root_path: Path) -> bool:
        """Set the project root path."""
        try:
            settings = self.get_settings()
            settings.project_root_path = str(root_path)
            self.save_settings()
            logger.info(f"Project root set to: {root_path}")
            return True
        except Exception as e:
            logger.error(f"Error setting project root: {e}")
            return False
    
    def get_project_root(self) -> Optional[Path]:
        """Get the configured project root path."""
        settings = self.get_settings()
        if settings.project_root_path:
            return Path(settings.project_root_path)
        return None
    
    def set_last_selected_studio(self, version: str) -> bool:
        """Set the last selected studio version."""
        try:
            settings = self.get_settings()
            settings.last_selected_studio = version
            self.save_settings()
            return True
        except Exception as e:
            logger.error(f"Error setting last selected studio: {e}")
            return False
    
    def get_last_selected_studio(self) -> Optional[str]:
        """Get the last selected studio version."""
        settings = self.get_settings()
        return settings.last_selected_studio
