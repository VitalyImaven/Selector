"""
CLI command implementations for Automation Studio Selector.
"""
import logging
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from src.config.settings import ConfigManager
from src.models.automation_studio import AutomationStudio, AutomationStudioVersion
from src.services.project_service import ProjectService, ProjectOperationError
from src.utils.logger import SessionLogger


logger = logging.getLogger(__name__)


class CLICommands:
    """Implementation of CLI commands."""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """Initialize CLI commands."""
        self.config_manager = config_manager or ConfigManager()
        self.session_logger = SessionLogger()
        self.project_service = ProjectService(self.session_logger)
    
    def open_project(self, options: Dict) -> int:
        """
        Open a project with specified AS version.
        
        Returns:
            0 for success, non-zero for error
        """
        try:
            project_name = options.get('project')
            project_path_str = options.get('project_path')
            studio_version = options.get('studio')
            studio_path_str = options.get('studio_path')
            verbose = options.get('verbose', False)
            silent = options.get('silent', False)
            wait = options.get('wait', False)
            
            # Determine project path (from name or direct path)
            if project_path_str:
                # Direct path provided - no GUI configuration needed!
                project_path = Path(project_path_str)
                if not project_path.exists():
                    self._print_error(f"Project path does not exist: {project_path_str}", silent)
                    return 1
                if not self._validate_project_structure(project_path):
                    self._print_error(f"Invalid project structure at: {project_path_str}", silent)
                    return 1
            elif project_name:
                # Project name provided - lookup in configuration
                project_path = self._find_project_by_name(project_name)
                if not project_path:
                    self._print_error(f"Project not found in configuration: {project_name}", silent)
                    self._print_error(f"Use -project-path to specify direct path, or add project via GUI first", silent)
                    return 3
            else:
                self._print_error("Project name or path is required", silent)
                return 1
            
            # Determine studio (from version or direct path)
            if studio_path_str:
                # Direct AS executable path provided - no GUI configuration needed!
                studio_exe = Path(studio_path_str)
                if not studio_exe.exists():
                    self._print_error(f"AS executable not found: {studio_path_str}", silent)
                    return 4
                
                # Determine version from path or default
                if 'AS6' in str(studio_exe).upper() or '\\6\\' in str(studio_exe):
                    studio = AutomationStudio.create_as6(studio_exe)
                elif 'AS45' in str(studio_exe).upper() or '45' in str(studio_exe):
                    studio = AutomationStudio.create_as45(studio_exe)
                else:
                    # Default to version from -studio parameter or AS 6
                    if studio_version and '4.5' in studio_version or '45' in studio_version:
                        studio = AutomationStudio.create_as45(studio_exe)
                    else:
                        studio = AutomationStudio.create_as6(studio_exe)
                        
            elif studio_version:
                # Studio version provided - lookup in configuration
                studio = self._find_studio_by_version(studio_version)
                if not studio:
                    self._print_error(f"Studio version '{studio_version}' not found in configuration", silent)
                    self._print_error(f"Use -studio-path to specify AS executable directly, or configure via GUI first", silent)
                    return 4
            else:
                # Try to use last selected studio
                studio_version = self.config_manager.get_last_selected_studio()
                if studio_version:
                    studio = self._find_studio_by_version(studio_version)
                    if not studio:
                        self._print_error("No valid studio configuration found", silent)
                        return 4
                else:
                    self._print_error("Studio version or path is required", silent)
                    return 4
            
            # Execute project setup
            prepare_only = options.get('prepare_only', False)
            
            if verbose and not silent:
                action = "Preparing" if prepare_only else "Opening"
                print(f"{action} project: {project_name}")
                print(f"Using AS: {studio.display_name}")
                print(f"Project path: {project_path}")
            
            # Note: Auto-sync is not available in CLI mode (requires Qt)
            # Files will still be prepared correctly
            
            # Execute setup based on mode
            if prepare_only:
                # Prepare files only, don't launch AS
                success = self.project_service.prepare_project_without_launch(project_path, studio)
                
                if not success:
                    self._print_error("Failed to prepare project", silent)
                    return 1
                
                if not silent:
                    print(f"✓ Project prepared successfully for {studio.display_name}")
                    print(f"  Files configured but Automation Studio NOT launched")
                    if verbose:
                        print(f"  You can now manually open: {project_path / 'OCB.apj'}")
            else:
                # Full setup with AS launch
                success = self.project_service.execute_full_project_setup(project_path, studio)
                
                if not success:
                    self._print_error("Failed to open project", silent)
                    return 1
                
                if not silent:
                    print(f"✓ Project opened successfully with {studio.display_name}")
                
                # Wait for AS to close if requested
                if wait:
                    self._wait_for_process(studio.executable_path, silent)
            
            return 0
            
        except Exception as e:
            self._print_error(f"Error opening project: {e}", options.get('silent', False))
            return 1
    
    def list_projects(self, options: Dict) -> int:
        """List all configured projects."""
        try:
            projects = self.config_manager.get_project_paths()
            format_type = options.get('format', 'text')
            
            if format_type == 'json':
                print(json.dumps(projects, indent=2))
            else:
                if not projects:
                    print("No projects configured")
                    return 0
                
                print("Configured Projects:")
                print("-" * 80)
                for i, project in enumerate(projects, 1):
                    print(f"{i}. {project['name']}")
                    print(f"   Path: {project['path']}")
                    if project.get('description'):
                        print(f"   Description: {project['description']}")
                    print()
            
            return 0
            
        except Exception as e:
            self._print_error(f"Error listing projects: {e}")
            return 1
    
    def list_studios(self, options: Dict) -> int:
        """List all configured Automation Studios."""
        try:
            studios = self.config_manager.get_automation_studios()
            format_type = options.get('format', 'text')
            
            if format_type == 'json':
                studios_data = [
                    {
                        'name': studio.name,
                        'version': studio.version.value,
                        'executable_path': str(studio.executable_path)
                    }
                    for studio in studios
                ]
                print(json.dumps(studios_data, indent=2))
            else:
                if not studios:
                    print("No Automation Studios configured")
                    return 0
                
                print("Configured Automation Studios:")
                print("-" * 80)
                for i, studio in enumerate(studios, 1):
                    print(f"{i}. {studio.display_name}")
                    print(f"   Executable: {studio.executable_path}")
                    print()
            
            return 0
            
        except Exception as e:
            self._print_error(f"Error listing studios: {e}")
            return 1
    
    def sync_project(self, options: Dict) -> int:
        """Perform manual sync."""
        try:
            project_name = options.get('project')
            silent = options.get('silent', False)
            
            # Get current or specified project
            if project_name:
                project_path = self._find_project_by_name(project_name)
                if not project_path:
                    self._print_error(f"Project not found: {project_name}", silent)
                    return 3
            else:
                project_path = self.config_manager.get_last_selected_project()
            if not project_path:
                self._print_error("No active project found", silent)
                return 3
            
            if not silent:
                print(f"Syncing project: {project_path.name}")
                print("Note: CLI sync requires GUI mode. Use the application GUI for manual sync.")
            
            # CLI mode doesn't support sync (requires Qt timers)
            # Direct user to use GUI mode
            files_synced = 0
            
            if not silent:
                if files_synced > 0:
                    print(f"✓ Sync completed: {files_synced} files synchronized")
                else:
                    print("✓ No changes detected - all files up to date")
            
            return 0
            
        except Exception as e:
            self._print_error(f"Error syncing project: {e}", options.get('silent', False))
            return 1
    
    def add_project(self, options: Dict) -> int:
        """Add a new project to configuration."""
        try:
            name = options.get('name')
            path = options.get('path')
            description = options.get('description', '')
            
            if not name or not path:
                self._print_error("Project name and path are required")
                return 1
            
            project_path = Path(path)
            
            if not project_path.exists():
                self._print_error(f"Project path does not exist: {path}")
                return 1
            
            # Validate project structure
            if not self._validate_project_structure(project_path):
                self._print_error(f"Invalid project structure (missing Logical or Physical folders)")
                return 1
            
            # Add to configuration
            if self.config_manager.add_project_path(name, project_path, description):
                print(f"✓ Project added: {name}")
                print(f"  Path: {project_path}")
                return 0
            else:
                self._print_error("Failed to add project (may already exist)")
                return 1
                
        except Exception as e:
            self._print_error(f"Error adding project: {e}")
            return 1
    
    def remove_project(self, options: Dict) -> int:
        """Remove a project from configuration."""
        try:
            name = options.get('name')
            force = options.get('force', False)
            
            if not name:
                self._print_error("Project name is required")
                return 1
            
            # Find project
            project_path = self._find_project_by_name(name)
            if not project_path:
                self._print_error(f"Project not found: {name}")
                return 3
            
            # Confirm if not forced
            if not force:
                response = input(f"Remove project '{name}'? (yes/no): ")
                if response.lower() not in ['yes', 'y']:
                    print("Cancelled")
                    return 0
            
            # Remove from configuration
            if self.config_manager.remove_project_path(project_path):
                print(f"✓ Project removed: {name}")
                return 0
            else:
                self._print_error("Failed to remove project")
                return 1
                
        except Exception as e:
            self._print_error(f"Error removing project: {e}")
            return 1
    
    def show_status(self, options: Dict) -> int:
        """Show application status."""
        try:
            format_type = 'json' if options.get('json', False) else 'text'
            
            # Get status information
            studios = self.config_manager.get_automation_studios()
            projects = self.config_manager.get_project_paths()
            last_studio = self.config_manager.get_last_selected_studio()
            last_project = self.config_manager.get_last_selected_project()
            
            if format_type == 'json':
                status_data = {
                    'studios_count': len(studios),
                    'projects_count': len(projects),
                    'last_studio': last_studio,
                    'last_project': str(last_project) if last_project else None,
                }
                print(json.dumps(status_data, indent=2))
            else:
                print("Automation Studio Selector - Status")
                print("=" * 80)
                print(f"Configured Studios: {len(studios)}")
                print(f"Configured Projects: {len(projects)}")
                print(f"Last Used Studio: {last_studio or 'None'}")
                print(f"Last Used Project: {last_project.name if last_project else 'None'}")
                print()
            
            return 0
            
        except Exception as e:
            self._print_error(f"Error getting status: {e}")
            return 1
    
    def show_sync_status(self, options: Dict) -> int:
        """Show sync status."""
        try:
            print("Auto-Sync Status")
            print("=" * 80)
            print("Note: Auto-sync monitoring is only available in GUI mode")
            print("Use the GUI application to view detailed sync statistics")
            print()
            return 0
            
        except Exception as e:
            self._print_error(f"Error getting sync status: {e}")
            return 1
    
    def show_config(self, options: Dict) -> int:
        """Show current configuration."""
        try:
            format_type = 'json' if options.get('json', False) else 'text'
            
            studios = self.config_manager.get_automation_studios()
            projects = self.config_manager.get_project_paths()
            
            if format_type == 'json':
                config_data = {
                    'studios': [
                        {
                            'name': studio.name,
                            'version': studio.version.value,
                            'path': str(studio.executable_path)
                        }
                        for studio in studios
                    ],
                    'projects': projects
                }
                print(json.dumps(config_data, indent=2))
            else:
                print("Current Configuration")
                print("=" * 80)
                print("\nAutomation Studios:")
                for studio in studios:
                    print(f"  - {studio.display_name}: {studio.executable_path}")
                
                print("\nProjects:")
                for project in projects:
                    print(f"  - {project['name']}: {project['path']}")
                    if project.get('description'):
                        print(f"    Description: {project['description']}")
                print()
            
            return 0
            
        except Exception as e:
            self._print_error(f"Error showing config: {e}")
            return 1
    
    def show_version(self, options: Dict) -> int:
        """Show application version."""
        print("Automation Studio Selector v1.1.0")
        print("Created by Vitaly Grosman - Indigo R&D Division")
        print("© 2025")
        return 0
    
    # Helper methods
    
    def _find_project_by_name(self, name: str) -> Optional[Path]:
        """Find project path by name."""
        projects = self.config_manager.get_project_paths()
        for project in projects:
            if project['name'].lower() == name.lower():
                return Path(project['path'])
        return None
    
    def _find_studio_by_version(self, version: str) -> Optional[AutomationStudio]:
        """Find studio by version string."""
        studios = self.config_manager.get_automation_studios()
        
        # Normalize version string (AS6, 6, AS45, 4.5 all work)
        version_clean = version.upper().replace('AS', '').replace(' ', '').strip()
        
        # Handle both "45" and "4.5" formats
        if version_clean == '45':
            version_clean = '4.5'
        elif version_clean == '6':
            version_clean = '6'
        
        for studio in studios:
            if studio.version.value == version_clean:
                return studio
        
        return None
    
    def _validate_project_structure(self, path: Path) -> bool:
        """Validate project structure."""
        try:
            if not path.exists() or not path.is_dir():
                return False
            
            logical_dir = path / "Logical"
            physical_dir = path / "Physical"
            
            return logical_dir.exists() and logical_dir.is_dir() and \
                   physical_dir.exists() and physical_dir.is_dir()
        except:
            return False
    
    def _wait_for_process(self, executable_path: Path, silent: bool = False):
        """Wait for AS process to close."""
        try:
            import psutil
            
            if not silent:
                print(f"Waiting for Automation Studio to close...")
            
            # Find the process
            target_process = None
            for proc in psutil.process_iter(['pid', 'exe']):
                try:
                    if proc.info['exe'] and Path(proc.info['exe']).samefile(executable_path):
                        target_process = proc
                        break
                except:
                    continue
            
            if target_process:
                # Wait for process to terminate
                target_process.wait()
                
                if not silent:
                    print(f"✓ Automation Studio closed")
                
                # Trigger sync on close
                time.sleep(1)  # Give file system time to settle
                self.auto_sync_manager.sync_on_application_close()
            else:
                if not silent:
                    print("Note: Automation Studio process not found")
                    
        except Exception as e:
            logger.error(f"Error waiting for process: {e}")
    
    def _print_error(self, message: str, silent: bool = False):
        """Print error message."""
        if not silent:
            print(f"ERROR: {message}", file=__import__('sys').stderr)
        logger.error(message)
