"""
Stylesheet definitions for Task Manager application.
"""

MAIN_STYLESHEET = """
/* Main window styling */
QMainWindow {
    background-color: #f8f9fa;
}

/* Button styles */
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 12px;
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

/* Line edit styles */
QLineEdit {
    padding: 8px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    font-size: 13px;
}

QLineEdit:focus {
    border: 2px solid #3498db;
    outline: none;
}

/* Combo box styles */
QComboBox {
    padding: 6px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: white;
    font-size: 13px;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    border: 1px solid #bdc3c7;
    selection-background-color: #3498db;
    selection-color: white;
}

/* Checkbox styles */
QCheckBox {
    spacing: 8px;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    border: 2px solid #bdc3c7;
    border-radius: 3px;
    background-color: white;
}

QCheckBox::indicator:checked {
    border: 2px solid #2ecc71;
    border-radius: 3px;
    background-color: #2ecc71;
    image: url('checkmark.png');
}

/* Tab widget styles */
QTabWidget::pane {
    border: 1px solid #dee2e6;
    background-color: white;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #e9ecef;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: 2px solid #3498db;
}

QTabBar::tab:hover:!selected {
    background-color: #dee2e6;
}

/* Scroll area styles */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background-color: #f8f9fa;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #bdc3c7;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #95a5a6;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

/* Group box styles */
QGroupBox {
    border: 1px solid #dee2e6;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: bold;
    padding-top: 10px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

/* Label styles */
QLabel {
    font-size: 13px;
}

/* Text edit styles */
QTextEdit {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    font-size: 13px;
    padding: 4px;
}

QTextEdit:focus {
    border: 2px solid #3498db;
}

/* Date edit styles */
QDateEdit {
    padding: 6px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: white;
    font-size: 13px;
}

/* Menu bar styles */
QMenuBar {
    background-color: #2c3e50;
    color: white;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #3498db;
}

QMenu {
    background-color: white;
    border: 1px solid #bdc3c7;
}

QMenu::item {
    padding: 6px 20px;
}

QMenu::item:selected {
    background-color: #3498db;
    color: white;
}

/* Status bar styles */
QStatusBar {
    background-color: #2c3e50;
    color: white;
    font-size: 11px;
}

/* Progress bar styles */
QProgressBar {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    text-align: center;
    background-color: #ecf0f1;
}

QProgressBar::chunk {
    background-color: #2ecc71;
    border-radius: 3px;
}
"""

DARK_STYLESHEET = """
/* Dark theme styles */
QMainWindow {
    background-color: #1a1a1a;
    color: #ffffff;
}

QWidget {
    background-color: #2d2d2d;
    color: #ffffff;
}

QLineEdit, QTextEdit, QComboBox, QDateEdit {
    background-color: #3d3d3d;
    color: #ffffff;
    border: 1px solid #555555;
}

QPushButton {
    background-color: #3498db;
    color: white;
}

QPushButton:hover {
    background-color: #2980b9;
}

QTabBar::tab {
    background-color: #3d3d3d;
    color: #ffffff;
}

QTabBar::tab:selected {
    background-color: #2d2d2d;
    color: #3498db;
}

QGroupBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #555555;
}

QScrollBar:vertical {
    background-color: #2d2d2d;
}

QScrollBar::handle:vertical {
    background-color: #555555;
}

QMenuBar {
    background-color: #1a1a1a;
}

QMenu {
    background-color: #2d2d2d;
    border: 1px solid #555555;
}
"""