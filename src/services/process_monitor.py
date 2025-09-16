"""
Process monitoring service for Automation Studio instances.
"""
import logging
import psutil
import time
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class ProcessInfo:
    """Information about a monitored process."""
    pid: int
    executable_path: Path
    start_time: float
    
    def is_running(self) -> bool:
        """Check if the process is still running."""
        try:
            process = psutil.Process(self.pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False


class ProcessMonitor:
    """Monitor Automation Studio processes."""
    
    def __init__(self):
        """Initialize process monitor."""
        self._monitored_processes: Dict[int, ProcessInfo] = {}
        self._executable_paths: List[Path] = []
    
    def add_executable_path(self, executable_path: Path):
        """Add an executable path to monitor."""
        if executable_path not in self._executable_paths:
            self._executable_paths.append(executable_path)
            logger.info(f"Added executable to monitor: {executable_path}")
    
    def remove_executable_path(self, executable_path: Path):
        """Remove an executable path from monitoring."""
        if executable_path in self._executable_paths:
            self._executable_paths.remove(executable_path)
            logger.info(f"Removed executable from monitor: {executable_path}")
    
    def scan_for_processes(self) -> List[ProcessInfo]:
        """Scan for new instances of monitored executables."""
        new_processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'exe', 'create_time']):
                try:
                    proc_info = proc.info
                    if proc_info['exe']:
                        exe_path = Path(proc_info['exe'])
                        
                        # Check if this executable is one we're monitoring
                        for monitored_path in self._executable_paths:
                            if exe_path.samefile(monitored_path):
                                pid = proc_info['pid']
                                
                                # Check if we're not already monitoring this process
                                if pid not in self._monitored_processes:
                                    process_info = ProcessInfo(
                                        pid=pid,
                                        executable_path=exe_path,
                                        start_time=proc_info['create_time']
                                    )
                                    
                                    self._monitored_processes[pid] = process_info
                                    new_processes.append(process_info)
                                    logger.info(f"Detected new AS process: PID {pid}")
                                
                                break
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                    continue
                    
        except Exception as e:
            logger.error(f"Error scanning for processes: {e}")
        
        return new_processes
    
    def check_for_closed_processes(self) -> List[ProcessInfo]:
        """Check for processes that have closed since last check."""
        closed_processes = []
        pids_to_remove = []
        
        for pid, process_info in self._monitored_processes.items():
            if not process_info.is_running():
                closed_processes.append(process_info)
                pids_to_remove.append(pid)
                logger.info(f"Detected closed AS process: PID {pid}")
        
        # Remove closed processes from monitoring
        for pid in pids_to_remove:
            del self._monitored_processes[pid]
        
        return closed_processes
    
    def get_running_processes(self) -> List[ProcessInfo]:
        """Get list of currently running monitored processes."""
        return list(self._monitored_processes.values())
    
    def is_any_process_running(self) -> bool:
        """Check if any monitored process is currently running."""
        # Clean up closed processes first
        self.check_for_closed_processes()
        return len(self._monitored_processes) > 0
    
    def get_process_by_executable(self, executable_path: Path) -> Optional[ProcessInfo]:
        """Get running process info for a specific executable."""
        for process_info in self._monitored_processes.values():
            try:
                if process_info.executable_path.samefile(executable_path):
                    if process_info.is_running():
                        return process_info
            except OSError:
                continue
        return None
    
    def stop_monitoring(self):
        """Stop monitoring all processes."""
        self._monitored_processes.clear()
        self._executable_paths.clear()
        logger.info("Process monitoring stopped")
    
    def get_process_uptime(self, pid: int) -> Optional[float]:
        """Get uptime of a process in seconds."""
        if pid in self._monitored_processes:
            process_info = self._monitored_processes[pid]
            if process_info.is_running():
                return time.time() - process_info.start_time
        return None
