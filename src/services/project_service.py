"""
Business logic for project operations and file management.
"""
import shutil
import logging
import time
import subprocess
from pathlib import Path
from typing import Optional, List
import psutil
from src.models.automation_studio import AutomationStudio, ProjectPaths
from src.utils.logger import SessionLogger


logger = logging.getLogger(__name__)


class ProjectOperationError(Exception):
    """Custom exception for project operations."""
    pass


class ProjectService:
    """Service for handling project operations and file management."""
    
    def __init__(self, session_logger: Optional[SessionLogger] = None):
        """Initialize project service."""
        self.session_logger = session_logger or SessionLogger()
    
    # ----------------------
    # Process safety helpers
    # ----------------------
    def _check_antivirus_running(self) -> str:
        """Check if common antivirus processes are running."""
        try:
            antivirus_processes = []
            antivirus_names = ['msmpeng', 'mssense', 'avast', 'avg', 'norton', 'mcafee', 
                              'kaspersky', 'defender', 'windowsdefender', 'sophossps']
            
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name'].lower()
                    for av_name in antivirus_names:
                        if av_name in name:
                            antivirus_processes.append(proc.info['name'])
                            break
                except:
                    continue
            
            if antivirus_processes:
                av_list = ", ".join(set(antivirus_processes[:3]))
                return f"\n\n⚠ ANTIVIRUS DETECTED: {av_list}\n   This may be scanning and locking the files.\n"
            return ""
        except:
            return ""
    
    def find_locking_processes(self, path: Path) -> str:
        """
        Find which processes have handles to files in the given path.
        Returns a formatted string with process information.
        """
        locking_info_parts = []
        
        try:
            logger.info(f"Attempting to identify processes locking: {path}")
            
            # Method 1: psutil open_files (most accurate but needs permissions)
            locking_procs = []
            path_str = str(path).lower()
            checked = 0
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    checked += 1
                    # Check if process has any open files in this directory
                    open_files = proc.open_files()
                    for f in open_files:
                        if path_str in f.path.lower():
                            proc_info = f"{proc.info['name']} (PID: {proc.info['pid']})"
                            locking_procs.append(proc_info)
                            logger.info(f"  Found locking process: {proc_info}")
                            break
                except psutil.AccessDenied:
                    continue  # No permission to check this process
                except (psutil.NoSuchProcess, AttributeError):
                    continue
                except Exception as e:
                    logger.debug(f"  Error checking process: {e}")
                    continue
            
            logger.info(f"Checked {checked} processes with psutil, found {len(locking_procs)} locking")
            
            if locking_procs:
                processes_list = "\n  • ".join(locking_procs[:10])  # Show max 10
                locking_info_parts.append(f"\n\n⚠ FILES LOCKED BY THESE PROCESSES:\n  • {processes_list}")
            
            # Method 2: Use Windows Handle tool via PowerShell (if available)
            # This works even without admin on newer Windows
            try:
                ps_script = f"""
$path = "{path}"
Get-Process | ForEach-Object {{
    try {{
        $proc = $_
        $proc.Modules | Where-Object {{$_.FileName -like "*$($path.Split('\\')[-1])*"}} | ForEach-Object {{
            Write-Output "$($proc.ProcessName) (PID: $($proc.Id))"
        }}
    }} catch {{}}
}} | Select-Object -First 5 -Unique
"""
                result = subprocess.run(
                    ['powershell', '-NoProfile', '-Command', ps_script],
                    capture_output=True,
                    text=True,
                    timeout=3,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                
                if result.stdout.strip() and not locking_procs:  # Only show if psutil didn't find anything
                    logger.info(f"PowerShell found: {result.stdout.strip()}")
                    locking_info_parts.append(f"\n\n⚠ POSSIBLY LOCKED BY:\n{result.stdout.strip()}")
            except Exception as e:
                logger.debug(f"PowerShell method failed: {e}")
            
            if not locking_info_parts:
                logger.warning("Could not identify any locking processes using available methods")
                # Return helpful tip
                return "\n\n💡 TIP: Open Task Manager and look for processes with files open in this folder."
            
            return "".join(locking_info_parts)
            
        except Exception as e:
            logger.error(f"Error in find_locking_processes: {e}", exc_info=True)
            return ""
    
    def check_automation_studio_running(self) -> List[psutil.Process]:
        """
        Check if any Automation Studio processes are currently running.
        Returns list of running AS processes.
        """
        try:
            logger.info("=== CHECKING FOR AUTOMATION STUDIO PROCESSES ===")
            found: List[psutil.Process] = []
            checked_count = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    checked_count += 1
                    name = (proc.info.get('name') or '').lower()
                    exe = (str(proc.info.get('exe')) if proc.info.get('exe') else '').lower()
                    
                    # Log every process that might be AS
                    if 'automation' in name or 'automation' in exe:
                        logger.info(f"  Process check: PID={proc.pid}, name='{name}', exe='{exe}'")
                    
                    # Check for Automation Studio processes
                    # Note: AS4.5 and AS6 use "pg.exe" as the process name, not "AutomationStudio.exe"
                    # We check for: pg.exe in BR/AS folders
                    # IMPORTANT: Exclude AutomationStudioSelector.exe (our own app!)
                    is_as_process = False
                    
                    # Skip our own selector app
                    if 'automationstudioselector' in name or 'automationstudioselector.exe' in exe:
                        continue
                    
                    if name == 'pg.exe' or exe.endswith('\\pg.exe'):
                        # pg.exe is the actual AS executable - check if it's in a BR/AS path
                        if 'brautomation' in exe or 'automationstudio' in exe or '\\as' in exe or '\\as4' in exe or '\\as6' in exe:
                            is_as_process = True
                    
                    if is_as_process:
                        logger.warning(f"  [FOUND AS] PID={proc.pid}, name='{name}', exe='{exe}'")
                        found.append(proc)
                        if self.session_logger:
                            self.session_logger.log_project_operation(
                                f"Detected AS process",
                                f"PID {proc.pid}: {name}"
                            )
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    continue
            
            logger.info(f"=== PROCESS CHECK COMPLETE: Checked {checked_count} processes, found {len(found)} AS instances ===")
            if self.session_logger:
                self.session_logger.log_project_operation(
                    "AS process check completed",
                    f"Found {len(found)} running instances"
                )
            return found
        except Exception as e:
            logger.error(f"Error checking for AS processes: {e}")
            if self.session_logger:
                self.session_logger.log_error("AS process check failed", e)
            return []
    
    def close_automation_studio_processes(self, processes: List[psutil.Process], timeout_seconds: int = 5) -> None:
        """
        Close the given Automation Studio processes.
        Attempts graceful terminate; escalates to kill if needed. Raises on failure.
        """
        try:
            if not processes:
                logger.info("No processes to close")
                return
            
            logger.info(f"Closing {len(processes)} Automation Studio process(es)")
            if self.session_logger:
                self.session_logger.log_project_operation(
                    "Closing Automation Studio",
                    f"Processes: {[p.pid for p in processes]}"
                )
            
            # Try graceful terminate first
            for p in processes:
                try:
                    logger.info(f"Terminating process PID={p.pid}")
                    p.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    logger.warning(f"Could not terminate PID={p.pid}: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Unexpected error terminating PID={p.pid}: {e}")
                    continue
            
            # Wait for termination
            logger.info(f"Waiting {timeout_seconds}s for processes to close...")
            end_time = time.time() + timeout_seconds
            while time.time() < end_time:
                alive = []
                for p in processes:
                    try:
                        if p.is_running():
                            alive.append(p)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                    except Exception as e:
                        logger.warning(f"Error checking if PID={p.pid} is running: {e}")
                        continue
                if not alive:
                    logger.info("All processes closed successfully")
                    break
                time.sleep(0.2)
            
            # Force kill if still alive
            still_alive = []
            for p in processes:
                try:
                    if p.is_running():
                        still_alive.append(p)
                        logger.info(f"Process PID={p.pid} still alive, will force kill")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                except Exception as e:
                    logger.warning(f"Error checking PID={p.pid}: {e}")
                    continue
            
            if still_alive:
                logger.info(f"Force killing {len(still_alive)} process(es)")
                for p in still_alive:
                    try:
                        logger.info(f"Force killing PID={p.pid}")
                        p.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                        logger.warning(f"Could not kill PID={p.pid}: {e}")
                        continue
                    except Exception as e:
                        logger.error(f"Unexpected error killing PID={p.pid}: {e}")
                        continue
                # brief wait
                time.sleep(0.5)
                
                # Final check
                final_alive = []
                for p in still_alive:
                    try:
                        if p.is_running():
                            final_alive.append(p)
                    except:
                        pass
                still_alive = final_alive
            
            if still_alive:
                pids = [p.pid for p in still_alive]
                message = (
                    "Automation Studio is running and could not be closed automatically. "
                    "Please close Automation Studio manually and try again."
                )
                logger.error(f"AS processes still alive after kill: {pids}")
                if self.session_logger:
                    self.session_logger.log_error(message, Exception(f"PIDs: {pids}"))
                raise ProjectOperationError(message)
            
            logger.info("All Automation Studio processes closed successfully")
            if self.session_logger:
                self.session_logger.log_project_operation("Automation Studio processes closed successfully")
        except ProjectOperationError:
            raise
        except Exception as e:
            message = f"Failed to close Automation Studio processes: {e}"
            logger.error(message, exc_info=True)
            if self.session_logger:
                self.session_logger.log_error(message, e)
            raise ProjectOperationError(message) from e
    
    # ----------------------
    # File operation helpers
    # ----------------------
    def _wait_for_filesystem_sync(self, path: Path, timeout: int = 2) -> None:
        """
        Wait for filesystem operations to complete and ensure all writes are flushed.
        Creates a marker file to force filesystem sync.
        
        Args:
            path: Directory path to sync
            timeout: Additional wait time in seconds after sync marker
        """
        try:
            logger.info(f"Waiting for filesystem sync on {path}")
            
            # Force sync by creating and deleting a marker file
            # This ensures all pending write operations are completed
            sync_marker = path / ".fs_sync_marker"
            sync_marker.write_text("sync", encoding='utf-8')
            sync_marker.unlink()
            
            # Additional wait for filesystem to stabilize
            time.sleep(timeout)
            logger.info(f"Filesystem sync completed for {path}")
            
        except Exception as e:
            logger.warning(f"Sync marker operation failed (non-critical): {e}")
            # Fallback: just wait
            time.sleep(timeout)
    
    def _verify_files_not_locked(self, path: Path, sample_size: int = 5) -> bool:
        """
        Verify that files in the given path are not locked by attempting to open them.
        
        Args:
            path: Directory path to check
            sample_size: Number of files to sample for lock checking
            
        Returns:
            True if files are accessible
            
        Raises:
            ProjectOperationError: If files are locked
        """
        try:
            logger.info(f"Verifying files are not locked in {path}")
            
            # Get a sample of files to check
            all_files = [f for f in path.rglob('*') if f.is_file()]
            
            if not all_files:
                logger.info("No files to verify (directory empty)")
                return True
            
            # Check up to sample_size files
            files_to_check = all_files[:min(sample_size, len(all_files))]
            
            for file_path in files_to_check:
                try:
                    # Try to open file in read mode to check if it's locked
                    with open(file_path, 'rb') as f:
                        # Read a small amount to ensure file is actually accessible
                        f.read(1024)
                    logger.debug(f"  ✓ File accessible: {file_path.name}")
                except PermissionError as e:
                    msg = f"File is locked and cannot be accessed: {file_path}"
                    logger.error(msg)
                    locking_info = self.find_locking_processes(path)
                    raise ProjectOperationError(f"{msg}\n{locking_info}") from e
                except Exception as e:
                    logger.warning(f"  Error checking file {file_path.name}: {e}")
            
            logger.info(f"Verified {len(files_to_check)} files are accessible and not locked")
            return True
            
        except ProjectOperationError:
            raise
        except Exception as e:
            logger.warning(f"File lock verification failed (non-critical): {e}")
            return True  # Don't fail the whole operation for verification issues
    
    def _safe_unlink(self, path: Path, max_retries: int = 5) -> None:
        """Delete a file; retry on transient locks; raise helpful error if locked/in-use."""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                path.unlink()
                if attempt > 0:
                    logger.info(f"Successfully deleted {path} on attempt {attempt + 1}")
                return  # Success
            except PermissionError as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = 1.0 * (2 ** attempt)  # 1s, 2s, 4s, 8s, 16s
                    logger.warning(f"Attempt {attempt + 1}/{max_retries}: Cannot delete {path}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    msg = (
                        f"Cannot delete file: {path}. The file is in use or locked by another application. "
                        "Please ensure Automation Studio is closed and try again."
                    )
                    logger.error(msg)
                    if self.session_logger:
                        self.session_logger.log_error(msg, e)
                    raise ProjectOperationError(msg) from e
            except OSError as e:
                last_error = e
                if getattr(e, 'winerror', None) == 32:  # ERROR_SHARING_VIOLATION
                    if attempt < max_retries - 1:
                        wait_time = 1.0 * (2 ** attempt)  # 1s, 2s, 4s, 8s, 16s
                        logger.warning(f"Attempt {attempt + 1}/{max_retries}: File sharing violation on {path}, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        msg = (
                            f"Cannot delete file: {path}. The file is currently in use. "
                            "Close Automation Studio or any program using the file and retry."
                        )
                        logger.error(msg)
                        if self.session_logger:
                            self.session_logger.log_error(msg, e)
                        raise ProjectOperationError(msg) from e
                else:
                    raise
    
    def _safe_rmtree(self, path: Path, max_retries: int = 5) -> None:
        """Recursively delete a directory; retry on transient locks; raise helpful error if locked/in-use."""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                shutil.rmtree(path)
                if attempt > 0:
                    logger.info(f"Successfully deleted {path} on attempt {attempt + 1}")
                    if self.session_logger:
                        self.session_logger.log_file_operation("Directory deleted (after retry)", str(path))
                return  # Success
            except PermissionError as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = 1.0 * (2 ** attempt)  # 1s, 2s, 4s, 8s, 16s
                    logger.warning(f"Attempt {attempt + 1}/{max_retries}: Cannot delete {path}, retrying in {wait_time}s...")
                    if self.session_logger:
                        self.session_logger.log_file_operation(f"Retry {attempt + 1}/{max_retries}", f"Waiting {wait_time}s")
                    time.sleep(wait_time)
                else:
                    # Try to find what's locking it
                    locking_info = self.find_locking_processes(path)
                    
                    # Check for common antivirus processes
                    antivirus_hint = self._check_antivirus_running()
                    
                    msg = (
                        f"Cannot delete directory: {path}\n\n"
                        f"One or more items are in use or locked by another application.\n"
                        "This could be caused by:\n"
                        "• Automation Studio still running (check Task Manager for pg.exe)\n"
                        "• Windows Explorer viewing the folder\n"
                        "• Antivirus/Windows Defender scanning the files\n"
                        "• File indexing service (SearchIndexer)\n"
                        f"{antivirus_hint}"
                        f"{locking_info}\n\n"
                        "Please try:\n"
                        "1. Wait a moment and click Prepare again\n"
                        "2. Temporarily disable antivirus real-time protection\n"
                        "3. Close Windows Explorer in this folder\n"
                        "4. Check Task Manager for any processes using the files"
                    )
                    logger.error(msg)
                    if self.session_logger:
                        self.session_logger.log_error(msg, e)
                    raise ProjectOperationError(msg) from e
            except OSError as e:
                last_error = e
                if getattr(e, 'winerror', None) == 32:  # ERROR_SHARING_VIOLATION
                    if attempt < max_retries - 1:
                        wait_time = 1.0 * (2 ** attempt)  # 1s, 2s, 4s, 8s, 16s
                        logger.warning(f"Attempt {attempt + 1}/{max_retries}: File sharing violation on {path}, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        msg = (
                            f"Cannot delete directory: {path}. Files appear to be in use. "
                            "Close Automation Studio, Windows Explorer, or any program using the Libraries and retry."
                        )
                        logger.error(msg)
                        if self.session_logger:
                            self.session_logger.log_error(msg, e)
                        raise ProjectOperationError(msg) from e
                else:
                    raise
    
    def validate_project_structure(self, project_root: Path) -> bool:
        """
        Validate that the project has the expected directory structure.
        
        Args:
            project_root: Root path of the project
            
        Returns:
            True if structure is valid
            
        Raises:
            ProjectOperationError: If structure is invalid
        """
        try:
            paths = ProjectPaths.from_root(project_root)
            
            # Check required directories exist
            if not paths.logical_path.exists():
                raise ProjectOperationError(f"Logical directory not found: {paths.logical_path}")
            
            if not paths.physical_path.exists():
                raise ProjectOperationError(f"Physical directory not found: {paths.physical_path}")
            
            logger.info(f"Project structure validated: {project_root}")
            return True
            
        except Exception as e:
            error_msg = f"Project structure validation failed: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            raise ProjectOperationError(error_msg) from e
    
    def clear_build_artifacts(self, project_root: Path) -> bool:
        """
        Clear all build artifacts that could cause cache mismatches.
        CRITICAL: Must be called after changing libraries/configuration to prevent corruption.
        
        This removes:
        - Temp/ - Build cache, object files, intermediate artifacts
        - Binaries/ - Compiled binaries from previous builds
        - _BRDYN/ - B&R dynamic loader artifacts
        - Diagnosis/ - Diagnostic data from previous runs
        - *.bak, *.tmp, *.$$$ - Backup and temporary files
        
        Args:
            project_root: Root path of the project
            
        Returns:
            True if successful
        """
        try:
            logger.info("=" * 60)
            logger.info("CLEARING BUILD ARTIFACTS TO PREVENT CACHE CORRUPTION")
            logger.info("=" * 60)
            
            # Directories to clear (these contain version-specific build cache)
            artifacts_to_clear = [
                ("Temp", True),        # Build cache - RECREATE after clearing
                ("Binaries", False),   # Compiled binaries - don't recreate
                ("_BRDYN", False),     # B&R dynamic artifacts - don't recreate
                ("Diagnosis", False),  # Diagnostic data - don't recreate
            ]
            
            cleared_count = 0
            
            for dir_name, recreate in artifacts_to_clear:
                artifact_dir = project_root / dir_name
                
                if artifact_dir.exists():
                    try:
                        logger.info(f"Clearing {dir_name}/ directory...")
                        self._safe_rmtree(artifact_dir)
                        logger.info(f"✓ Cleared: {dir_name}/")
                        self.session_logger.log_file_operation(f"Build artifacts cleared", str(artifact_dir))
                        cleared_count += 1
                        
                        # Recreate Temp/ (AS expects it to exist)
                        if recreate:
                            artifact_dir.mkdir(parents=True, exist_ok=True)
                            logger.info(f"✓ Recreated empty {dir_name}/ folder")
                            self.session_logger.log_file_operation(f"Directory recreated", str(artifact_dir))
                            
                    except Exception as e:
                        logger.warning(f"Could not clear {dir_name}/: {e}")
                        # Non-critical - continue with other artifacts
                else:
                    logger.debug(f"{dir_name}/ does not exist (skipping)")
            
            # Clear backup and temporary files throughout the project
            logger.info("Clearing backup and temporary files...")
            backup_patterns = ["*.bak", "*.tmp", "*.$$$"]
            backup_count = 0
            
            for pattern in backup_patterns:
                for backup_file in project_root.rglob(pattern):
                    try:
                        self._safe_unlink(backup_file)
                        logger.debug(f"Deleted: {backup_file.relative_to(project_root)}")
                        backup_count += 1
                    except Exception as e:
                        logger.debug(f"Could not delete {backup_file.name}: {e}")
                        # Non-critical - continue with other files
            
            if backup_count > 0:
                logger.info(f"✓ Cleared {backup_count} backup/temp files")
            
            logger.info("=" * 60)
            logger.info(f"BUILD ARTIFACTS CLEANUP COMPLETE ({cleared_count} directories cleared)")
            logger.info("=" * 60)
            
            self.session_logger.log_project_operation(
                "Build artifacts cleared",
                f"{cleared_count} directories, {backup_count} temp files"
            )
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to clear build artifacts: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            # Don't raise - this is important but not critical enough to fail the whole operation
            logger.warning("Continuing despite build artifact cleanup failure...")
            return False
    
    def clear_libraries_directory(self, project_root: Path) -> bool:
        """
        Clear all contents from the Libraries directory.
        
        Args:
            project_root: Root path of the project
            
        Returns:
            True if successful
        """
        try:
            paths = ProjectPaths.from_root(project_root)
            
            if paths.libraries_path.exists():
                # Remove all contents
                for item in paths.libraries_path.iterdir():
                    if item.is_dir():
                        self._safe_rmtree(item)
                        self.session_logger.log_file_operation("Directory deleted", str(item))
                    else:
                        self._safe_unlink(item)
                        self.session_logger.log_file_operation("File deleted", str(item))
                
                logger.info(f"Libraries directory cleared: {paths.libraries_path}")
                self.session_logger.log_project_operation("Libraries directory cleared")
                return True
            else:
                # Create the directory if it doesn't exist
                paths.libraries_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Libraries directory created: {paths.libraries_path}")
                return True
                
        except Exception as e:
            error_msg = f"Failed to clear Libraries directory: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            raise ProjectOperationError(error_msg) from e
    
    def copy_libraries_for_version(self, project_root: Path, studio: AutomationStudio) -> bool:
        """
        Copy libraries from version-specific directory to Libraries directory.
        
        Args:
            project_root: Root path of the project
            studio: Automation studio configuration
            
        Returns:
            True if successful
        """
        try:
            paths = ProjectPaths.from_root(project_root)
            source_dir = paths.logical_path / f"Libraries_{studio.libraries_suffix}"
            target_dir = paths.libraries_path
            
            if not source_dir.exists():
                raise ProjectOperationError(f"Source libraries directory not found: {source_dir}")
            
            # Ensure target directory exists and is empty
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all contents from source to target
            copied_items = 0
            for item in source_dir.iterdir():
                if item.is_dir():
                    target_item = target_dir / item.name
                    if target_item.exists():
                        self._safe_rmtree(target_item)
                    shutil.copytree(item, target_item)
                    self.session_logger.log_file_operation("Directory copied", str(item), str(target_item))
                    copied_items += 1
                else:
                    target_item = target_dir / item.name
                    shutil.copy2(item, target_item)
                    self.session_logger.log_file_operation("File copied", str(item), str(target_item))
                    copied_items += 1
            
            logger.info(f"Libraries copied from {source_dir} to {target_dir}")
            self.session_logger.log_project_operation(
                f"Libraries copied for {studio.display_name}",
                f"From: {source_dir} To: {target_dir}"
            )
            
            # VERIFICATION: Count files to ensure complete copy
            logger.info("Verifying library copy completeness...")
            source_files = [f for f in source_dir.rglob('*') if f.is_file()]
            target_files = [f for f in target_dir.rglob('*') if f.is_file()]
            
            if len(source_files) != len(target_files):
                raise ProjectOperationError(
                    f"Library copy verification FAILED!\n"
                    f"Source has {len(source_files)} files, but target has {len(target_files)} files.\n"
                    f"The copy operation may have been interrupted."
                )
            
            logger.info(f"✓ Verification passed: {len(target_files)} files copied successfully")
            self.session_logger.log_project_operation(
                "Library copy verified",
                f"{len(target_files)} files"
            )
            
            # FILESYSTEM SYNC: Wait for all write operations to complete
            logger.info("Waiting for filesystem to flush all write operations...")
            self._wait_for_filesystem_sync(target_dir, timeout=3)
            
            # LOCK CHECK: Verify files are accessible and not locked
            logger.info("Verifying files are not locked...")
            self._verify_files_not_locked(target_dir, sample_size=10)
            
            logger.info("✓ All library files are accessible and ready")
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to copy libraries: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            raise ProjectOperationError(error_msg) from e
    
    def update_physical_pkg(self, project_root: Path, studio: AutomationStudio) -> bool:
        """
        Update Physical.pkg file based on selected automation studio version.
        
        Args:
            project_root: Root path of the project
            studio: Automation studio configuration
            
        Returns:
            True if successful
        """
        try:
            paths = ProjectPaths.from_root(project_root)
            target_file = paths.physical_path / "Physical.pkg"
            source_file = paths.physical_path / f"Physical_{studio.physical_pkg_suffix}.pkg"
            
            if not source_file.exists():
                raise ProjectOperationError(f"Source Physical.pkg not found: {source_file}")
            
            # Remove existing Physical.pkg if it exists
            if target_file.exists():
                self._safe_unlink(target_file)
                self.session_logger.log_file_operation("File deleted", str(target_file))
            
            # Copy version-specific file to Physical.pkg
            shutil.copy2(source_file, target_file)
            
            logger.info(f"Physical.pkg updated from {source_file}")
            self.session_logger.log_file_operation("File copied", str(source_file), str(target_file))
            self.session_logger.log_project_operation(
                f"Physical.pkg updated for {studio.display_name}"
            )
            
            # Wait for filesystem to ensure file is fully written
            self._wait_for_filesystem_sync(paths.physical_path, timeout=1)
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to update Physical.pkg: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            raise ProjectOperationError(error_msg) from e
    
    def update_project_file(self, project_root: Path, studio: AutomationStudio) -> bool:
        """
        Update the main project file (OCB.apj) based on selected automation studio version.
        
        Args:
            project_root: Root path of the project
            studio: Automation studio configuration
            
        Returns:
            True if successful
        """
        try:
            target_file = project_root / "OCB.apj"
            source_file = project_root / f"OCB_as{studio.project_file_suffix}.apj"
            
            if not source_file.exists():
                raise ProjectOperationError(f"Source project file not found: {source_file}")
            
            # Remove existing OCB.apj if it exists
            if target_file.exists():
                self._safe_unlink(target_file)
                self.session_logger.log_file_operation("File deleted", str(target_file))
            
            # Copy version-specific file to OCB.apj
            shutil.copy2(source_file, target_file)
            
            # Verify the copy was successful
            if not target_file.exists():
                raise ProjectOperationError(f"Failed to create target file: {target_file}")
            
            # Verify file size matches
            source_size = source_file.stat().st_size
            target_size = target_file.stat().st_size
            if source_size != target_size:
                raise ProjectOperationError(f"File size mismatch after copy: source={source_size}, target={target_size}")
            
            logger.info(f"Project file updated from {source_file} (size: {source_size} bytes)")
            self.session_logger.log_file_operation("File copied", str(source_file), str(target_file))
            self.session_logger.log_project_operation(
                f"Project file updated for {studio.display_name}"
            )
            
            # Wait for filesystem to ensure file is fully written and ready to open
            logger.info("Ensuring project file is fully written to disk...")
            self._wait_for_filesystem_sync(project_root, timeout=2)
            
            # Verify the file is not locked
            logger.info("Verifying project file is accessible...")
            try:
                with open(target_file, 'rb') as f:
                    f.read(1024)  # Read first 1KB to ensure file is accessible
                logger.info("✓ Project file is ready")
            except Exception as e:
                logger.warning(f"Project file verification warning: {e}")
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to update project file: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            raise ProjectOperationError(error_msg) from e

    def open_project_file(self, project_root: Path, studio: AutomationStudio) -> bool:
        """
        Open the main project file (OCB.apj) with the selected automation studio.
        
        Args:
            project_root: Root path of the project
            studio: Automation studio configuration
            
        Returns:
            True if successful
        """
        try:
            project_file = project_root / "OCB.apj"
            
            if not project_file.exists():
                raise ProjectOperationError(f"Project file not found: {project_file}")
            
            if not studio.executable_path.exists():
                raise ProjectOperationError(f"Automation Studio executable not found: {studio.executable_path}")
            
            # Import subprocess here to avoid issues if not needed
            import subprocess
            
            # Open the project file with the automation studio
            subprocess.Popen([str(studio.executable_path), str(project_file)])
            
            logger.info(f"Project opened: {project_file} with {studio.display_name}")
            self.session_logger.log_project_operation(
                f"Project opened with {studio.display_name}",
                f"File: {project_file}"
            )
            return True
            
        except Exception as e:
            error_msg = f"Failed to open project: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            raise ProjectOperationError(error_msg) from e
    
    def prepare_project_without_launch(self, project_root: Path, studio: AutomationStudio) -> bool:
        """
        Prepare project files without launching Automation Studio.
        
        Args:
            project_root: Root path of the project
            studio: Automation studio configuration
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Preparing project for {studio.display_name} (no launch)")
            self.session_logger.log_studio_selection(studio.name, studio.version.value)
            
            # Step 1: Validate project structure
            self.validate_project_structure(project_root)
            
            # Step 2: Clear Libraries directory
            self.clear_libraries_directory(project_root)
            
            # Step 3: Copy version-specific libraries
            self.copy_libraries_for_version(project_root, studio)
            
            # Step 4: Update Physical.pkg
            self.update_physical_pkg(project_root, studio)
            
            # Step 5: Update project file (OCB.apj)
            self.update_project_file(project_root, studio)
            
            # Step 6: Clear build artifacts (CRITICAL - prevents cache corruption)
            self.clear_build_artifacts(project_root)
            
            # Step 7: Final filesystem sync to ensure Temp/ recreation is written
            self._wait_for_filesystem_sync(project_root, timeout=1)
            
            logger.info(f"Project prepared successfully for {studio.display_name}")
            self.session_logger.log_project_operation("Project prepared successfully (no launch)")
            
            return True
            
        except Exception as e:
            error_msg = f"Project preparation failed: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            return False
    
    def execute_full_project_setup(self, project_root: Path, studio: AutomationStudio) -> bool:
        """
        Execute the complete project setup process for the selected studio.
        
        Args:
            project_root: Root path of the project
            studio: Automation studio configuration
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Starting project setup for {studio.display_name}")
            self.session_logger.log_studio_selection(studio.name, studio.version.value)
            
            # Step 1: Validate project structure
            self.validate_project_structure(project_root)
            
            # Step 2: Clear Libraries directory
            self.clear_libraries_directory(project_root)
            
            # Step 3: Copy version-specific libraries
            self.copy_libraries_for_version(project_root, studio)
            
            # Step 4: Update Physical.pkg
            self.update_physical_pkg(project_root, studio)
            
            # Step 5: Update project file (OCB.apj)
            self.update_project_file(project_root, studio)
            
            # Step 6: Clear build artifacts (CRITICAL - prevents cache corruption)
            self.clear_build_artifacts(project_root)
            
            # Step 7: Final filesystem sync to ensure Temp/ recreation is written
            self._wait_for_filesystem_sync(project_root, timeout=1)
            
            # Step 8: Open project file
            self.open_project_file(project_root, studio)
            
            logger.info(f"Project setup completed successfully for {studio.display_name}")
            self.session_logger.log_project_operation("Project setup completed successfully")
            
            return True
            
        except Exception as e:
            error_msg = f"Project setup failed: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            return False
