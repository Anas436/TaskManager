"""
Data models for Task Manager application.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Task data model."""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    priority: int = 2  # 1: High, 2: Medium, 3: Low
    due_date: Optional[str] = None
    completed: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    category: str = "General"
    
    @property
    def priority_text(self) -> str:
        """Get priority as text."""
        priorities = {1: "High", 2: "Medium", 3: "Low"}
        return priorities.get(self.priority, "Medium")
    
    @property
    def priority_color(self) -> str:
        """Get priority color."""
        colors = {1: "#e74c3c", 2: "#f39c12", 3: "#2ecc71"}
        return colors.get(self.priority, "#f39c12")
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date or self.completed:
            return False
        
        try:
            due = datetime.fromisoformat(self.due_date)
            return due < datetime.now()
        except:
            return False
    
    @property
    def due_date_formatted(self) -> str:
        """Get formatted due date."""
        if not self.due_date:
            return "No due date"
        
        try:
            due = datetime.fromisoformat(self.due_date)
            return due.strftime("%b %d, %Y %H:%M")
        except:
            return self.due_date

@dataclass
class Category:
    """Category data model."""
    id: Optional[int] = None
    name: str = ""
    color: str = "#3498db"