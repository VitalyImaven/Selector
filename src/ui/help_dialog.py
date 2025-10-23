"""
Interactive help and tutorial dialog for the Automation Studio Selector.
"""
import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QTreeWidget, QTreeWidgetItem, QSplitter, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

from src.ui.styles import MAIN_STYLE


logger = logging.getLogger(__name__)


class HelpDialog(QDialog):
    """Interactive help and tutorial dialog."""
    
    def __init__(self, parent=None):
        """Initialize help dialog."""
        super().__init__(parent)
        self.setup_ui()
        self.load_help_content()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("How To Use - Automation Studio Selector")
        self.setModal(True)
        self.resize(800, 920)
        
        # Apply styles
        self.setStyleSheet(MAIN_STYLE)
        
        layout = QVBoxLayout(self)
        
        # Header section
        self.setup_header(layout)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left panel - navigation tree
        self.setup_navigation_panel(splitter)
        
        # Right panel - content display
        self.setup_content_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([250, 650])
        
        # Close button
        self.setup_close_button(layout)
        
    def setup_header(self, parent_layout):
        """Setup the header section."""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 0px;
                padding: 5px 10px;
                margin: 0px;
                max-height: 35px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(5, 2, 5, 2)
        header_layout.setSpacing(8)
        
        # Small logo
        try:
            import sys
            import os
            
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                # Running in development - go up to project root
                current_file = os.path.abspath(__file__)
                ui_dir = os.path.dirname(current_file)
                src_dir = os.path.dirname(ui_dir)
                base_path = os.path.dirname(src_dir)
            
            logo_path = os.path.join(base_path, 'assets', 'logo.png')
            logo = QLabel()
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo.setPixmap(scaled_pixmap)
                header_layout.addWidget(logo)
        except:
            pass
        
        # Minimal title
        title = QLabel("Help & Documentation")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                margin: 0px;
                padding: 0px;
            }
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        parent_layout.addWidget(header_frame)
    
    def setup_navigation_panel(self, splitter):
        """Setup the navigation tree panel."""
        nav_frame = QFrame()
        nav_layout = QVBoxLayout(nav_frame)
        
        nav_title = QLabel("Help Topics")
        nav_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px;
                border-bottom: 2px solid #3498db;
                margin-bottom: 10px;
            }
        """)
        nav_layout.addWidget(nav_title)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                font-size: 14px;
            }
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTreeWidget::item:hover {
                background-color: #f8f9fa;
            }
            QTreeWidget::item:selected {
                background-color: #16a085;
                color: white;
            }
        """)
        self.tree.itemClicked.connect(self.on_topic_selected)
        nav_layout.addWidget(self.tree)
        
        splitter.addWidget(nav_frame)
    
    def setup_content_panel(self, splitter):
        """Setup the content display panel."""
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        
        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        self.content_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                padding: 15px;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        content_layout.addWidget(self.content_display)
        
        splitter.addWidget(content_frame)
    
    def setup_close_button(self, parent_layout):
        """Setup the close button."""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setObjectName("primary")
        close_btn.clicked.connect(self.accept)
        close_btn.setFixedSize(100, 35)
        button_layout.addWidget(close_btn)
        
        parent_layout.addLayout(button_layout)
    
    def load_help_content(self):
        """Load help topics into the navigation tree."""
        # Getting Started section
        getting_started = QTreeWidgetItem(self.tree, ["🚀 Getting Started"])
        QTreeWidgetItem(getting_started, ["First-Time Setup"])
        QTreeWidgetItem(getting_started, ["Basic Workflow"])
        QTreeWidgetItem(getting_started, ["Project Structure"])
        
        # Interface Guide section
        interface = QTreeWidgetItem(self.tree, ["🖥️ Interface Guide"])
        QTreeWidgetItem(interface, ["Header Section"])
        QTreeWidgetItem(interface, ["Project Root Directory"])
        QTreeWidgetItem(interface, ["Automation Studio Selection"])
        QTreeWidgetItem(interface, ["Operation Progress"])
        QTreeWidgetItem(interface, ["Session Log"])
        QTreeWidgetItem(interface, ["Menu System"])
        
        # Features section
        features = QTreeWidgetItem(self.tree, ["⚡ Features"])
        QTreeWidgetItem(features, ["Auto-Sync System"])
        QTreeWidgetItem(features, ["Manual Sync"])
        QTreeWidgetItem(features, ["Settings Configuration"])
        QTreeWidgetItem(features, ["Status Monitoring"])
        
        # Troubleshooting section
        troubleshooting = QTreeWidgetItem(self.tree, ["🔧 Troubleshooting"])
        QTreeWidgetItem(troubleshooting, ["Common Issues"])
        QTreeWidgetItem(troubleshooting, ["Error Messages"])
        QTreeWidgetItem(troubleshooting, ["Log Files"])
        
        # Tips section
        tips = QTreeWidgetItem(self.tree, ["💡 Tips & Best Practices"])
        QTreeWidgetItem(tips, ["Workflow Optimization"])
        QTreeWidgetItem(tips, ["Safety Guidelines"])
        QTreeWidgetItem(tips, ["Performance Tips"])
        
        # CLI section
        cli_section = QTreeWidgetItem(self.tree, ["🖥️ Command Line (CLI)"])
        QTreeWidgetItem(cli_section, ["CLI Overview"])
        QTreeWidgetItem(cli_section, ["Basic CLI Commands"])
        QTreeWidgetItem(cli_section, ["Prepare-Only Mode"])
        QTreeWidgetItem(cli_section, ["Jenkins & CI/CD"])
        QTreeWidgetItem(cli_section, ["CLI Examples"])
        
        # Advanced section
        advanced = QTreeWidgetItem(self.tree, ["🔧 Advanced Topics"])
        QTreeWidgetItem(advanced, ["What Happens Step-by-Step"])
        QTreeWidgetItem(advanced, ["File Operations Explained"])
        QTreeWidgetItem(advanced, ["Multiple Projects"])
        
        # Expand all sections
        self.tree.expandAll()
        
        # Select first item by default
        if self.tree.topLevelItemCount() > 0:
            first_item = self.tree.topLevelItem(0)
            if first_item.childCount() > 0:
                self.tree.setCurrentItem(first_item.child(0))
                self.on_topic_selected(first_item.child(0), 0)
    
    def on_topic_selected(self, item, column):
        """Handle topic selection from navigation tree."""
        if not item:
            return
            
        topic = item.text(0)
        content = self.get_content_for_topic(topic)
        self.content_display.setHtml(content)
    
    def get_content_for_topic(self, topic):
        """Get HTML content for the selected topic."""
        content_map = {
            "First-Time Setup": self.get_first_time_setup_content(),
            "Basic Workflow": self.get_basic_workflow_content(),
            "Project Structure": self.get_project_structure_content(),
            "Header Section": self.get_header_section_content(),
            "Project Root Directory": self.get_project_root_content(),
            "Automation Studio Selection": self.get_studio_selection_content(),
            "Operation Progress": self.get_progress_content(),
            "Session Log": self.get_session_log_content(),
            "Menu System": self.get_menu_system_content(),
            "Auto-Sync System": self.get_auto_sync_content(),
            "Manual Sync": self.get_manual_sync_content(),
            "Settings Configuration": self.get_settings_content(),
            "Status Monitoring": self.get_status_monitoring_content(),
            "Common Issues": self.get_common_issues_content(),
            "Error Messages": self.get_error_messages_content(),
            "Log Files": self.get_log_files_content(),
            "Workflow Optimization": self.get_workflow_optimization_content(),
            "Safety Guidelines": self.get_safety_guidelines_content(),
            "Performance Tips": self.get_performance_tips_content(),
            "CLI Overview": self.get_cli_overview_content(),
            "Basic CLI Commands": self.get_cli_commands_content(),
            "Prepare-Only Mode": self.get_prepare_only_content(),
            "Jenkins & CI/CD": self.get_jenkins_content(),
            "CLI Examples": self.get_cli_examples_content(),
            "What Happens Step-by-Step": self.get_step_by_step_content(),
            "File Operations Explained": self.get_file_operations_content(),
            "Multiple Projects": self.get_multiple_projects_content(),
        }
        
        return content_map.get(topic, self.get_default_content())
    
    def get_first_time_setup_content(self):
        """Content for first-time setup."""
        return """
        <h2>🚀 First-Time Setup</h2>
        
        <p>When you first launch the Automation Studio Selector, you need to configure two main things:</p>
        
        <h3>1. Automation Studio Paths</h3>
        <p>Tell the application where your Automation Studio installations are located:</p>
        <ul>
            <li><strong>Click "Add AS 4.5"</strong> - Browse to your AS 4.5 installation directory</li>
            <li><strong>Click "Add AS 6"</strong> - Browse to your AS 6 installation directory</li>
            <li><strong>Select AutomationStudio.exe</strong> in each directory</li>
        </ul>
        
        <h3>2. Project Root Directory</h3>
        <p>Select your project's main folder:</p>
        <ul>
            <li><strong>Click "Browse..."</strong> next to Project Root Directory</li>
            <li><strong>Navigate to your project</strong> that contains Logical and Physical folders</li>
            <li><strong>Select the folder</strong> and click "Select Folder"</li>
        </ul>
        
        <h3>3. Save and Continue</h3>
        <p>After configuring both items:</p>
        <ul>
            <li><strong>Review your settings</strong> in the setup dialog</li>
            <li><strong>Click "Save & Continue"</strong> to complete setup</li>
            <li>The application will <strong>validate your configuration</strong></li>
        </ul>
        
        <div style="background-color: #e8f6f3; padding: 15px; border-left: 4px solid #16a085; margin: 15px 0;">
            <strong>💡 Tip:</strong> You can always change these settings later using the File menu.
        </div>
        """
    
    def get_basic_workflow_content(self):
        """Content for basic workflow."""
        return """
        <h2>🔄 Basic Workflow</h2>
        
        <p>Follow these steps to use the Automation Studio Selector:</p>
        
        <h3>Step 1: Verify Project Root</h3>
        <ul>
            <li>Check that the <strong>Project Root Directory</strong> shows your project path</li>
            <li>If not correct, click <strong>"Browse..."</strong> to select the right folder</li>
        </ul>
        
        <h3>Step 2: Choose Automation Studio Version</h3>
        <ul>
            <li>Look at the <strong>"Select Automation Studio"</strong> section</li>
            <li>You'll see all configured AS versions (e.g., "Automation Studio 4.5", "Automation Studio 6")</li>
            <li><strong>Click on the version</strong> you want to use</li>
            <li>The selected version will be <strong>highlighted in teal</strong></li>
        </ul>
        
        <h3>Step 3: Open Your Project</h3>
        <ul>
            <li>Click the <strong>"Open Project"</strong> button (green button)</li>
            <li>Watch the <strong>Operation Progress</strong> section for updates</li>
            <li>The application will automatically:
                <ul>
                    <li>✅ Validate your project structure</li>
                    <li>🗑️ Clear the active Libraries directory</li>
                    <li>📋 Copy libraries for your selected AS version</li>
                    <li>📄 Update Physical.pkg file</li>
                    <li>📁 Update project file (OCB.apj)</li>
                    <li>🚀 Launch Automation Studio with your project</li>
                </ul>
            </li>
        </ul>
        
        <h3>Step 4: Work Normally</h3>
        <ul>
            <li><strong>Automation Studio opens</strong> with your project ready</li>
            <li><strong>Make your changes</strong> as you normally would</li>
            <li><strong>Save your work</strong> in Automation Studio</li>
            <li>The <strong>auto-sync system</strong> will automatically preserve your changes</li>
        </ul>
        
        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0;">
            <strong>⚠️ Important:</strong> Always let the "Open Project" operation complete before using Automation Studio.
        </div>
        """
    
    def get_project_structure_content(self):
        """Content for project structure."""
        return """
        <h2>📁 Project Structure</h2>
        
        <p>Your project should be organized with this specific structure:</p>
        
        <div style="background-color: #f8f9fa; padding: 15px; border: 1px solid #dee2e6; border-radius: 6px; font-family: 'Courier New', monospace;">
        YourProject/<br>
        ├── Logical/<br>
        │&nbsp;&nbsp;&nbsp;├── Libraries/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Active working directory (managed automatically)<br>
        │&nbsp;&nbsp;&nbsp;├── Libraries_45/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# AS 4.5 libraries (your permanent storage)<br>
        │&nbsp;&nbsp;&nbsp;└── Libraries_6/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# AS 6 libraries (your permanent storage)<br>
        ├── Physical/<br>
        │&nbsp;&nbsp;&nbsp;├── Physical.pkg&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Active config (managed automatically)<br>
        │&nbsp;&nbsp;&nbsp;├── Physical_45.pkg&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# AS 4.5 config (your permanent storage)<br>
        │&nbsp;&nbsp;&nbsp;└── Physical_6.pkg&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# AS 6 config (your permanent storage)<br>
        ├── OCB.apj&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Main project file (managed automatically)<br>
        ├── OCB_as45.apj&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# AS 4.5 project template (your permanent storage)<br>
        └── OCB_as6.apj&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# AS 6 project template (your permanent storage)
        </div>
        
        <h3>📝 Key Understanding:</h3>
        
        <h4>🚫 Files You Should NEVER Edit:</h4>
        <ul>
            <li><strong>Libraries/</strong> - Active working directory (automatically managed)</li>
            <li><strong>Physical.pkg</strong> - Active configuration (automatically managed)</li>
            <li><strong>OCB.apj</strong> - Main project file (automatically managed)</li>
        </ul>
        
        <h4>✅ Files You Work With:</h4>
        <ul>
            <li><strong>Libraries_45/</strong> - Your AS 4.5 libraries (permanent storage)</li>
            <li><strong>Libraries_6/</strong> - Your AS 6 libraries (permanent storage)</li>
            <li><strong>Physical_45.pkg</strong> - Your AS 4.5 configuration</li>
            <li><strong>Physical_6.pkg</strong> - Your AS 6 configuration</li>
            <li><strong>OCB_as45.apj</strong> - Your AS 4.5 project template</li>
            <li><strong>OCB_as6.apj</strong> - Your AS 6 project template</li>
        </ul>
        
        <h3>🔄 How It Works:</h3>
        <ol>
            <li>You select <strong>AS 6</strong> → Libraries_6 content is copied to Libraries</li>
            <li>You work in AS and modify files in Libraries</li>
            <li><strong>Auto-sync triggers</strong> → Your changes are copied from Libraries back to Libraries_6</li>
            <li>Later, you select <strong>AS 4.5</strong> → Libraries_45 content is copied to Libraries</li>
            <li>Your AS 6 work is safely stored in Libraries_6!</li>
        </ol>
        
        <div style="background-color: #e8f6f3; padding: 15px; border-left: 4px solid #16a085; margin: 15px 0;">
            <strong>💡 Pro Tip:</strong> The Selector manages the "active" files automatically, so you never lose work when switching versions.
        </div>
        """
    
    def get_studio_selection_content(self):
        """Content for studio selection."""
        return """
        <h2>🎯 Automation Studio Selection</h2>
        
        <p>This section lets you choose which Automation Studio version to use for your project.</p>
        
        <h3>📋 What You'll See:</h3>
        
        <h4>📄 Instructions Text</h4>
        <p>"Choose which Automation Studio version to use for opening your project:"</p>
        
        <h4>📝 Studio List</h4>
        <ul>
            <li>Shows all your configured Automation Studio versions</li>
            <li>Format: <strong>"Automation Studio X.X"</strong></li>
            <li>Below each: <strong>Path to executable</strong></li>
            <li>Example:
                <ul>
                    <li>Automation Studio 4.5</li>
                    <li>Path: C:\\BrAutomation\\AS45\\Bin-en\\AutomationStudio.exe</li>
                </ul>
            </li>
        </ul>
        
        <h3>🖱️ How to Use:</h3>
        
        <h4>Selecting a Version:</h4>
        <ol>
            <li><strong>Click on any studio version</strong> in the list</li>
            <li>The selected item will be <strong>highlighted in teal</strong></li>
            <li>The <strong>"Open Project" button becomes active</strong> (green)</li>
        </ol>
        
        <h4>Double-Click Shortcut:</h4>
        <ul>
            <li><strong>Double-click</strong> any studio version to select it AND immediately open the project</li>
            <li>This is a faster way to work if you know which version you want</li>
        </ul>
        
        <h3>🔘 Button Functions:</h3>
        
        <h4>"Refresh List" Button:</h4>
        <ul>
            <li><strong>Purpose:</strong> Reload the list of configured studios</li>
            <li><strong>When to use:</strong> After adding new AS installations or if the list seems outdated</li>
            <li><strong>What it does:</strong> Re-reads your configuration and updates the display</li>
        </ul>
        
        <h4>"Open Project" Button (Green):</h4>
        <ul>
            <li><strong>Purpose:</strong> Start the selected Automation Studio with your project</li>
            <li><strong>When enabled:</strong> When both a studio is selected AND a valid project root is set</li>
            <li><strong>What it does:</strong> Performs the complete project setup and opens AS</li>
        </ul>
        
        <h3>📊 Status Indicators:</h3>
        
        <h4>Selection Highlight:</h4>
        <ul>
            <li><strong>Teal background:</strong> Currently selected studio</li>
            <li><strong>No selection:</strong> No studio chosen yet</li>
        </ul>
        
        <h4>Button States:</h4>
        <ul>
            <li><strong>Green "Open Project":</strong> Ready to open (studio selected + valid project)</li>
            <li><strong>Gray "Open Project":</strong> Not ready (missing selection or invalid project)</li>
        </ul>
        
        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0;">
            <strong>⚠️ Remember:</strong> The application remembers your last selected studio, so it will be pre-selected next time you open the app.
        </div>
        """
    
    def get_auto_sync_content(self):
        """Content for auto-sync system."""
        return """
        <h2>⚡ Auto-Sync System</h2>
        
        <p>The auto-sync system is the heart of the application - it ensures you never lose work when switching between Automation Studio versions.</p>
        
        <h3>🔄 How Auto-Sync Works:</h3>
        
        <p>The system automatically copies your changes from the active working directory back to the permanent version-specific storage.</p>
        
        <h4>Example Flow:</h4>
        <ol>
            <li>You select <strong>AS 6</strong> → Libraries_6 content is copied to Libraries</li>
            <li>You work in AS and modify files in Libraries</li>
            <li><strong>Auto-sync triggers</strong> → Your changes are copied from Libraries back to Libraries_6</li>
            <li>Later, you select <strong>AS 4.5</strong> → Libraries_45 content is copied to Libraries</li>
            <li>Your AS 6 work is safely stored in Libraries_6!</li>
        </ol>
        
        <h3>⚡ When Auto-Sync Happens:</h3>
        
        <h4>1. 🔴 Automation Studio Closes (Default: Enabled)</h4>
        <ul>
            <li><strong>Trigger:</strong> When you close any Automation Studio process</li>
            <li><strong>Action:</strong> Immediately syncs all changes back to version-specific storage</li>
            <li><strong>Why:</strong> Captures your work session changes immediately</li>
        </ul>
        
        <h4>2. 🚪 Selector Application Closes (Default: Enabled)</h4>
        <ul>
            <li><strong>Trigger:</strong> When you close the Selector application</li>
            <li><strong>Action:</strong> Final sync to ensure nothing is lost</li>
            <li><strong>Why:</strong> Safety net for any remaining changes</li>
        </ul>
        
        <h4>3. ⏰ Periodic Timer (Default: Every 5 minutes)</h4>
        <ul>
            <li><strong>Trigger:</strong> Regular interval while you work</li>
            <li><strong>Action:</strong> Checks for changes and syncs if found</li>
            <li><strong>Why:</strong> Continuous backup of your work</li>
        </ul>
        
        <h3>🛡️ Safety Features:</h3>
        
        <h4>📦 Automatic Backups:</h4>
        <ul>
            <li>Creates <strong>timestamped backups</strong> before overwriting</li>
            <li>Keeps the last <strong>3 backup versions</strong> by default</li>
            <li>Stored in backup directories with timestamps</li>
        </ul>
        
        <h4>🔍 Change Detection:</h4>
        <ul>
            <li>Only syncs files that <strong>actually changed</strong></li>
            <li>Compares file size and modification time</li>
            <li>Avoids unnecessary copying</li>
        </ul>
        
        <h4>📝 Comprehensive Logging:</h4>
        <ul>
            <li>Every sync operation is <strong>logged with timestamps</strong></li>
            <li>Shows exactly which files were synced</li>
            <li>Visible in the Session Log area</li>
        </ul>
        
        <h3>📊 Monitoring Auto-Sync:</h3>
        
        <h4>In the Session Log:</h4>
        <ul>
            <li><strong>"✓ Auto-sync completed: X files synchronized"</strong> - Success message</li>
            <li><strong>"✗ Auto-sync error: [message]"</strong> - Error message</li>
            <li><strong>Timestamps</strong> show when each sync occurred</li>
        </ul>
        
        <h4>In the Status Bar:</h4>
        <ul>
            <li><strong>"Auto-sync: X files synchronized"</strong> - Brief status update</li>
            <li>Appears temporarily when sync completes</li>
        </ul>
        
        <h3>⚙️ Configuring Auto-Sync:</h3>
        
        <p>Go to <strong>Settings → Sync → Auto-Sync Settings...</strong> to configure:</p>
        <ul>
            <li><strong>Enable/disable</strong> each trigger type</li>
            <li><strong>Adjust timer interval</strong> (1-60 minutes)</li>
            <li><strong>Control backup settings</strong> (enable/disable, max backups)</li>
            <li><strong>Toggle logging</strong> on/off</li>
        </ul>
        
        <div style="background-color: #e8f6f3; padding: 15px; border-left: 4px solid #16a085; margin: 15px 0;">
            <strong>💡 Pro Tip:</strong> Leave auto-sync enabled with default settings. It's designed to be transparent and reliable, protecting your work without getting in your way.
        </div>
        """
    
    def get_default_content(self):
        """Default content when no specific topic is found."""
        return """
        <h2>📖 Help Topic</h2>
        <p>Select a topic from the navigation panel to see detailed information.</p>
        <p>Use the tree on the left to browse through different help sections:</p>
        <ul>
            <li><strong>🚀 Getting Started</strong> - Basic setup and workflow</li>
            <li><strong>🖥️ Interface Guide</strong> - Detailed explanation of each UI element</li>
            <li><strong>⚡ Features</strong> - Advanced functionality and features</li>
            <li><strong>🔧 Troubleshooting</strong> - Solutions to common problems</li>
            <li><strong>💡 Tips & Best Practices</strong> - Expert advice for optimal usage</li>
        </ul>
        """
    
    # Additional content methods for other topics...
    def get_header_section_content(self):
        return """
        <h2>🏠 Header Section</h2>
        <p>The header displays the application branding and title.</p>
        <h3>Elements:</h3>
        <ul>
            <li><strong>Logo:</strong> Indigo R&D Division branding</li>
            <li><strong>Title:</strong> "Automation Studio Selector"</li>
        </ul>
        """
    
    def get_project_root_content(self):
        return """
        <h2>📁 Project Root Directory</h2>
        <p>This section shows and allows you to change your current project location.</p>
        <h3>Components:</h3>
        <ul>
            <li><strong>Path Display:</strong> Shows current project directory</li>
            <li><strong>Browse Button:</strong> Click to select a different project</li>
        </ul>
        <h3>Requirements:</h3>
        <p>The selected directory must contain both "Logical" and "Physical" subdirectories.</p>
        """
    
    def get_menu_system_content(self):
        return """
        <h2>📋 Menu System</h2>
        <h3>File Menu:</h3>
        <ul>
            <li><strong>Setup Automation Studio Paths...</strong> - Configure AS installations</li>
            <li><strong>Change Project Root...</strong> - Select different project</li>
            <li><strong>Manual Sync Now</strong> - Immediate synchronization</li>
        </ul>
        <h3>Settings Menu:</h3>
        <ul>
            <li><strong>Sync → Auto-Sync Settings...</strong> - Configure synchronization</li>
            <li><strong>Sync → View Sync Status</strong> - Monitor sync operations</li>
        </ul>
        <h3>Help Menu:</h3>
        <ul>
            <li><strong>How To</strong> - This interactive help system</li>
            <li><strong>About</strong> - Application information</li>
        </ul>
        """
    
    def get_common_issues_content(self):
        return """
        <h2>🔧 Common Issues</h2>
        <h3>"Project structure validation failed"</h3>
        <p><strong>Solutions:</strong></p>
        <ul>
            <li>Ensure you have "Logical" and "Physical" folders</li>
            <li>Check project root directory path</li>
            <li>Verify read permissions</li>
        </ul>
        <h3>"Automation Studio executable not found"</h3>
        <p><strong>Solutions:</strong></p>
        <ul>
            <li>Reconfigure paths in File → Setup Automation Studio Paths</li>
            <li>Verify AS installation</li>
            <li>Check file permissions</li>
        </ul>
        """
    
    def get_progress_content(self):
        """Content for operation progress."""
        return """
        <h2>⚙️ Operation Progress</h2>
        <p>This section shows the progress of project setup operations.</p>
        <h3>What You'll See:</h3>
        <ul>
            <li><strong>Progress Bar:</strong> Animated bar during operations</li>
            <li><strong>Status Messages:</strong> Real-time updates in status bar</li>
            <li><strong>Completion:</strong> Bar disappears when done</li>
        </ul>
        <h3>Typical Steps:</h3>
        <ol>
            <li>Validating project structure...</li>
            <li>Clearing Libraries directory...</li>
            <li>Copying version-specific libraries...</li>
            <li>Updating Physical.pkg file...</li>
            <li>Updating project file...</li>
            <li>Opening project...</li>
        </ol>
        """
    
    def get_session_log_content(self):
        """Content for session log."""
        return """
        <h2>📝 Session Log</h2>
        <p>The session log shows a detailed record of all operations.</p>
        <h3>Log Format:</h3>
        <ul>
            <li><strong>[HH:MM:SS]</strong> - Timestamp</li>
            <li><strong>✓</strong> - Success indicator</li>
            <li><strong>✗</strong> - Error indicator</li>
            <li><strong>Message</strong> - Operation description</li>
        </ul>
        <h3>What Gets Logged:</h3>
        <ul>
            <li>Application startup and configuration</li>
            <li>Project operations (setup, sync)</li>
            <li>Auto-sync activities</li>
            <li>Errors and warnings</li>
        </ul>
        <h3>Clear Log Button:</h3>
        <p>Click to clear the display. Note: This only clears the visible log, not the permanent log files.</p>
        """
    
    def get_manual_sync_content(self):
        """Content for manual sync."""
        return """
        <h2>🔄 Manual Sync</h2>
        <p>Sometimes you want to synchronize immediately without waiting for automatic triggers.</p>
        <h3>How to Use:</h3>
        <ol>
            <li>Go to <strong>File → Manual Sync Now</strong></li>
            <li>Wait for the operation to complete</li>
            <li>Check the Session Log for results</li>
        </ol>
        <h3>When to Use Manual Sync:</h3>
        <ul>
            <li>Before switching AS versions</li>
            <li>After making important changes</li>
            <li>To test if auto-sync is working</li>
            <li>Before closing the application</li>
        </ul>
        <h3>What Happens:</h3>
        <ul>
            <li>Scans for changed files in Libraries directory</li>
            <li>Copies changes back to version-specific storage</li>
            <li>Shows success/failure message</li>
            <li>Updates log with operation details</li>
        </ul>
        """
    
    def get_settings_content(self):
        """Content for settings configuration."""
        return """
        <h2>⚙️ Settings Configuration</h2>
        <p>Access via <strong>Settings → Sync → Auto-Sync Settings...</strong></p>
        <h3>Sync Triggers:</h3>
        <ul>
            <li><strong>Sync when Automation Studio closes</strong> - Recommended: Enabled</li>
            <li><strong>Sync when Selector application closes</strong> - Recommended: Enabled</li>
        </ul>
        <h3>Periodic Sync:</h3>
        <ul>
            <li><strong>Enable periodic sync</strong> - Automatic background syncing</li>
            <li><strong>Check interval</strong> - How often to check (1-60 minutes)</li>
        </ul>
        <h3>Safety & Logging:</h3>
        <ul>
            <li><strong>Log sync operations</strong> - Record all sync activities</li>
            <li><strong>Create backups before sync</strong> - Safety copies</li>
            <li><strong>Max backups</strong> - How many backup versions to keep</li>
        </ul>
        """
    
    def get_status_monitoring_content(self):
        """Content for status monitoring."""
        return """
        <h2>📊 Status Monitoring</h2>
        <p>Access via <strong>Settings → Sync → View Sync Status</strong></p>
        <h3>Information Displayed:</h3>
        <ul>
            <li><strong>Active Studio:</strong> Currently selected AS version</li>
            <li><strong>Files synced this session:</strong> Count of files synchronized</li>
            <li><strong>Total syncs performed:</strong> Lifetime sync operations</li>
            <li><strong>Last sync:</strong> When last sync occurred</li>
            <li><strong>Last check:</strong> When last checked for changes</li>
        </ul>
        <h3>Configuration Summary:</h3>
        <ul>
            <li>Current periodic sync settings</li>
            <li>Sync interval in minutes</li>
            <li>Configuration file location</li>
        </ul>
        """
    
    def get_error_messages_content(self):
        """Content for error messages."""
        return """
        <h2>❌ Error Messages</h2>
        <h3>Common Error Messages:</h3>
        
        <h4>"Source libraries directory not found"</h4>
        <p><strong>Meaning:</strong> Version-specific library folder missing</p>
        <p><strong>Solution:</strong> Create Libraries_45 or Libraries_6 folder in Logical directory</p>
        
        <h4>"Auto-sync failed"</h4>
        <p><strong>Meaning:</strong> Automatic synchronization encountered an error</p>
        <p><strong>Solution:</strong> Check file permissions and disk space</p>
        
        <h4>"Invalid project root"</h4>
        <p><strong>Meaning:</strong> Selected directory doesn't have required structure</p>
        <p><strong>Solution:</strong> Ensure directory contains Logical and Physical folders</p>
        """
    
    def get_log_files_content(self):
        """Content for log files."""
        return """
        <h2>📄 Log Files</h2>
        <p>The application creates detailed log files for troubleshooting.</p>
        <h3>Log Locations:</h3>
        <ul>
            <li><strong>Application logs:</strong> %USERPROFILE%\\.automation_selector\\logs\\application.log</li>
            <li><strong>Session logs:</strong> %USERPROFILE%\\.automation_selector\\logs\\session_YYYYMMDD_HHMMSS.log</li>
        </ul>
        <h3>What's Logged:</h3>
        <ul>
            <li>Application startup and shutdown</li>
            <li>Configuration loading and saving</li>
            <li>All sync operations and results</li>
            <li>Error messages with full details</li>
            <li>File operations and paths</li>
        </ul>
        <h3>When to Check Logs:</h3>
        <ul>
            <li>When troubleshooting issues</li>
            <li>To verify sync operations occurred</li>
            <li>To understand error details</li>
            <li>For support requests</li>
        </ul>
        """
    
    def get_workflow_optimization_content(self):
        """Content for workflow optimization."""
        return """
        <h2>🏆 Workflow Optimization</h2>
        <h3>Best Practices:</h3>
        <ul>
            <li><strong>Leave Selector open:</strong> Keep running for automatic sync</li>
            <li><strong>Use desktop shortcut:</strong> Quick access to application</li>
            <li><strong>Monitor session log:</strong> Watch for sync confirmations</li>
            <li><strong>Regular manual sync:</strong> Before important work sessions</li>
        </ul>
        <h3>Keyboard Shortcuts:</h3>
        <ul>
            <li><strong>F5:</strong> Refresh studio list</li>
            <li><strong>Enter:</strong> Open project (when studio selected)</li>
            <li><strong>Escape:</strong> Close dialogs</li>
        </ul>
        <h3>Time-Saving Tips:</h3>
        <ul>
            <li>Double-click studio version to select and open immediately</li>
            <li>Use File → Manual Sync Now before switching versions</li>
            <li>Check Settings → Sync → View Sync Status regularly</li>
        </ul>
        """
    
    def get_safety_guidelines_content(self):
        """Content for safety guidelines."""
        return """
        <h2>🛡️ Safety Guidelines</h2>
        <h3>Always DO:</h3>
        <ul>
            <li>✅ <strong>Let auto-sync complete</strong> before switching versions</li>
            <li>✅ <strong>Check session log</strong> for sync confirmations</li>
            <li>✅ <strong>Keep backups enabled</strong> for safety</li>
            <li>✅ <strong>Test in both versions</strong> before deploying</li>
        </ul>
        <h3>Never DO:</h3>
        <ul>
            <li>❌ <strong>Edit active files directly</strong> (Libraries, Physical.pkg, OCB.apj)</li>
            <li>❌ <strong>Delete version-specific directories</strong> while AS is running</li>
            <li>❌ <strong>Run multiple AS versions</strong> on same project simultaneously</li>
            <li>❌ <strong>Disable auto-sync</strong> without backup strategy</li>
        </ul>
        <h3>Emergency Procedures:</h3>
        <ul>
            <li>If sync fails: Use File → Manual Sync Now</li>
            <li>If files missing: Check backup directories</li>
            <li>If AS won't start: Verify project structure</li>
        </ul>
        """
    
    def get_performance_tips_content(self):
        """Content for performance tips."""
        return """
        <h2>⚡ Performance Tips</h2>
        <h3>Sync Performance:</h3>
        <ul>
            <li><strong>Adjust sync frequency:</strong> Longer intervals for large projects</li>
            <li><strong>Monitor disk space:</strong> Backups can accumulate</li>
            <li><strong>Clean old logs:</strong> Periodically clean log directories</li>
        </ul>
        <h3>System Performance:</h3>
        <ul>
            <li><strong>Close unused AS:</strong> Don't run multiple versions simultaneously</li>
            <li><strong>Use SSD storage:</strong> Faster file operations</li>
            <li><strong>Sufficient RAM:</strong> Large projects need more memory</li>
        </ul>
        <h3>Project Optimization:</h3>
        <ul>
            <li>Keep projects reasonably sized</li>
            <li>Remove unnecessary files from version-specific directories</li>
            <li>Use descriptive naming for project versions</li>
        </ul>
        """
    
    def get_cli_overview_content(self):
        """Content for CLI overview."""
        return """
        <h2>🖥️ Command Line Interface Overview</h2>
        
        <p>The Automation Studio Selector can be controlled entirely from the command line, perfect for:</p>
        <ul>
            <li><strong>Automation</strong>: Batch processing and scheduled tasks</li>
            <li><strong>Jenkins/CI-CD</strong>: Integration with build pipelines</li>
            <li><strong>Scripting</strong>: Custom workflows and automation</li>
            <li><strong>Remote Operations</strong>: Configure projects without GUI</li>
        </ul>
        
        <h3>Two Operating Modes:</h3>
        
        <h4>1. GUI Mode (No Arguments):</h4>
        <pre>AutomationStudioSelector.exe</pre>
        <p>Opens the graphical interface you're using right now.</p>
        
        <h4>2. CLI Mode (With Arguments):</h4>
        <pre>python main.py -project-path "C:\\Projects\\MyProject" -studio-path "C:\\AS45\\exe" -as-version 45 -prepare-only</pre>
        <p>Executes commands and exits - perfect for automation.</p>
        
        <h3>Key Benefits:</h3>
        <ul>
            <li><strong>No GUI Required</strong>: Works on build servers without desktop</li>
            <li><strong>Scriptable</strong>: Easy to integrate with existing workflows</li>
            <li><strong>Fast</strong>: Direct execution without UI overhead</li>
            <li><strong>Logged</strong>: All operations logged to files</li>
        </ul>
        
        <div style="background-color: #e8f6f3; padding: 15px; border-left: 4px solid #16a085; margin: 15px 0;">
            <strong>Note:</strong> See other CLI topics in this help system for detailed commands and examples.
        </div>
        """
    
    def get_cli_commands_content(self):
        """Content for basic CLI commands."""
        return """
        <h2>📋 Basic CLI Commands</h2>
        
        <h3>Information Commands:</h3>
        <pre>
python main.py -list-projects      List all configured projects
python main.py -list-studios       List all configured AS versions
python main.py -status             Show application status
python main.py -version            Show version information
python main.py -help               Show help message
        </pre>
        
        <h3>Project Operations (With GUI Configuration):</h3>
        <pre>
python main.py OCB AS45            Open OCB project with AS 4.5
python main.py MyProject AS6       Open project with AS 6
        </pre>
        
        <h3>Direct Path Mode (No GUI Configuration Needed):</h3>
        <pre>
python main.py ^
  -project-path "C:\\Path\\To\\Project" ^
  -studio-path "C:\\AS45\\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only
        </pre>
        
        <h3>Common Options:</h3>
        <ul>
            <li><strong>-prepare-only</strong>: Configure files but don't launch AS</li>
            <li><strong>-silent</strong>: No console output (automation mode)</li>
            <li><strong>-verbose</strong>: Detailed output (debugging)</li>
            <li><strong>-wait</strong>: Wait for AS to close before exiting</li>
        </ul>
        
        <h3>Examples:</h3>
        <pre>
REM List all projects
python main.py -list-projects

REM Prepare project without launching AS
python main.py OCB AS45 -prepare-only

REM Full Jenkins command (no GUI config needed)
python main.py -project-path "%WORKSPACE%" -studio-path "C:\\AS45\\exe" -as-version 45 -prepare-only -silent
        </pre>
        """
    
    def get_prepare_only_content(self):
        """Content for prepare-only mode."""
        return """
        <h2>🎯 Prepare-Only Mode</h2>
        
        <p>The <code>-prepare-only</code> flag configures all project files WITHOUT launching Automation Studio.</p>
        
        <h3>What It Does:</h3>
        <ol>
            <li>[OK] Validates project structure</li>
            <li>[OK] Clears Libraries directory</li>
            <li>[OK] Copies version-specific libraries</li>
            <li>[OK] Updates Physical.pkg</li>
            <li>[OK] Updates OCB.apj</li>
            <li>[SKIP] Does NOT launch Automation Studio</li>
        </ol>
        
        <h3>Perfect For:</h3>
        <ul>
            <li><strong>Jenkins/CI builds</strong>: Configure projects on build servers</li>
            <li><strong>Batch processing</strong>: Prepare multiple projects quickly</li>
            <li><strong>Pre-configuration</strong>: Set up before manual opening</li>
            <li><strong>Automated testing</strong>: Configure for test environments</li>
            <li><strong>Remote servers</strong>: No desktop GUI available</li>
        </ul>
        
        <h3>Usage:</h3>
        <pre>
REM Simple form
python main.py MyProject AS45 -prepare-only

REM Jenkins form (no GUI config)
python main.py -project-path "C:\\Jenkins\\workspace\\Build" -studio-path "C:\\AS45\\exe" -as-version 45 -prepare-only -silent
        </pre>
        
        <h3>After Preparation:</h3>
        <p>The project is ready to be opened:</p>
        <ul>
            <li>Double-click OCB.apj in Windows Explorer</li>
            <li>Or launch AS manually with the project file</li>
            <li>All files are configured correctly</li>
        </ul>
        
        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0;">
            <strong>Important:</strong> Prepare-only does all file operations but stops before launching AS.
        </div>
        """
    
    def get_jenkins_content(self):
        """Content for Jenkins & CI/CD."""
        return """
        <h2>🏭 Jenkins & CI/CD Integration</h2>
        
        <p>The Automation Studio Selector is fully compatible with CI/CD pipelines like Jenkins, with NO GUI configuration required.</p>
        
        <h3>The Jenkins Command:</h3>
        <pre>
python main.py ^
  -project-path "%WORKSPACE%" ^
  -studio-path "C:\\BrAutomation\\AS45\\Bin-en\\AutomationStudio.exe" ^
  -as-version 45 ^
  -prepare-only ^
  -silent
        </pre>
        
        <h3>Critical Parameters:</h3>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #f8f9fa;">
                <th style="padding: 8px; border: 1px solid #ddd;">Parameter</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Description</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><code>-project-path</code></td>
                <td style="padding: 8px; border: 1px solid #ddd;">Full path where Git cloned your project</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><code>-studio-path</code></td>
                <td style="padding: 8px; border: 1px solid #ddd;">Full path to AutomationStudio.exe</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><code>-as-version</code></td>
                <td style="padding: 8px; border: 1px solid #ddd;">45 or 6 (which files to copy)</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><code>-prepare-only</code></td>
                <td style="padding: 8px; border: 1px solid #ddd;">Don't launch AS (just prepare files)</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><code>-silent</code></td>
                <td style="padding: 8px; border: 1px solid #ddd;">No console output (clean logs)</td>
            </tr>
        </table>
        
        <h3>Complete Jenkins Workflow:</h3>
        <pre>
@echo off
REM Jenkins Build Script

echo Step 1: Git pull (done by Jenkins)
echo Project at: %WORKSPACE%

echo Step 2: Configure for AS
python main.py -project-path "%WORKSPACE%" -studio-path "C:\\AS45\\exe" -as-version 45 -prepare-only -silent

if %errorlevel% equ 0 (
    echo [OK] Project configured
    REM Step 3: Your build commands here
) else (
    echo [ERROR] Configuration failed
    exit /b 1
)
        </pre>
        
        <h3>Why This Works Without GUI:</h3>
        <ul>
            <li>Uses direct paths - no project name lookup needed</li>
            <li>Specifies AS version explicitly - no config lookup needed</li>
            <li>Self-contained - everything in the command</li>
            <li>Portable - same script works on any build server</li>
        </ul>
        
        <div style="background-color: #e8f6f3; padding: 15px; border-left: 4px solid #16a085; margin: 15px 0;">
            <strong>Pro Tip:</strong> For detailed Jenkins examples and troubleshooting, see JENKINS_QA_GUIDE.md in your installation directory.
        </div>
        """
    
    def get_cli_examples_content(self):
        """Content for CLI examples."""
        return """
        <h2>📝 CLI Examples</h2>
        
        <h3>Example 1: Quick Project Preparation</h3>
        <pre>
REM Prepare OCB project for AS 4.5
python main.py -project-path "C:\\Projects\\OCB" -studio-path "C:\\AS45\\exe" -as-version 45 -prepare-only
        </pre>
        
        <h3>Example 2: Batch Prepare Multiple Projects</h3>
        <pre>
@echo off
for %%P in (Project1 Project2 Project3) do (
    echo Preparing %%P...
    python main.py -project-path "C:\\Projects\\%%P" -studio-path "C:\\AS45\\exe" -as-version 45 -prepare-only -silent
)
echo All projects prepared!
        </pre>
        
        <h3>Example 3: Open and Wait</h3>
        <pre>
REM Open project, wait for user to close AS, then exit
python main.py OCB AS45 -wait
        </pre>
        
        <h3>Example 4: Jenkins Parameterized Build</h3>
        <pre>
@echo off
REM Use Jenkins parameter: AS_VERSION (45 or 6)

if "%AS_VERSION%"=="45" (
    set AS_EXE=C:\\AS45\\AutomationStudio.exe
) else (
    set AS_EXE=C:\\AS6\\AutomationStudio.exe
)

python main.py -project-path "%WORKSPACE%" -studio-path "%AS_EXE%" -as-version %AS_VERSION% -prepare-only -silent
        </pre>
        
        <h3>Example 5: Git Clone and Configure</h3>
        <pre>
@echo off
REM Complete workflow from Git to ready project

cd C:\\Temp
git clone https://repo.git MyProject
cd MyProject

python main.py -project-path "%CD%" -studio-path "C:\\AS45\\exe" -as-version 45 -prepare-only

echo Project ready at: %CD%\\OCB.apj
        </pre>
        """
    
    def get_step_by_step_content(self):
        """Content for step-by-step process."""
        return """
        <h2>🔍 What Happens Step-by-Step</h2>
        
        <p>Understanding the complete process the Selector performs:</p>
        
        <h3>Step 1: Validate Project Structure</h3>
        <ul>
            <li>Checks if project directory exists</li>
            <li>Verifies Logical folder exists</li>
            <li>Verifies Physical folder exists</li>
            <li>If validation fails, process stops immediately</li>
        </ul>
        
        <h3>Step 2: Clear Libraries Directory</h3>
        <ul>
            <li>Goes to: Logical\\Libraries\\</li>
            <li>Deletes ALL files and subdirectories inside</li>
            <li>Keeps the Libraries folder itself (empties it)</li>
            <li>Why: Removes old files from previous AS version</li>
        </ul>
        
        <h3>Step 3: Copy Version-Specific Libraries</h3>
        <p><strong>For AS 4.5:</strong></p>
        <ul>
            <li>Source: Logical\\Libraries_45\\</li>
            <li>Target: Logical\\Libraries\\</li>
            <li>Copies: ALL files and subdirectories</li>
        </ul>
        <p><strong>For AS 6:</strong></p>
        <ul>
            <li>Source: Logical\\Libraries_6\\</li>
            <li>Target: Logical\\Libraries\\</li>
            <li>Copies: ALL files and subdirectories</li>
        </ul>
        
        <h3>Step 4: Update Physical.pkg</h3>
        <p><strong>For AS 4.5:</strong></p>
        <ul>
            <li>Delete: Physical\\Physical.pkg (if exists)</li>
            <li>Copy: Physical_45.pkg -> Physical.pkg</li>
        </ul>
        <p><strong>For AS 6:</strong></p>
        <ul>
            <li>Delete: Physical\\Physical.pkg (if exists)</li>
            <li>Copy: Physical_6.pkg -> Physical.pkg</li>
        </ul>
        
        <h3>Step 5: Update OCB.apj</h3>
        <p><strong>For AS 4.5:</strong></p>
        <ul>
            <li>Delete: OCB.apj (if exists)</li>
            <li>Copy: OCB_as45.apj -> OCB.apj</li>
        </ul>
        <p><strong>For AS 6:</strong></p>
        <ul>
            <li>Delete: OCB.apj (if exists)</li>
            <li>Copy: OCB_as6.apj -> OCB.apj</li>
        </ul>
        
        <h3>Step 6: Launch Automation Studio (Full Mode Only)</h3>
        <p><strong>Full Procedure:</strong></p>
        <ul>
            <li>Launches: AutomationStudio.exe with project file</li>
            <li>AS opens with your configured project</li>
        </ul>
        <p><strong>Prepare-Only Mode:</strong></p>
        <ul>
            <li>SKIPS this step</li>
            <li>Files ready but AS not launched</li>
        </ul>
        
        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0;">
            <strong>Important:</strong> Version-specific files (Libraries_45, Physical_45.pkg, OCB_as45.apj) are NEVER modified - they're your source templates.
        </div>
        """
    
    def get_file_operations_content(self):
        """Content for file operations."""
        return """
        <h2>📁 File Operations Explained</h2>
        
        <h3>Files Modified (Active Work Files):</h3>
        <table style="width:100%; border-collapse: collapse; margin: 15px 0;">
            <tr style="background-color: #f8f9fa;">
                <th style="padding: 8px; border: 1px solid #ddd;">File/Folder</th>
                <th style="padding: 8px; border: 1px solid #ddd;">What Happens</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Logical/Libraries/</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">Entire contents replaced from Libraries_45 or Libraries_6</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Physical/Physical.pkg</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">Deleted and replaced from Physical_45.pkg or Physical_6.pkg</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>OCB.apj</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">Deleted and replaced from OCB_as45.apj or OCB_as6.apj</td>
            </tr>
        </table>
        
        <h3>Files NEVER Modified (Source Templates):</h3>
        <table style="width:100%; border-collapse: collapse; margin: 15px 0;">
            <tr style="background-color: #f8f9fa;">
                <th style="padding: 8px; border: 1px solid #ddd;">File/Folder</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Purpose</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Logical/Libraries_45/</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">AS 4.5 source template - always preserved</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Logical/Libraries_6/</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">AS 6 source template - always preserved</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Physical/Physical_45.pkg</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">AS 4.5 source - always preserved</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Physical/Physical_6.pkg</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">AS 6 source - always preserved</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>OCB_as45.apj</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">AS 4.5 source - always preserved</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>OCB_as6.apj</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">AS 6 source - always preserved</td>
            </tr>
        </table>
        
        <h3>The Flow:</h3>
        <p><strong>Example for AS 4.5:</strong></p>
        <pre>
Libraries_45/ (source) -> Libraries/ (active)
Physical_45.pkg        -> Physical.pkg
OCB_as45.apj           -> OCB.apj

Result: Project configured for AS 4.5
        </pre>
        
        <div style="background-color: #e8f6f3; padding: 15px; border-left: 4px solid #16a085; margin: 15px 0;">
            <strong>Key Concept:</strong> The Selector manages "active" files (Libraries, Physical.pkg, OCB.apj) automatically. You work with version-specific templates (Libraries_45, Physical_45.pkg, OCB_as45.apj) which are never modified.
        </div>
        """
    
    def get_multiple_projects_content(self):
        """Content for multiple projects."""
        return """
        <h2>🗂️ Working with Multiple Projects</h2>
        
        <p>The Selector now supports managing multiple projects easily.</p>
        
        <h3>Adding Projects:</h3>
        <ol>
            <li>Click <strong>"Add Project..."</strong> button</li>
            <li>Browse to your project directory</li>
            <li>Enter a friendly name (e.g., "Production Line")</li>
            <li>Optionally add a description</li>
            <li>Project is added to your list</li>
        </ol>
        
        <h3>Switching Between Projects:</h3>
        <ol>
            <li>Click on any project in the Project Selection list</li>
            <li>Project becomes active immediately</li>
            <li>Select your AS version</li>
            <li>Click "Open Project"</li>
        </ol>
        
        <h3>Project List Features:</h3>
        <ul>
            <li><strong>Multiple Projects</strong>: Add as many as you need</li>
            <li><strong>Quick Switching</strong>: One click to change active project</li>
            <li><strong>Remembered</strong>: Last used project auto-selected</li>
            <li><strong>Descriptions</strong>: Add notes to identify projects</li>
        </ul>
        
        <h3>Workflow Example:</h3>
        <pre>
Morning: Click "Production" -> Select AS 4.5 -> Open Project
Afternoon: Click "Development" -> Select AS 6 -> Open Project  
Evening: Click "Testing" -> Select AS 4.5 -> Open Project
        </pre>
        
        <p>Each project maintains its own version-specific files and auto-sync tracks changes separately.</p>
        
        <h3>CLI Support:</h3>
        <p>You can also manage projects via CLI:</p>
        <pre>
python main.py -add-project "NewProj" "C:\\Projects\\New"
python main.py -remove-project "OldProj"
python main.py -list-projects
        </pre>
        """
