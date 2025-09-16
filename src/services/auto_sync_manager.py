"""
Main auto-sync manager that orchestrates all synchronization operations.
"""
import logging
import time
from pathlib import Path
from typing import Optional
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

from src.models.automation_studio import AutomationStudio
from src.models.sync_settings import AutoSyncSettings, SyncState
from src.services.sync_config_service import SyncConfigService
from src.services.file_sync_engine import FileSyncEngine
from src.services.process_monitor import ProcessMonitor
from src.utils.logger import SessionLogger


logger = logging.getLogger(__name__)


class AutoSyncManager(QObject):
    """Main manager for automatic file synchronization."""
    
    # Signals
    sync_completed = pyqtSignal(int)  # Number of files synced
    sync_error = pyqtSignal(str)      # Error message
    
    def __init__(self, session_logger: Optional[SessionLogger] = None):
        """Initialize auto-sync manager."""
        super().__init__()
        
        self.session_logger = session_logger
        self.config_service = SyncConfigService()
        self.sync_engine = FileSyncEngine(session_logger)
        self.process_monitor = ProcessMonitor()
        
        # Current state
        self.sync_state = SyncState()
        self.project_root: Optional[Path] = None
        
        # Timers
        self.periodic_timer = QTimer()
        self.periodic_timer.timeout.connect(self._on_periodic_check)
        
        self.process_check_timer = QTimer()
        self.process_check_timer.timeout.connect(self._check_processes)
        self.process_check_timer.start(2000)  # Check every 2 seconds
        
        # Load initial settings
        self.settings = self.config_service.load_settings()
        self._update_periodic_timer()
        
        logger.info("Auto-sync manager initialized")
    
    def set_project_root(self, project_root: Path):
        """Set the project root directory."""
        self.project_root = project_root
        logger.info(f"Auto-sync project root set to: {project_root}")
    
    def register_automation_studio(self, studio: AutomationStudio):
        """Register an Automation Studio for process monitoring."""
        self.process_monitor.add_executable_path(studio.executable_path)
        logger.info(f"Registered AS for monitoring: {studio.display_name}")
    
    def start_session(self, studio: AutomationStudio):
        """Start a new sync session for the given studio."""
        try:
            self.sync_state.active_studio_version = studio.version.value
            self.sync_state.libraries_source_path = self._get_libraries_source_path(studio)
            self.sync_state.files_synced_this_session = 0
            
            logger.info(f"Auto-sync session started for {studio.display_name}")
            
            if self.session_logger:
                self.session_logger.log_project_operation(
                    "Auto-sync session started", 
                    f"Studio: {studio.display_name}"
                )
                
        except Exception as e:
            logger.error(f"Error starting sync session: {e}")
    
    def _get_libraries_source_path(self, studio: AutomationStudio) -> Path:
        """Get the source libraries path for a studio."""
        if self.project_root:
            return self.project_root / "Logical" / f"Libraries_{studio.libraries_suffix}"
        raise ValueError("Project root not set")
    
    def _get_libraries_target_path(self) -> Path:
        """Get the target libraries path."""
        if self.project_root:
            return self.project_root / "Logical" / "Libraries"
        raise ValueError("Project root not set")
    
    def _on_periodic_check(self):
        """Handle periodic sync check."""
        try:
            if not self.settings.periodic_sync_enabled:
                return
            
            if not self._can_perform_sync():
                return
            
            # Check for changes
            source_path = self.sync_state.libraries_source_path
            target_path = self._get_libraries_target_path()
            
            if source_path and self.sync_engine.has_changes(source_path, target_path):
                files_synced = self.sync_engine.perform_full_sync(
                    source_path, target_path, self.settings
                )
                
                if files_synced > 0:
                    self.sync_state.files_synced_this_session += files_synced
                    self.sync_state.last_sync_timestamp = time.time()
                    self.sync_completed.emit(files_synced)
                    
                    logger.info(f"Periodic sync completed: {files_synced} files")
            
            self.sync_state.last_check_timestamp = time.time()
            
        except Exception as e:
            logger.error(f"Error in periodic sync: {e}")
            self.sync_error.emit(str(e))
    
    def _check_processes(self):
        """Check for AS process changes."""
        try:
            # Check for new processes
            new_processes = self.process_monitor.scan_for_processes()
            for process_info in new_processes:
                logger.info(f"New AS process detected: {process_info.executable_path}")
            
            # Check for closed processes
            closed_processes = self.process_monitor.check_for_closed_processes()
            for process_info in closed_processes:
                self._on_process_closed(process_info)
                
        except Exception as e:
            logger.error(f"Error checking processes: {e}")
    
    def _on_process_closed(self, process_info):
        """Handle AS process closure."""
        try:
            if not self.settings.sync_on_automation_studio_close:
                return
            
            if not self._can_perform_sync():
                return
            
            # Perform sync
            source_path = self.sync_state.libraries_source_path
            target_path = self._get_libraries_target_path()
            
            if source_path:
                files_synced = self.sync_engine.perform_full_sync(
                    source_path, target_path, self.settings
                )
                
                if files_synced > 0:
                    self.sync_state.files_synced_this_session += files_synced
                    self.sync_state.last_sync_timestamp = time.time()
                    self.sync_completed.emit(files_synced)
                    
                    logger.info(f"AS close sync completed: {files_synced} files")
                    
                    if self.session_logger:
                        self.session_logger.log_project_operation(
                            "Auto-sync on AS close", 
                            f"{files_synced} files synced"
                        )
                        
        except Exception as e:
            logger.error(f"Error in AS close sync: {e}")
            self.sync_error.emit(str(e))
    
    def perform_manual_sync(self) -> int:
        """Perform manual sync and return number of files synced."""
        try:
            if not self._can_perform_sync():
                return 0
            
            source_path = self.sync_state.libraries_source_path
            target_path = self._get_libraries_target_path()
            
            if source_path:
                files_synced = self.sync_engine.perform_full_sync(
                    source_path, target_path, self.settings
                )
                
                if files_synced > 0:
                    self.sync_state.files_synced_this_session += files_synced
                    self.sync_state.last_sync_timestamp = time.time()
                    self.sync_completed.emit(files_synced)
                    
                    logger.info(f"Manual sync completed: {files_synced} files")
                
                return files_synced
            
        except Exception as e:
            logger.error(f"Error in manual sync: {e}")
            self.sync_error.emit(str(e))
        
        return 0
    
    def sync_on_application_close(self):
        """Perform sync when the selector application is closing."""
        try:
            if not self.settings.sync_on_selector_close:
                return
            
            if not self._can_perform_sync():
                return
            
            source_path = self.sync_state.libraries_source_path
            target_path = self._get_libraries_target_path()
            
            if source_path:
                files_synced = self.sync_engine.perform_full_sync(
                    source_path, target_path, self.settings
                )
                
                if files_synced > 0:
                    logger.info(f"Application close sync completed: {files_synced} files")
                    
                    if self.session_logger:
                        self.session_logger.log_project_operation(
                            "Auto-sync on app close", 
                            f"{files_synced} files synced"
                        )
                        
        except Exception as e:
            logger.error(f"Error in application close sync: {e}")
    
    def _can_perform_sync(self) -> bool:
        """Check if sync can be performed."""
        return (self.project_root is not None and 
                self.sync_state.libraries_source_path is not None and
                self.sync_state.libraries_source_path.exists())
    
    def reload_settings(self):
        """Reload settings from configuration."""
        self.settings = self.config_service.load_settings()
        self._update_periodic_timer()
        logger.info("Auto-sync settings reloaded")
    
    def update_settings(self, settings: AutoSyncSettings) -> bool:
        """Update and save settings."""
        if self.config_service.update_settings(settings):
            self.settings = settings
            self._update_periodic_timer()
            logger.info("Auto-sync settings updated")
            return True
        return False
    
    def _update_periodic_timer(self):
        """Update the periodic timer based on current settings."""
        if self.settings.periodic_sync_enabled:
            interval_ms = self.settings.periodic_sync_interval_seconds * 1000
            self.periodic_timer.start(interval_ms)
            logger.info(f"Periodic sync enabled: {self.settings.periodic_sync_interval_minutes} minutes")
        else:
            self.periodic_timer.stop()
            logger.info("Periodic sync disabled")
    
    def get_sync_statistics(self) -> dict:
        """Get sync statistics."""
        return {
            'active_studio': self.sync_state.active_studio_version,
            'files_synced_this_session': self.sync_state.files_synced_this_session,
            'total_syncs_performed': self.sync_state.total_syncs_performed,
            'last_sync_time': self.sync_state.last_sync_timestamp,
            'last_check_time': self.sync_state.last_check_timestamp,
            'periodic_sync_enabled': self.settings.periodic_sync_enabled,
            'sync_interval_minutes': self.settings.periodic_sync_interval_minutes
        }
    
    def stop(self):
        """Stop the auto-sync manager."""
        self.periodic_timer.stop()
        self.process_check_timer.stop()
        self.process_monitor.stop_monitoring()
        logger.info("Auto-sync manager stopped")
