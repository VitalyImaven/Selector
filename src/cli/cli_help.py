"""
Help system for CLI commands.
"""


class CLIHelp:
    """CLI help and documentation."""
    
    def show_general_help(self):
        """Show general help information."""
        print("""
Automation Studio Selector - Command Line Interface
Created by Vitaly Grosman - Indigo R&D Division

USAGE:
    AutomationStudioSelector.exe [command] [options]

COMMON COMMANDS:
    
    Project Operations:
        -open PROJECT -studio AS6        Open project with AS 6
        -open PROJECT -studio AS45       Open project with AS 4.5
        PROJECT AS6                      Shorthand: open project with AS 6
        
    Information:
        -list-projects                   Show all configured projects
        -list-studios                    Show all configured AS versions
        -list                            Show both projects and studios
        -status                          Show application status
        -sync-status                     Show sync statistics
        
    Synchronization:
        -sync                            Sync current project
        -sync PROJECT                    Sync specific project
        
    Project Management:
        -add-project NAME PATH           Add new project
        -remove-project NAME             Remove project from list
        
    Configuration:
        -show-config                     Display current configuration
        -version                         Show application version
        -help                            Show this help message
        -help COMMAND                    Show help for specific command

EXAMPLES:
    
    Open a project:
        AutomationStudioSelector.exe -open MyProject -studio AS6
        AutomationStudioSelector.exe MyProject AS6              (shorthand)
    
    List everything:
        AutomationStudioSelector.exe -list
    
    Sync a project:
        AutomationStudioSelector.exe -sync MyProject
    
    Add new project:
        AutomationStudioSelector.exe -add-project TestProj C:\\Projects\\Test

OPTIONS:
    -silent          Suppress output (errors only)
    -verbose         Show detailed information
    -json            Output in JSON format
    -wait            Wait for Automation Studio to close
    -force           Skip confirmation prompts

For detailed help on a specific command:
    AutomationStudioSelector.exe -help COMMAND

For GUI mode:
    AutomationStudioSelector.exe (no arguments)
        """)
    
    def show_command_help(self, command: str):
        """Show help for specific command."""
        help_map = {
            'open': self._help_open,
            'list-projects': self._help_list_projects,
            'list-studios': self._help_list_studios,
            'sync': self._help_sync,
            'add-project': self._help_add_project,
            'remove-project': self._help_remove_project,
            'status': self._help_status,
        }
        
        handler = help_map.get(command)
        if handler:
            handler()
        else:
            print(f"No detailed help available for: {command}")
            print("Use -help to see all available commands")
    
    def _help_open(self):
        """Help for open command."""
        print("""
COMMAND: open
    Open a project with specified Automation Studio version

USAGE:
    AutomationStudioSelector.exe -open PROJECT -studio VERSION [options]
    AutomationStudioSelector.exe PROJECT VERSION                (shorthand)

ARGUMENTS:
    PROJECT          Name of the project (from configured projects)
    VERSION          AS version (AS6, AS45, 6, 4.5, etc.)

OPTIONS:
    -prepare-only    Prepare files but DON'T launch Automation Studio
    -wait            Wait for Automation Studio to close before exiting
    -silent          Suppress all output except errors
    -verbose         Show detailed progress information

EXAMPLES:
    AutomationStudioSelector.exe -open ProductionLine -studio AS6
    AutomationStudioSelector.exe ProductionLine AS6
    AutomationStudioSelector.exe -open TestProject -studio AS45 -wait
    AutomationStudioSelector.exe MyProject AS6 -prepare-only         (just prepare files)
        """)    
    
    def _help_prepare(self):
        """Help for prepare-only mode."""
        print("""
OPTION: -prepare-only
    Prepare project files for Automation Studio without launching it

DESCRIPTION:
    This mode performs all file operations (copy libraries, update Physical.pkg,
    update OCB.apj) but stops before launching Automation Studio.
    
    Useful for:
    - Batch file preparation
    - CI/CD pipelines
    - Pre-configuring projects
    - Automated testing
    - Remote server operations

USAGE:
    AutomationStudioSelector.exe -open PROJECT -studio VERSION -prepare-only
    AutomationStudioSelector.exe PROJECT VERSION -prepare-only

WHAT IT DOES:
    1. ✓ Validates project structure
    2. ✓ Clears Libraries directory
    3. ✓ Copies version-specific libraries
    4. ✓ Updates Physical.pkg file
    5. ✓ Updates OCB.apj file
    6. ✗ Does NOT launch Automation Studio

EXAMPLES:
    # Prepare for AS 6
    AutomationStudioSelector.exe MyProject AS6 -prepare-only
    
    # Prepare multiple projects in batch
    AutomationStudioSelector.exe Project1 AS6 -prepare-only -silent
    AutomationStudioSelector.exe Project2 AS45 -prepare-only -silent
    AutomationStudioSelector.exe Project3 AS6 -prepare-only -silent
    
    # Prepare with verbose output
    AutomationStudioSelector.exe MyProject AS6 -prepare-only -verbose
        """)
        
    
    def _help_list_projects(self):
        """Help for list-projects command."""
        print("""
COMMAND: list-projects
    Display all configured projects

USAGE:
    AutomationStudioSelector.exe -list-projects [options]

OPTIONS:
    -json            Output in JSON format
    -verbose         Show additional details

EXAMPLES:
    AutomationStudioSelector.exe -list-projects
    AutomationStudioSelector.exe -list-projects -json
        """)
    
    def _help_list_studios(self):
        """Help for list-studios command."""
        print("""
COMMAND: list-studios
    Display all configured Automation Studio installations

USAGE:
    AutomationStudioSelector.exe -list-studios [options]

OPTIONS:
    -json            Output in JSON format
    -verbose         Show additional details

EXAMPLES:
    AutomationStudioSelector.exe -list-studios
    AutomationStudioSelector.exe -list-studios -json
        """)
    
    def _help_sync(self):
        """Help for sync command."""
        print("""
COMMAND: sync
    Manually synchronize project files

USAGE:
    AutomationStudioSelector.exe -sync [PROJECT] [options]

ARGUMENTS:
    PROJECT          Project name (optional, uses last selected if omitted)

OPTIONS:
    -silent          Suppress output
    -verbose         Show detailed sync information

EXAMPLES:
    AutomationStudioSelector.exe -sync
    AutomationStudioSelector.exe -sync ProductionLine
    AutomationStudioSelector.exe -sync MyProject -verbose
        """)
    
    def _help_add_project(self):
        """Help for add-project command."""
        print("""
COMMAND: add-project
    Add a new project to the configuration

USAGE:
    AutomationStudioSelector.exe -add-project -name NAME -path PATH [options]
    AutomationStudioSelector.exe -add-project NAME PATH              (shorthand)

ARGUMENTS:
    NAME             Friendly name for the project
    PATH             Full path to project directory

OPTIONS:
    -description     Optional project description

EXAMPLES:
    AutomationStudioSelector.exe -add-project -name TestProj -path C:\\Projects\\Test
    AutomationStudioSelector.exe -add-project MyProject C:\\Projects\\MyProject
    AutomationStudioSelector.exe -add-project -name Prod -path C:\\Prod -description "Production system"
        """)
    
    def _help_remove_project(self):
        """Help for remove-project command."""
        print("""
COMMAND: remove-project
    Remove a project from the configuration

USAGE:
    AutomationStudioSelector.exe -remove-project NAME [options]
    AutomationStudioSelector.exe -remove-project -name NAME

ARGUMENTS:
    NAME             Name of the project to remove

OPTIONS:
    -force           Skip confirmation prompt

EXAMPLES:
    AutomationStudioSelector.exe -remove-project OldProject
    AutomationStudioSelector.exe -remove-project TestProj -force
        """)
    
    def _help_status(self):
        """Help for status command."""
        print("""
COMMAND: status
    Display application status and configuration summary

USAGE:
    AutomationStudioSelector.exe -status [options]

OPTIONS:
    -json            Output in JSON format
    -verbose         Show additional details

EXAMPLES:
    AutomationStudioSelector.exe -status
    AutomationStudioSelector.exe -status -json
        """)
