"""Main application module for Task Manager.
Modern desktop application for managing tasks efficiently.
"""

import sys
from datetime import datetime, timedelta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QDateEdit, QTimeEdit, QGroupBox, QScrollArea, QFrame,
    QTabWidget, QMessageBox, QMenuBar, QMenu, QStatusBar,
    QGridLayout, QDialog, QFormLayout, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
# Add QIcon to the imports:
from PyQt6.QtGui import QFont, QIcon, QAction

from utils import resource_path
from database import DatabaseManager
from widgets import TaskWidget, StatisticsWidget
from styles import MAIN_STYLESHEET, DARK_STYLESHEET


class AddTaskDialog(QDialog):
    """Dialog for adding/editing tasks."""
    
    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)
        self.task_data = task_data
        self.is_edit_mode = task_data is not None
        self.init_ui()
        self.setWindowTitle("Edit Task" if self.is_edit_mode else "Add New Task")
        self.setMinimumWidth(400)
    
    def init_ui(self):
        """Initialize dialog UI."""
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # Title field
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title...")
        if self.is_edit_mode:
            self.title_input.setText(self.task_data.get('title', ''))
        form_layout.addRow("Title:", self.title_input)
        
        # Description field
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        if self.is_edit_mode:
            self.desc_input.setText(self.task_data.get('description', ''))
        form_layout.addRow("Description:", self.desc_input)
        
        # Priority field
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["High", "Medium", "Low"])
        if self.is_edit_mode:
            priority_map = {1: "High", 2: "Medium", 3: "Low"}
            current_priority = priority_map.get(self.task_data.get('priority', 2), "Medium")
            self.priority_combo.setCurrentText(current_priority)
        else:
            self.priority_combo.setCurrentText("Medium")
        form_layout.addRow("Priority:", self.priority_combo)
        
        # Category field
        self.category_combo = QComboBox()
        if self.is_edit_mode:
            self.category_combo.setCurrentText(self.task_data.get('category', 'General'))
        form_layout.addRow("Category:", self.category_combo)
        
        # Due date and time
        due_date_layout = QHBoxLayout()
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDateTime.currentDateTime().date().addDays(1))
        
        self.time_input = QTimeEdit()
        self.time_input.setTime(QDateTime.currentDateTime().time())
        
        due_date_layout.addWidget(self.date_input)
        due_date_layout.addWidget(QLabel("at"))
        due_date_layout.addWidget(self.time_input)
        
        form_layout.addRow("Due Date:", due_date_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def set_categories(self, categories):
        """Set available categories."""
        self.category_combo.clear()
        for category in categories:
            self.category_combo.addItem(category['name'])
        self.category_combo.setCurrentText('General')
    
    def get_task_data(self):
        """Get task data from dialog inputs."""
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        
        # Combine date and time
        due_date = QDateTime(
            self.date_input.date(),
            self.time_input.time()
        )
        
        return {
            'title': self.title_input.text().strip(),
            'description': self.desc_input.toPlainText().strip(),
            'priority': priority_map.get(self.priority_combo.currentText(), 2),
            'due_date': due_date.toString(Qt.DateFormat.ISODate),
            'category': self.category_combo.currentText()
        }

class AddCategoryDialog(QDialog):
    """Dialog for adding new categories."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle("Add New Category")
    
    def init_ui(self):
        """Initialize dialog UI."""
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter category name...")
        form_layout.addRow("Category Name:", self.name_input)
        
        # Color selection
        self.color_combo = QComboBox()
        colors = [
            ("Blue", "#3498db"),
            ("Red", "#e74c3c"),
            ("Green", "#2ecc71"),
            ("Orange", "#f39c12"),
            ("Purple", "#9b59b6"),
            ("Teal", "#1abc9c")
        ]
        for color_name, color_code in colors:
            self.color_combo.addItem(color_name, color_code)
        form_layout.addRow("Color:", self.color_combo)
        
        layout.addLayout(form_layout)
        
        # Preview
        self.preview_label = QLabel("Preview")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet(f"""
            background-color: {colors[0][1]};
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
        layout.addWidget(self.preview_label)
        
        # Connect color change
        self.color_combo.currentIndexChanged.connect(self.update_preview)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def update_preview(self):
        """Update preview label with selected color."""
        color_code = self.color_combo.currentData()
        self.preview_label.setStyleSheet(f"""
            background-color: {color_code};
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
    
    def get_category_data(self):
        """Get category data from dialog inputs."""
        return {
            'name': self.name_input.text().strip(),
            'color': self.color_combo.currentData()
        }

class TaskManagerApp(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_filter = "All"
        self.dark_mode = False
        self.init_ui()
        #self.load_categories()
        self.load_tasks()
        self.update_statistics()
    
    def init_ui(self):
        """Initialize the main UI."""
        self.setWindowTitle("")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Header section
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Statistics widget
        self.stats_widget = QWidget()
        main_layout.addWidget(self.stats_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Pending tasks tab
        self.pending_tab = QWidget()
        self.setup_pending_tab()
        self.tab_widget.addTab(self.pending_tab, "📋 Pending Tasks")
        
        # Completed tasks tab
        self.completed_tab = QWidget()
        self.setup_completed_tab()
        self.tab_widget.addTab(self.completed_tab, "✅ Completed Tasks")
        
        main_layout.addWidget(self.tab_widget)
        
        # Apply styles
        self.apply_styles()
        
        # Setup auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
    
    def create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_task_action = QAction("New Task", self)
        new_task_action.triggered.connect(self.show_add_task_dialog)
        new_task_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_task_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export Tasks", self)
        export_action.triggered.connect(self.export_tasks)
        file_menu.addAction(export_action)
        
        import_action = QAction("Import Tasks", self)
        import_action.triggered.connect(self.import_tasks)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        dark_mode_action = QAction("Toggle Dark Mode", self)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        dark_mode_action.setShortcut("Ctrl+D")
        view_menu.addAction(dark_mode_action)
        
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_tasks)
        refresh_action.setShortcut("F5")
        view_menu.addAction(refresh_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        add_category_action = QAction("Add Category", self)
        add_category_action.triggered.connect(self.show_add_category_dialog)
        tools_menu.addAction(add_category_action)
        
        stats_action = QAction("Show Statistics", self)
        stats_action.triggered.connect(self.show_statistics_dialog)
        tools_menu.addAction(stats_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        docs_action = QAction("Documentation", self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
    
    def create_header(self):
        """Create header widget with search functionality only."""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Title (completely removed - just empty space)
        title_label = QLabel("")  # Empty label
        header_layout.addWidget(title_label)
        
        # Add space on left
        header_layout.addStretch()
        
        # ===== SEARCH SECTION (CENTER) =====
        search_widget = QFrame()
        search_widget.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(10, 5, 10, 5)
        
        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks by title, description or category...")
        self.search_input.setMinimumWidth(400)  # Wider search box
        # Connect to search function when text changes
        self.search_input.textChanged.connect(self.search_tasks)
        search_layout.addWidget(self.search_input)
        
        # Search button
        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(self.search_tasks)
        search_layout.addWidget(search_btn)
        
        # Clear search button
        clear_search_btn = QPushButton("✕ Clear")
        clear_search_btn.clicked.connect(self.clear_search)
        clear_search_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        search_layout.addWidget(clear_search_btn)
        
        # Add search widget to header
        header_layout.addWidget(search_widget)
        
        # Add space on right
        header_layout.addStretch()
        
        return header_widget
    
    def setup_pending_tab(self):
        """Setup pending tasks tab."""
        layout = QVBoxLayout(self.pending_tab)
        
        # Tasks container with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.pending_container = QWidget()
        self.pending_layout = QVBoxLayout(self.pending_container)
        self.pending_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.pending_container)
        layout.addWidget(scroll_area)
    
    def setup_completed_tab(self):
        """Setup completed tasks tab."""
        layout = QVBoxLayout(self.completed_tab)
        
        # Clear completed button
        clear_btn = QPushButton("Clear All Completed Tasks")
        clear_btn.clicked.connect(self.clear_completed_tasks)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(clear_btn)
        
        # Tasks container with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.completed_container = QWidget()
        self.completed_layout = QVBoxLayout(self.completed_container)
        self.completed_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.completed_container)
        layout.addWidget(scroll_area)
    
    def load_categories(self):
        """Load categories from database."""
        categories = self.db.get_categories()
        #self.filter_combo.clear()
        #self.filter_combo.addItem("All Categories")
        #for category in categories:
        #    self.filter_combo.addItem(category['name'])
        pass # Just do nothing for now
    
    def load_tasks(self):
        """Load tasks from database."""
        # Clear existing tasks
        self.clear_layout(self.pending_layout)
        self.clear_layout(self.completed_layout)
        
        # Load pending tasks
        pending_tasks = self.db.get_tasks(completed=False)
        for task_data in pending_tasks:
            task_widget = TaskWidget(task_data)
            task_widget.task_updated.connect(self.update_task)
            task_widget.task_deleted.connect(self.delete_task)
            self.pending_layout.addWidget(task_widget)
        
        # Load completed tasks
        completed_tasks = self.db.get_tasks(completed=True)
        for task_data in completed_tasks:
            task_widget = TaskWidget(task_data)
            task_widget.task_updated.connect(self.update_task)
            task_widget.task_deleted.connect(self.delete_task)
            self.completed_layout.addWidget(task_widget)
        
        # Add stretch to push tasks to top
        self.pending_layout.addStretch()
        self.completed_layout.addStretch()
        
        # Update status bar
        pending_count = len(pending_tasks)
        completed_count = len(completed_tasks)
        self.status_bar.showMessage(f"Loaded {pending_count} pending and {completed_count} completed tasks")
    
    def update_task(self, task_id: int, changes: dict):
        """Update task in database."""
        self.db.update_task(task_id, **changes)
        self.load_tasks()
        self.update_statistics()
        
        if 'completed' in changes:
            status = "completed" if changes['completed'] else "marked as pending"
            self.status_bar.showMessage(f"Task {status} successfully")
    
    def delete_task(self, task_id: int):
        """Delete task from database."""
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this task?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_task(task_id)
            self.load_tasks()
            self.update_statistics()
            self.status_bar.showMessage("Task deleted successfully")
    
    def add_quick_task(self):
        """Add a quick task from the input field."""
        title = self.quick_task_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Warning", "Please enter a task title")
            return
        
        task_id = self.db.add_task(title=title)
        self.quick_task_input.clear()
        self.load_tasks()
        self.update_statistics()
        self.status_bar.showMessage("Task added successfully")
    
    def show_add_task_dialog(self):
        """Show dialog to add a new task."""
        dialog = AddTaskDialog(self)
        dialog.set_categories(self.db.get_categories())
        
        if dialog.exec():
            task_data = dialog.get_task_data()
            
            if not task_data['title']:
                QMessageBox.warning(self, "Warning", "Please enter a task title")
                return
            
            task_id = self.db.add_task(**task_data)
            self.load_tasks()
            self.update_statistics()
            self.status_bar.showMessage("Task added successfully")
    
    def show_add_category_dialog(self):
        """Show dialog to add a new category."""
        dialog = AddCategoryDialog(self)
        
        if dialog.exec():
            category_data = dialog.get_category_data()
            
            if not category_data['name']:
                QMessageBox.warning(self, "Warning", "Please enter a category name")
                return
            
            self.db.add_category(**category_data)
            self.load_categories()
            self.status_bar.showMessage("Category added successfully")
        
    def update_statistics(self):
        """Update statistics widget."""
        stats = self.db.get_task_statistics()
        
        # Clear existing statistics
        self.clear_layout(self.stats_widget.layout())
        
        # Create new statistics layout
        stats_layout = QVBoxLayout(self.stats_widget)
        stats_widget = StatisticsWidget(stats)
        stats_layout.addWidget(stats_widget)
    
    def clear_completed_tasks(self):
        """Clear all completed tasks."""
        reply = QMessageBox.question(
            self, 'Confirm Clear',
            'Are you sure you want to clear all completed tasks?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Delete all completed tasks
            cursor = self.db.conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE completed = 1")
            self.db.conn.commit()
            
            self.load_tasks()
            self.update_statistics()
            self.status_bar.showMessage("Completed tasks cleared successfully")
    
    def clear_layout(self, layout):
        """Clear all widgets from a layout."""
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
    
    def toggle_dark_mode(self):
        """Toggle dark mode."""
        self.dark_mode = not self.dark_mode
        self.apply_styles()
        
        mode = "Dark" if self.dark_mode else "Light"
        self.status_bar.showMessage(f"Switched to {mode} mode")
    
    def apply_styles(self):
        """Apply stylesheet to application."""
        stylesheet = DARK_STYLESHEET if self.dark_mode else MAIN_STYLESHEET
        self.setStyleSheet(stylesheet)
    
    def refresh_tasks(self):
        """Refresh tasks from database."""
        self.load_tasks()
        self.update_statistics()
        self.status_bar.showMessage("Tasks refreshed")
    
    def auto_save(self):
        """Auto-save current state."""
        # In a real application, you might save unsaved changes here
        # For now, just update the status bar
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_bar.showMessage(f"Auto-saved at {current_time}")
    
    def export_tasks(self):
        """Export tasks to file."""
        # Implementation for exporting tasks
        QMessageBox.information(self, "Export", "Export feature coming soon!")
    
    def import_tasks(self):
        """Import tasks from file."""
        # Implementation for importing tasks
        QMessageBox.information(self, "Import", "Import feature coming soon!")
    
    def show_statistics_dialog(self):
        """Show detailed statistics dialog."""
        stats = self.db.get_task_statistics()
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Detailed Statistics")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Create detailed statistics
        stats_text = f"""
        📊 Task Statistics
        
        Total Tasks: {stats['total']}
        Pending Tasks: {stats['pending']}
        Completed Tasks: {stats['completed']}
        High Priority Tasks: {stats['high_priority']}
        Overdue Tasks: {stats['overdue']}
        
        Completion Rate: {stats['completed'] / stats['total'] * 100 if stats['total'] > 0 else 0:.1f}%
        """
        
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet("font-family: monospace; padding: 20px;")
        layout.addWidget(stats_label)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def show_about_dialog(self):
        """Show about dialog."""
        about_text = """
        <h2>Modern Task Manager</h2>
        <p>Version 1.0.0</p>
        <p>A modern desktop application for managing your tasks efficiently.</p>
        <p>Built with PyQt6 and SQLite</p>
        <p>© 2024 Modern Task Manager. All rights reserved.</p>
        """
        
        QMessageBox.about(self, "About Modern Task Manager", about_text)
    
    def show_documentation(self):
        """Show documentation."""
        doc_text = """
        <h2>Task Manager Documentation</h2>
        
        <h3>Features:</h3>
        <ul>
        <li>Add, edit, and delete tasks</li>
        <li>Set priorities (High, Medium, Low)</li>
        <li>Add due dates and times</li>
        <li>Categorize tasks</li>
        <li>Mark tasks as complete</li>
        <li>Filter by category</li>
        <li>View statistics</li>
        <li>Dark/Light mode</li>
        </ul>
        
        <h3>Keyboard Shortcuts:</h3>
        <ul>
        <li>Ctrl+N: New Task</li>
        <li>Ctrl+Q: Exit</li>
        <li>Ctrl+D: Toggle Dark Mode</li>
        <li>F5: Refresh</li>
        </ul>
        """
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Documentation")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(doc_text)
        layout.addWidget(text_edit)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def closeEvent(self, event):
        """Handle application close event."""
        reply = QMessageBox.question(
            self, 'Confirm Exit',
            'Are you sure you want to exit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.close()
            event.accept()
        else:
            event.ignore()

    def search_tasks(self):
        """Search tasks by keyword in title, description, or category."""
        # Get search text and convert to lowercase for case-insensitive search
        search_text = self.search_input.text().strip().lower()
        
        # If search is empty, reload all tasks normally
        if not search_text:
            self.load_tasks()
            self.status_bar.showMessage("Showing all tasks")
            return
        
        # Clear current task displays
        self.clear_layout(self.pending_layout)
        self.clear_layout(self.completed_layout)
        
        # Get all tasks from database (both pending and completed)
        # First get pending tasks
        pending_tasks = self.db.get_tasks(completed=False)
        
        # Then get completed tasks
        completed_tasks = self.db.get_tasks(completed=True)
        
        # Combine all tasks
        all_tasks = pending_tasks + completed_tasks
        
        # Filter tasks based on search text
        found_tasks = []
        for task in all_tasks:
            # Check if search text is in title (case-insensitive)
            title_match = search_text in task['title'].lower()
            
            # Check if search text is in description (case-insensitive)
            desc_match = False
            if task.get('description'):
                desc_match = search_text in task['description'].lower()
            
            # Check if search text is in category (case-insensitive)
            category_match = search_text in task.get('category', '').lower()
            
            # If any match found, include this task
            if title_match or desc_match or category_match:
                found_tasks.append(task)
        
        # Separate found tasks into pending and completed
        found_pending = [t for t in found_tasks if not t['completed']]
        found_completed = [t for t in found_tasks if t['completed']]
        
        # Display found pending tasks
        for task_data in found_pending:
            task_widget = TaskWidget(task_data)
            task_widget.task_updated.connect(self.update_task)
            task_widget.task_deleted.connect(self.delete_task)
            self.pending_layout.addWidget(task_widget)
        
        # Display found completed tasks
        for task_data in found_completed:
            task_widget = TaskWidget(task_data)
            task_widget.task_updated.connect(self.update_task)
            task_widget.task_deleted.connect(self.delete_task)
            self.completed_layout.addWidget(task_widget)
        
        # Add stretch to push tasks to top
        self.pending_layout.addStretch()
        self.completed_layout.addStretch()
        
        # Update status message
        count = len(found_tasks)
        self.status_bar.showMessage(f"Found {count} task(s) matching '{search_text}'")

    def clear_search(self):
        """Clear search input and show all tasks."""
        self.search_input.clear()
        self.load_tasks()
        self.status_bar.showMessage("Showing all tasks")

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Task Manager")
    app.setOrganizationName("TaskManager Inc.")
    
    # Set application style
    app.setStyle("Fusion")

    # Set application icon
    try:
        icon_path = resource_path("assets/task64.ico")
        app.setWindowIcon(QIcon(icon_path))
    except:
        pass
    
    window = TaskManagerApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()