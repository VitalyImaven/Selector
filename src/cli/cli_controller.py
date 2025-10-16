"""
CLI controller for routing commands and managing execution.
"""
import logging
import sys
from typing import List

from src.cli.cli_parser import CLIParser
from src.cli.cli_commands import CLICommands
from src.cli.cli_help import CLIHelp


logger = logging.getLogger(__name__)


class CLIController:
    """Main controller for CLI operations."""
    
    def __init__(self):
        """Initialize CLI controller."""
        self.parser = CLIParser()
        self.commands = CLICommands()
        self.help = CLIHelp()
    
    def execute(self, args: List[str]) -> int:
        """
        Execute CLI command.
        
        Args:
            args: Command-line arguments (without program name)
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Parse arguments
            command, options = self.parser.parse(args)
            
            if command is None:
                # No valid command found
                print("ERROR: Invalid command or arguments")
                print("Use: AutomationStudioSelector.exe -help for usage information")
                return 1
            
            # Route command to appropriate handler
            return self._route_command(command, options)
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user")
            return 130
        except Exception as e:
            logger.error(f"CLI execution error: {e}")
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
    
    def _route_command(self, command: str, options: dict) -> int:
        """Route command to appropriate handler."""
        command_map = {
            'open': self.commands.open_project,
            'list-projects': self.commands.list_projects,
            'list-studios': self.commands.list_studios,
            'list': self._handle_list_command,
            'sync': self.commands.sync_project,
            'add-project': self.commands.add_project,
            'remove-project': self.commands.remove_project,
            'status': self.commands.show_status,
            'sync-status': self.commands.show_sync_status,
            'show-config': self.commands.show_config,
            'version': self.commands.show_version,
            'help': self._handle_help_command,
        }
        
        handler = command_map.get(command)
        if handler:
            return handler(options)
        else:
            print(f"ERROR: Command not implemented: {command}")
            return 1
    
    def _handle_list_command(self, options: dict) -> int:
        """Handle generic list command."""
        # Show both projects and studios
        print("=" * 80)
        self.commands.list_projects(options)
        print("=" * 80)
        self.commands.list_studios(options)
        return 0
    
    def _handle_help_command(self, options: dict) -> int:
        """Handle help command."""
        specific_command = options.get('command')
        
        if specific_command:
            self.help.show_command_help(specific_command)
        else:
            self.help.show_general_help()
        
        return 0
