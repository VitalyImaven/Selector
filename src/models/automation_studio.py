"""
Data models for Automation Studio configurations.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from enum import Enum


class AutomationStudioVersion(Enum):
    """Enum for supported Automation Studio versions."""
    AS_45 = "4.5"
    AS_6 = "6"


@dataclass
class AutomationStudio:
    """Model representing an Automation Studio installation."""
    name: str
    version: AutomationStudioVersion
    executable_path: Path
    libraries_suffix: str
    physical_pkg_suffix: str
    project_file_suffix: str
    
    @property
    def display_name(self) -> str:
        """Get display name for UI."""
        return f"Automation Studio {self.version.value}"
    
    @classmethod
    def create_as45(cls, executable_path: Path) -> "AutomationStudio":
        """Create AS 4.5 configuration."""
        return cls(
            name="AS 4.5",
            version=AutomationStudioVersion.AS_45,
            executable_path=executable_path,
            libraries_suffix="45",
            physical_pkg_suffix="45",
            project_file_suffix="45"
        )
    
    @classmethod
    def create_as6(cls, executable_path: Path) -> "AutomationStudio":
        """Create AS 6 configuration."""
        return cls(
            name="AS 6",
            version=AutomationStudioVersion.AS_6,
            executable_path=executable_path,
            libraries_suffix="6",
            physical_pkg_suffix="6",
            project_file_suffix="6"
        )


@dataclass
class ProjectPaths:
    """Model for project directory structure."""
    root_path: Path
    logical_path: Path
    physical_path: Path
    libraries_path: Path
    
    @classmethod
    def from_root(cls, root_path: Path) -> "ProjectPaths":
        """Create ProjectPaths from root directory."""
        root = Path(root_path)
        return cls(
            root_path=root,
            logical_path=root / "Logical",
            physical_path=root / "Physical", 
            libraries_path=root / "Logical" / "Libraries"
        )
