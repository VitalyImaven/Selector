"""
Command-line argument parser for Automation Studio Selector.
"""
import logging
from typing import Dict, List, Optional, Tuple


logger = logging.getLogger(__name__)


class CLIParser:
    """Parse command-line arguments."""
    
    def __init__(self):
        """Initialize CLI parser."""
        self.commands = {
            'open': self.parse_open_command,
            'list-projects': self.parse_list_command,
            'list-studios': self.parse_list_command,
            'list': self.parse_list_command,
            'sync': self.parse_sync_command,
            'add-project': self.parse_add_project_command,
            'remove-project': self.parse_remove_project_command,
            'add-studio': self.parse_add_studio_command,
            'remove-studio': self.parse_remove_studio_command,
            'status': self.parse_simple_command,
            'sync-status': self.parse_simple_command,
            'show-config': self.parse_simple_command,
            'version': self.parse_simple_command,
            'help': self.parse_help_command,
        }
    
    def parse(self, args: List[str]) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Parse command-line arguments.
        
        Args:
            args: List of command-line arguments
            
        Returns:
            Tuple of (command, options_dict) or (None, None) if invalid
        """
        try:
            if not args:
                return None, None
            
            # Check if first arg is a known command or a flag
            first_arg = args[0].lstrip('-').lower()
            
            # If first argument starts with '-', assume it's the 'open' command with flags
            if args[0].startswith('-'):
                # Flags without explicit command = assume 'open' command
                return 'open', self.parse_open_command(args)
            
            # Check if it's a valid command
            if first_arg in self.commands:
                parser_func = self.commands[first_arg]
                options = parser_func(args[1:])
                return first_arg, options
            else:
                # Try to parse as shorthand: ProjectName AS6
                if len(args) >= 2 and not args[0].startswith('-'):
                    # Shorthand for: open ProjectName -studio AS6
                    return 'open', {
                        'project': args[0],
                        'studio': args[1].upper(),
                        'prepare_only': False,
                        'wait': False,
                        'silent': False,
                        'verbose': False,
                        'project_path': None,
                        'studio_path': None,
                        'as_version': None,
                    }
                elif len(args) == 1 and not args[0].startswith('-'):
                    # Shorthand for: open ProjectName (use last studio)
                    return 'open', {
                        'project': args[0],
                        'studio': None,
                        'prepare_only': False,
                        'wait': False,
                        'silent': False,
                        'verbose': False,
                        'project_path': None,
                        'studio_path': None,
                        'as_version': None,
                    }
                
                logger.error(f"Unknown command: {first_arg}")
                return None, None
                
        except Exception as e:
            logger.error(f"Error parsing arguments: {e}")
            return None, None
    
    def parse_open_command(self, args: List[str]) -> Dict:
        """Parse open command arguments."""
        options = {
            'project': None,
            'project_path': None,  # Direct path to project
            'studio': None,
            'studio_path': None,   # Direct path to AS executable
            'as_version': None,    # AS version (45 or 6) - required for direct paths
            'wait': False,
            'silent': False,
            'verbose': False,
            'prepare_only': False,  # Prepare files but don't launch AS
        }
        
        i = 0
        while i < len(args):
            arg = args[i].lstrip('-').lower()
            
            if arg in ['project', 'p']:
                if i + 1 < len(args):
                    options['project'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg in ['project-path', 'path']:
                if i + 1 < len(args):
                    options['project_path'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg in ['studio', 's', 'as']:
                if i + 1 < len(args):
                    options['studio'] = args[i + 1].upper()
                    i += 2
                else:
                    i += 1
            elif arg in ['studio-path', 'as-path', 'exe-path']:
                if i + 1 < len(args):
                    options['studio_path'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg in ['as-version', 'version', 'v']:
                if i + 1 < len(args):
                    # Normalize version: 45, 4.5, AS45 all become "45"
                    version = args[i + 1].upper().replace('AS', '').replace('.', '').strip()
                    options['as_version'] = version
                    i += 2
                else:
                    i += 1
            elif arg == 'wait':
                options['wait'] = True
                i += 1
            elif arg == 'silent':
                options['silent'] = True
                i += 1
            elif arg == 'verbose':
                options['verbose'] = True
                i += 1
            elif arg in ['prepare-only', 'prepare', 'no-launch', 'nolaunch']:
                options['prepare_only'] = True
                i += 1
            else:
                # Assume it's a project name if no flag
                if not args[i].startswith('-'):
                    options['project'] = args[i]
                i += 1
        
        return options
    
    def parse_list_command(self, args: List[str]) -> Dict:
        """Parse list command arguments."""
        options = {
            'format': 'text',  # text or json
            'verbose': False,
        }
        
        i = 0
        while i < len(args):
            arg = args[i].lstrip('-').lower()
            
            if arg in ['format', 'f']:
                if i + 1 < len(args):
                    options['format'] = args[i + 1].lower()
                    i += 2
                else:
                    i += 1
            elif arg == 'json':
                options['format'] = 'json'
                i += 1
            elif arg == 'verbose':
                options['verbose'] = True
                i += 1
            else:
                i += 1
        
        return options
    
    def parse_sync_command(self, args: List[str]) -> Dict:
        """Parse sync command arguments."""
        options = {
            'project': None,
            'all': False,
            'silent': False,
            'verbose': False,
        }
        
        i = 0
        while i < len(args):
            arg = args[i].lstrip('-').lower()
            
            if arg in ['project', 'p']:
                if i + 1 < len(args):
                    options['project'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg == 'all':
                options['all'] = True
                i += 1
            elif arg == 'silent':
                options['silent'] = True
                i += 1
            elif arg == 'verbose':
                options['verbose'] = True
                i += 1
            else:
                # Assume it's a project name
                if not args[i].startswith('-'):
                    options['project'] = args[i]
                i += 1
        
        return options
    
    def parse_add_project_command(self, args: List[str]) -> Dict:
        """Parse add-project command arguments."""
        options = {
            'name': None,
            'path': None,
            'description': '',
        }
        
        i = 0
        while i < len(args):
            arg = args[i].lstrip('-').lower()
            
            if arg in ['name', 'n']:
                if i + 1 < len(args):
                    options['name'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg in ['path', 'p']:
                if i + 1 < len(args):
                    options['path'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg in ['description', 'desc', 'd']:
                if i + 1 < len(args):
                    options['description'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            else:
                # Try to parse positional arguments
                if not args[i].startswith('-'):
                    if options['name'] is None:
                        options['name'] = args[i]
                    elif options['path'] is None:
                        options['path'] = args[i]
                i += 1
        
        return options
    
    def parse_remove_project_command(self, args: List[str]) -> Dict:
        """Parse remove-project command arguments."""
        options = {
            'name': None,
            'force': False,
        }
        
        i = 0
        while i < len(args):
            arg = args[i].lstrip('-').lower()
            
            if arg in ['name', 'n']:
                if i + 1 < len(args):
                    options['name'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg == 'force':
                options['force'] = True
                i += 1
            else:
                if not args[i].startswith('-'):
                    options['name'] = args[i]
                i += 1
        
        return options
    
    def parse_add_studio_command(self, args: List[str]) -> Dict:
        """Parse add-studio command arguments."""
        options = {
            'version': None,
            'path': None,
        }
        
        i = 0
        while i < len(args):
            arg = args[i].lstrip('-').lower()
            
            if arg in ['version', 'v']:
                if i + 1 < len(args):
                    options['version'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg in ['path', 'p']:
                if i + 1 < len(args):
                    options['path'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            else:
                if not args[i].startswith('-'):
                    if options['version'] is None:
                        options['version'] = args[i]
                    elif options['path'] is None:
                        options['path'] = args[i]
                i += 1
        
        return options
    
    def parse_remove_studio_command(self, args: List[str]) -> Dict:
        """Parse remove-studio command arguments."""
        options = {
            'version': None,
            'force': False,
        }
        
        i = 0
        while i < len(args):
            arg = args[i].lstrip('-').lower()
            
            if arg in ['version', 'v']:
                if i + 1 < len(args):
                    options['version'] = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg == 'force':
                options['force'] = True
                i += 1
            else:
                if not args[i].startswith('-'):
                    options['version'] = args[i]
                i += 1
        
        return options
    
    def parse_simple_command(self, args: List[str]) -> Dict:
        """Parse simple commands with optional flags."""
        options = {
            'verbose': False,
            'json': False,
        }
        
        for arg in args:
            arg_lower = arg.lstrip('-').lower()
            if arg_lower == 'verbose':
                options['verbose'] = True
            elif arg_lower == 'json':
                options['json'] = True
        
        return options
    
    def parse_help_command(self, args: List[str]) -> Dict:
        """Parse help command arguments."""
        options = {
            'command': None,
        }
        
        if args and not args[0].startswith('-'):
            options['command'] = args[0].lstrip('-').lower()
        elif len(args) >= 2 and args[0].lstrip('-').lower() in ['command', 'c']:
            options['command'] = args[1].lstrip('-').lower()
        
        return options
