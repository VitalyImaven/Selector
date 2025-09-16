"""
Modern styling for the Automation Studio Selector UI.
"""

MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
    color: #333333;
}

QLabel {
    color: #333333;
    font-size: 14px;
    font-weight: 500;
}

QLabel#title {
    font-size: 24px;
    font-weight: 700;
    color: #2c3e50;
    margin: 20px 0px;
}

QLabel#subtitle {
    font-size: 16px;
    color: #7f8c8d;
    margin-bottom: 20px;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
    min-width: 120px;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #21618c;
}

QPushButton:disabled {
    background-color: #bdc3c7;
    color: #7f8c8d;
}

QPushButton#primary {
    background-color: #27ae60;
    min-width: 150px;
    min-height: 45px;
    font-size: 16px;
}

QPushButton#primary:hover {
    background-color: #229954;
}

QPushButton#secondary {
    background-color: #95a5a6;
}

QPushButton#secondary:hover {
    background-color: #7f8c8d;
}

QPushButton#danger {
    background-color: #e74c3c;
}

QPushButton#danger:hover {
    background-color: #c0392b;
}

QListWidget {
    background-color: white;
    border: 2px solid #ecf0f1;
    border-radius: 8px;
    padding: 8px;
    font-size: 14px;
    selection-background-color: #16a085;
    selection-color: white;
    outline: none;
}

QListWidget::item {
    padding: 12px;
    border-bottom: 1px solid #ecf0f1;
    border-radius: 4px;
    margin: 2px 0px;
}

QListWidget::item:hover {
    background-color: #f0f8ff;
}

QListWidget::item:selected {
    background-color: #16a085;
    color: white;
}

QGroupBox {
    font-size: 16px;
    font-weight: 600;
    color: #2c3e50;
    border: 2px solid #bdc3c7;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    background-color: #f5f5f5;
}

QLineEdit {
    background-color: white;
    border: 2px solid #ecf0f1;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: #333333;
}

QLineEdit:focus {
    border-color: #3498db;
}

QTextEdit {
    background-color: white;
    border: 2px solid #ecf0f1;
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
    color: #333333;
    font-family: 'Consolas', 'Monaco', monospace;
}

QProgressBar {
    border: 2px solid #ecf0f1;
    border-radius: 8px;
    text-align: center;
    background-color: #ecf0f1;
}

QProgressBar::chunk {
    background-color: #3498db;
    border-radius: 6px;
}

QStatusBar {
    background-color: #34495e;
    color: white;
    font-size: 12px;
}

QMenuBar {
    background-color: #2c3e50;
    color: white;
    font-size: 14px;
}

QMenuBar::item {
    padding: 8px 16px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #34495e;
}

QMenu {
    background-color: white;
    border: 1px solid #bdc3c7;
    color: #333333;
}

QMenu::item {
    padding: 8px 16px;
}

QMenu::item:selected {
    background-color: #3498db;
    color: white;
}
"""
