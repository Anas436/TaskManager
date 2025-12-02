"""
Custom widgets for Task Manager application.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

class TaskWidget(QFrame):
    """Custom widget for displaying a single task."""
    task_updated = pyqtSignal(int, dict)  # task_id, changes
    task_deleted = pyqtSignal(int)  # task_id
    
    def __init__(self, task_data: dict):
        super().__init__()
        self.task_id = task_data['id']
        self.task_data = task_data
        self.init_ui()
        self.setup_styles()
    
    def init_ui(self):
        """Initialize UI components."""
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setMinimumHeight(80)
        
        main_layout = QHBoxLayout()
        
        # Left side: Checkbox and task info
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 5, 5, 5)
        
        # Title with priority indicator
        title_layout = QHBoxLayout()
        
        # Priority indicator
        priority_color = {
            1: "#e74c3c", 2: "#f39c12", 3: "#2ecc71"
        }.get(self.task_data['priority'], "#f39c12")
        
        priority_label = QLabel("●")
        priority_label.setStyleSheet(f"color: {priority_color}; font-size: 16px;")
        title_layout.addWidget(priority_label)
        
        # Title
        title_label = QLabel(self.task_data['title'])
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(11)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        left_layout.addLayout(title_layout)
        
        # Description
        if self.task_data.get('description'):
            desc_label = QLabel(self.task_data['description'])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #666; font-size: 10px;")
            left_layout.addWidget(desc_label)
        
        # Category and due date
        info_layout = QHBoxLayout()
        
        # Category
        category_label = QLabel(self.task_data.get('category', 'General'))
        category_label.setStyleSheet(f"""
            background-color: {self.get_category_color(self.task_data.get('category'))};
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 9px;
        """)
        info_layout.addWidget(category_label)
        
        # Due date
        if self.task_data.get('due_date'):
            due_date = self.task_data['due_date'][:10]  # Just show date
            due_label = QLabel(f"📅 {due_date}")
            due_label.setStyleSheet("color: #666; font-size: 9px;")
            info_layout.addWidget(due_label)
        
        info_layout.addStretch()
        left_layout.addLayout(info_layout)
        
        # Right side: Action buttons
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 5, 10, 5)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Complete checkbox
        self.complete_checkbox = QCheckBox("Complete")
        self.complete_checkbox.setChecked(bool(self.task_data['completed']))
        self.complete_checkbox.stateChanged.connect(self.toggle_complete)
        right_layout.addWidget(self.complete_checkbox)
        
        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_btn.clicked.connect(self.delete_task)
        right_layout.addWidget(delete_btn)
        
        # Add widgets to main layout
        main_layout.addWidget(left_widget, 4)
        main_layout.addWidget(right_widget, 1)
        
        self.setLayout(main_layout)
    
    def get_category_color(self, category_name: str) -> str:
        """Get color for category."""
        category_colors = {
            'Work': '#e74c3c',
            'Personal': '#2ecc71',
            'Shopping': '#f39c12',
            'Health': '#9b59b6',
            'Finance': '#1abc9c',
            'General': '#3498db'
        }
        return category_colors.get(category_name, '#3498db')
    
    def setup_styles(self):
        """Setup widget styles."""
        if self.task_data['completed']:
            self.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                }
                QLabel {
                    color: #999 !important;
                    text-decoration: line-through;
                }
            """)
        elif self.task_data.get('due_date') and self.is_overdue():
            self.setStyleSheet("""
                QFrame {
                    background-color: #fff5f5;
                    border: 1px solid #e74c3c;
                    border-radius: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                }
                QFrame:hover {
                    border-color: #3498db;
                    background-color: #f8fafc;
                }
            """)
    
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.task_data.get('due_date'):
            return False
        
        from datetime import datetime
        try:
            due = datetime.fromisoformat(self.task_data['due_date'])
            return due < datetime.now() and not self.task_data['completed']
        except:
            return False
    
    def toggle_complete(self, state):
        """Toggle task completion status."""
        completed = state == 2  # Qt.Checked = 2
        self.task_updated.emit(self.task_id, {'completed': completed})
        self.setup_styles()  # Update styles
    
    def delete_task(self):
        """Delete this task."""
        self.task_deleted.emit(self.task_id)

class StatisticsWidget(QWidget):
    """Widget for displaying task statistics."""
    
    def __init__(self, stats: dict):
        super().__init__()
        self.stats = stats
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components."""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Create stat cards
        stat_cards = [
            ("Total Tasks", self.stats.get('total', 0), "#3498db"),
            ("Pending", self.stats.get('pending', 0), "#f39c12"),
            ("Completed", self.stats.get('completed', 0), "#2ecc71"),
            ("High Priority", self.stats.get('high_priority', 0), "#e74c3c"),
            ("Overdue", self.stats.get('overdue', 0), "#9b59b6")
        ]
        
        for title, value, color in stat_cards:
            card = self.create_stat_card(title, value, color)
            layout.addWidget(card)
        
        self.setLayout(layout)
    
    def create_stat_card(self, title: str, value: int, color: str) -> QWidget:
        """Create a single statistic card."""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                border-top: 4px solid {color};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Value
        value_label = QLabel(str(value))
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(title_label)
        
        card.setLayout(layout)
        return card