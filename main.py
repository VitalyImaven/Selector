"""
Main entry point for the Automation Studio Selector application.
"""
import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.logger import LoggerSetup
from src.ui.main_window import MainWindow


def setup_application_logging():
    """Setup application-wide logging."""
    try:
        # Create logs directory
        log_dir = Path.home() / ".automation_selector" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup main application logger
        log_file = log_dir / "application.log"
        logger = LoggerSetup.setup_logger(
            name="automation_selector",
            log_level=logging.INFO,
            log_file=log_file,
            console_output=True
        )
        
        logger.info("Application logging initialized")
        return True
        
    except Exception as e:
        print(f"Failed to setup logging: {e}")
        return False


def main():
    """Main application entry point."""
    try:
        # Setup logging first
        if not setup_application_logging():
            sys.exit(1)
        
        logger = logging.getLogger("automation_selector")
        logger.info("Starting Automation Studio Selector")
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("Automation Studio Selector")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Automation Tools")
        
        # Set application properties (High DPI scaling is enabled by default in PyQt6)
        # app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)  # Not needed in PyQt6
        # app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)     # Not needed in PyQt6
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        logger.info("Main window created and shown")
        
        # Run application
        exit_code = app.exec()
        logger.info(f"Application exited with code: {exit_code}")
        
        return exit_code
        
    except Exception as e:
        error_msg = f"Critical error starting application: {e}"
        print(error_msg)
        
        try:
            logger = logging.getLogger("automation_selector")
            logger.critical(error_msg, exc_info=True)
        except:
            pass
        
        # Try to show error dialog if possible
        try:
            if 'app' in locals():
                QMessageBox.critical(
                    None,
                    "Critical Error",
                    f"Failed to start Automation Studio Selector:\n\n{str(e)}"
                )
        except:
            pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
