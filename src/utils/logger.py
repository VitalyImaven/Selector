"""
Logging utilities for the Automation Studio Selector.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class LoggerSetup:
    """Setup and configure application logging."""
    
    @staticmethod
    def setup_logger(
        name: str = "automation_selector",
        log_level: int = logging.INFO,
        log_file: Optional[Path] = None,
        console_output: bool = True
    ) -> logging.Logger:
        """
        Setup application logger with file and console handlers.
        
        Args:
            name: Logger name
            log_level: Logging level
            log_file: Path to log file (optional)
            console_output: Whether to output to console
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        
        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()
        logger.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            try:
                log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.error(f"Failed to setup file logging: {e}")
        
        return logger
    
    @staticmethod
    def create_session_log_file(base_dir: Optional[Path] = None) -> Path:
        """
        Create a session-specific log file.
        
        Args:
            base_dir: Base directory for logs
            
        Returns:
            Path to the session log file
        """
        if base_dir is None:
            base_dir = Path.home() / ".automation_selector" / "logs"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = base_dir / f"session_{timestamp}.log"
        
        return log_file


class SessionLogger:
    """Logger for tracking user sessions and operations."""
    
    def __init__(self, log_file: Optional[Path] = None):
        """Initialize session logger."""
        if log_file is None:
            log_file = LoggerSetup.create_session_log_file()
            
        self.log_file = log_file
        self.logger = LoggerSetup.setup_logger(
            name="session",
            log_file=log_file,
            console_output=False
        )
        
        # Log session start
        self.logger.info("=" * 50)
        self.logger.info("NEW AUTOMATION SELECTOR SESSION STARTED")
        self.logger.info("=" * 50)
    
    def log_studio_selection(self, studio_name: str, studio_version: str):
        """Log automation studio selection."""
        self.logger.info(f"User selected: {studio_name} (Version {studio_version})")
    
    def log_project_operation(self, operation: str, details: str = ""):
        """Log project operations."""
        message = f"Project operation: {operation}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_error(self, error_msg: str, exception: Optional[Exception] = None):
        """Log errors with optional exception details."""
        self.logger.error(f"ERROR: {error_msg}")
        if exception:
            self.logger.error(f"Exception details: {str(exception)}")
    
    def log_file_operation(self, operation: str, source: str, target: str = ""):
        """Log file operations."""
        message = f"File operation: {operation} - Source: {source}"
        if target:
            message += f" - Target: {target}"
        self.logger.info(message)
    
    def close_session(self):
        """Log session end."""
        self.logger.info("=" * 50)
        self.logger.info("AUTOMATION SELECTOR SESSION ENDED")
        self.logger.info("=" * 50)
