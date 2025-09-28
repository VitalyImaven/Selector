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
    project_root_path: Optional[str] = None  # Keep for backward compatibility
    project_paths: List[Dict] = None  # New: multiple project paths
    last_selected_studio: Optional[str] = None
    last_selected_project: Optional[str] = None  # New: last selected project
    
    def __post_init__(self):
        if self.automation_studios is None:
            self.automation_studios = {}
        if self.project_paths is None:
            self.project_paths = []


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
    
    def add_project_path(self, name: str, path: Path, description: str = "") -> bool:
        """Add a project path to the list."""
        try:
            settings = self.get_settings()
            
            # Check if project already exists
            for project in settings.project_paths:
                if project.get('path') == str(path):
                    logger.warning(f"Project path already exists: {path}")
                    return False
            
            project_data = {
                'name': name,
                'path': str(path),
                'description': description,
                'added_date': str(Path(path).stat().st_mtime) if path.exists() else ""
            }
            
            settings.project_paths.append(project_data)
            self.save_settings()
            logger.info(f"Added project path: {name} -> {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding project path: {e}")
            return False
    
    def remove_project_path(self, path: Path) -> bool:
        """Remove a project path from the list."""
        try:
            settings = self.get_settings()
            original_count = len(settings.project_paths)
            
            settings.project_paths = [
                project for project in settings.project_paths 
                if project.get('path') != str(path)
            ]
            
            if len(settings.project_paths) < original_count:
                self.save_settings()
                logger.info(f"Removed project path: {path}")
                return True
            else:
                logger.warning(f"Project path not found for removal: {path}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing project path: {e}")
            return False
    
    def get_project_paths(self) -> List[Dict]:
        """Get list of all configured project paths."""
        settings = self.get_settings()
        return settings.project_paths.copy()
    
    def set_last_selected_project(self, path: Path) -> bool:
        """Set the last selected project path."""
        try:
            settings = self.get_settings()
            settings.last_selected_project = str(path)
            self.save_settings()
            return True
        except Exception as e:
            logger.error(f"Error setting last selected project: {e}")
            return False
    
    def get_last_selected_project(self) -> Optional[Path]:
        """Get the last selected project path."""
        settings = self.get_settings()
        if settings.last_selected_project:
            return Path(settings.last_selected_project)
        # Fallback to old single project root for backward compatibility
        return self.get_project_root()
    
    def migrate_single_project_to_list(self) -> bool:
        """Migrate old single project root to new project list format."""
        try:
            settings = self.get_settings()
            
            # If we have old project_root_path but no project_paths, migrate
            if settings.project_root_path and not settings.project_paths:
                old_path = Path(settings.project_root_path)
                if old_path.exists():
                    project_name = old_path.name
                    self.add_project_path(
                        name=project_name,
                        path=old_path,
                        description="Migrated from single project configuration"
                    )
                    logger.info(f"Migrated single project to list: {project_name}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error migrating single project: {e}")
            return False
