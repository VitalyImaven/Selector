"""
File synchronization engine for automatic library syncing.
"""
import logging
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from src.models.sync_settings import AutoSyncSettings
from src.utils.logger import SessionLogger


logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """Information about a file for change detection."""
    path: Path
    size: int
    modified_time: float
    
    @classmethod
    def from_path(cls, path: Path) -> Optional['FileInfo']:
        """Create FileInfo from file path."""
        try:
            if path.exists() and path.is_file():
                stat = path.stat()
                return cls(
                    path=path,
                    size=stat.st_size,
                    modified_time=stat.st_mtime
                )
        except Exception as e:
            logger.error(f"Error getting file info for {path}: {e}")
        return None
    
    def has_changed(self, other: 'FileInfo') -> bool:
        """Check if file has changed compared to another FileInfo."""
        return (self.size != other.size or 
                abs(self.modified_time - other.modified_time) > 1.0)  # 1 second tolerance


class FileSyncEngine:
    """Engine for synchronizing files between directories."""
    
    def __init__(self, session_logger: Optional[SessionLogger] = None):
        """Initialize file sync engine."""
        self.session_logger = session_logger
        self._file_cache: Dict[Path, FileInfo] = {}
        self._last_scan_time: float = 0
    
    def scan_directory(self, directory: Path) -> Dict[Path, FileInfo]:
        """Scan directory and return file information."""
        file_info = {}
        
        try:
            if not directory.exists():
                return file_info
            
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    info = FileInfo.from_path(file_path)
                    if info:
                        # Use relative path as key for easier comparison
                        relative_path = file_path.relative_to(directory)
                        file_info[relative_path] = info
                        
        except Exception as e:
            logger.error(f"Error scanning directory {directory}: {e}")
            
        return file_info
    
    def detect_changes(self, source_dir: Path, target_dir: Path) -> Tuple[List[Path], List[Path], List[Path]]:
        """
        Detect changes between source and target directories.
        
        Returns:
            Tuple of (modified_files, new_files, deleted_files)
        """
        try:
            source_files = self.scan_directory(source_dir)
            target_files = self.scan_directory(target_dir)
            
            modified_files = []
            new_files = []
            deleted_files = []
            
            # Check for modified and new files
            for rel_path, target_info in target_files.items():
                if rel_path in source_files:
                    source_info = source_files[rel_path]
                    if target_info.has_changed(source_info):
                        modified_files.append(rel_path)
                else:
                    new_files.append(rel_path)
            
            # Check for deleted files (exist in source but not in target)
            for rel_path in source_files:
                if rel_path not in target_files:
                    deleted_files.append(rel_path)
            
            return modified_files, new_files, deleted_files
            
        except Exception as e:
            logger.error(f"Error detecting changes: {e}")
            return [], [], []
    
    def sync_files(self, source_dir: Path, target_dir: Path, 
                   files_to_sync: List[Path], settings: AutoSyncSettings) -> bool:
        """
        Sync specific files from target back to source.
        
        Args:
            source_dir: Source directory (e.g., Libraries_6)
            target_dir: Target directory (e.g., Libraries)
            files_to_sync: List of relative file paths to sync
            settings: Auto-sync settings
            
        Returns:
            True if sync was successful
        """
        try:
            if not files_to_sync:
                return True
            
            synced_count = 0
            
            # Create backup if enabled
            if settings.backup_before_sync:
                self._create_backup(source_dir, settings.max_backups)
            
            for rel_path in files_to_sync:
                try:
                    source_file = source_dir / rel_path
                    target_file = target_dir / rel_path
                    
                    if target_file.exists():
                        # Create parent directories if needed
                        source_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Copy file from target to source
                        shutil.copy2(target_file, source_file)
                        synced_count += 1
                        
                        if settings.log_sync_operations and self.session_logger:
                            self.session_logger.log_file_operation(
                                "Auto-sync", str(target_file), str(source_file)
                            )
                    
                    elif source_file.exists():
                        # File was deleted in target, delete from source
                        source_file.unlink()
                        synced_count += 1
                        
                        if settings.log_sync_operations and self.session_logger:
                            self.session_logger.log_file_operation(
                                "Auto-sync delete", str(source_file)
                            )
                
                except Exception as e:
                    logger.error(f"Error syncing file {rel_path}: {e}")
                    continue
            
            if synced_count > 0:
                logger.info(f"Auto-sync completed: {synced_count} files synced")
                if self.session_logger:
                    self.session_logger.log_project_operation(
                        "Auto-sync completed", f"{synced_count} files synced"
                    )
            
            return True
            
        except Exception as e:
            logger.error(f"Error during sync operation: {e}")
            if self.session_logger:
                self.session_logger.log_error(f"Auto-sync failed: {e}")
            return False
    
    def _create_backup(self, source_dir: Path, max_backups: int):
        """Create timestamped backup of source directory."""
        try:
            if not source_dir.exists():
                return
            
            backup_base = source_dir.parent / f"{source_dir.name}_backup"
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_dir = backup_base / timestamp
            
            # Create backup
            shutil.copytree(source_dir, backup_dir)
            logger.info(f"Backup created: {backup_dir}")
            
            # Clean up old backups
            self._cleanup_old_backups(backup_base, max_backups)
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
    
    def _cleanup_old_backups(self, backup_base: Path, max_backups: int):
        """Remove old backup directories, keeping only the most recent ones."""
        try:
            if not backup_base.exists() or max_backups <= 0:
                return
            
            # Get all backup directories sorted by creation time
            backup_dirs = [d for d in backup_base.iterdir() if d.is_dir()]
            backup_dirs.sort(key=lambda x: x.stat().st_ctime, reverse=True)
            
            # Remove excess backups
            for old_backup in backup_dirs[max_backups:]:
                shutil.rmtree(old_backup)
                logger.info(f"Removed old backup: {old_backup}")
                
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
    
    def perform_full_sync(self, source_dir: Path, target_dir: Path, 
                         settings: AutoSyncSettings) -> int:
        """
        Perform full sync of all changed files from target to source.
        
        Returns:
            Number of files synced
        """
        try:
            modified_files, new_files, deleted_files = self.detect_changes(source_dir, target_dir)
            all_changes = modified_files + new_files + deleted_files
            
            if not all_changes:
                return 0
            
            success = self.sync_files(source_dir, target_dir, all_changes, settings)
            return len(all_changes) if success else 0
            
        except Exception as e:
            logger.error(f"Error in full sync: {e}")
            return 0
    
    def has_changes(self, source_dir: Path, target_dir: Path) -> bool:
        """Check if there are any changes between directories."""
        try:
            modified, new, deleted = self.detect_changes(source_dir, target_dir)
            return len(modified) + len(new) + len(deleted) > 0
        except Exception as e:
            logger.error(f"Error checking for changes: {e}")
            return False
