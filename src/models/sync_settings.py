"""
Data models for auto-sync settings.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AutoSyncSettings:
    """Configuration for automatic file synchronization."""
    
    # Sync triggers
    sync_on_automation_studio_close: bool = True
    sync_on_selector_close: bool = True
    periodic_sync_enabled: bool = True
    
    # Timing settings
    periodic_sync_interval_minutes: int = 5
    
    # Safety and logging
    log_sync_operations: bool = True
    backup_before_sync: bool = True
    max_backups: int = 3
    
    def validate(self) -> bool:
        """Validate settings values."""
        if not (1 <= self.periodic_sync_interval_minutes <= 60):
            return False
        if not (0 <= self.max_backups <= 10):
            return False
        return True
    
    @property
    def periodic_sync_interval_seconds(self) -> int:
        """Get periodic sync interval in seconds."""
        return self.periodic_sync_interval_minutes * 60


@dataclass
class SyncState:
    """Current state of the sync system."""
    
    # Current session info
    active_studio_version: Optional[str] = None
    active_studio_process_id: Optional[int] = None
    libraries_source_path: Optional[Path] = None
    
    # Timing info
    last_sync_timestamp: Optional[float] = None
    last_check_timestamp: Optional[float] = None
    
    # Statistics
    total_syncs_performed: int = 0
    files_synced_this_session: int = 0
    
    def reset_session(self):
        """Reset session-specific data."""
        self.active_studio_version = None
        self.active_studio_process_id = None
        self.libraries_source_path = None
        self.files_synced_this_session = 0
