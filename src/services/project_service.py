"""
Business logic for project operations and file management.
"""
import shutil
import logging
from pathlib import Path
from typing import Optional, List
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
                        shutil.rmtree(item)
                        self.session_logger.log_file_operation("Directory deleted", str(item))
                    else:
                        item.unlink()
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
            for item in source_dir.iterdir():
                if item.is_dir():
                    target_item = target_dir / item.name
                    if target_item.exists():
                        shutil.rmtree(target_item)
                    shutil.copytree(item, target_item)
                    self.session_logger.log_file_operation("Directory copied", str(item), str(target_item))
                else:
                    target_item = target_dir / item.name
                    shutil.copy2(item, target_item)
                    self.session_logger.log_file_operation("File copied", str(item), str(target_item))
            
            logger.info(f"Libraries copied from {source_dir} to {target_dir}")
            self.session_logger.log_project_operation(
                f"Libraries copied for {studio.display_name}",
                f"From: {source_dir} To: {target_dir}"
            )
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
                target_file.unlink()
                self.session_logger.log_file_operation("File deleted", str(target_file))
            
            # Copy version-specific file to Physical.pkg
            shutil.copy2(source_file, target_file)
            
            logger.info(f"Physical.pkg updated from {source_file}")
            self.session_logger.log_file_operation("File copied", str(source_file), str(target_file))
            self.session_logger.log_project_operation(
                f"Physical.pkg updated for {studio.display_name}"
            )
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
                target_file.unlink()
                self.session_logger.log_file_operation("File deleted", str(target_file))
            
            # Copy version-specific file to OCB.apj
            shutil.copy2(source_file, target_file)
            
            logger.info(f"Project file updated from {source_file}")
            self.session_logger.log_file_operation("File copied", str(source_file), str(target_file))
            self.session_logger.log_project_operation(
                f"Project file updated for {studio.display_name}"
            )
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
            
            # Step 6: Open project file
            self.open_project_file(project_root, studio)
            
            logger.info(f"Project setup completed successfully for {studio.display_name}")
            self.session_logger.log_project_operation("Project setup completed successfully")
            
            return True
            
        except Exception as e:
            error_msg = f"Project setup failed: {e}"
            logger.error(error_msg)
            self.session_logger.log_error(error_msg, e)
            return False
