"""
Database module for Task Manager application.
Handles all SQLite database operations.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_name: str = "tasks.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        """Create necessary tables for the application."""
        cursor = self.conn.cursor()
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER DEFAULT 2,  -- 1: High, 2: Medium, 3: Low
                due_date TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                category TEXT DEFAULT 'General'
            )
        ''')
        
        # Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#3498db'
            )
        ''')
        
        # Insert default categories if they don't exist
        default_categories = [
            ('General', '#3498db'),
            ('Work', '#e74c3c'),
            ('Personal', '#2ecc71'),
            ('Shopping', '#f39c12'),
            ('Health', '#9b59b6'),
            ('Finance', '#1abc9c')
        ]
        
        for category, color in default_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, color) VALUES (?, ?)
            ''', (category, color))
        
        self.conn.commit()
    
    def add_task(self, title: str, description: str = "", priority: int = 2,
                 due_date: str = None, category: str = "General") -> int:
        """Add a new task to the database."""
        cursor = self.conn.cursor()
        current_time = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO tasks (title, description, priority, due_date, 
                              created_at, updated_at, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, priority, due_date, 
              current_time, current_time, category))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_tasks(self, completed: bool = False, category: str = None) -> List[Dict]:
        """Retrieve tasks from database with optional filters."""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM tasks WHERE completed = ?"
        params = [1 if completed else 0]
        
        if category and category != "All":
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY priority ASC, due_date ASC"
        
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        tasks = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return tasks
    
    def update_task(self, task_id: int, **kwargs):
        """Update task attributes."""
        if not kwargs:
            return
        
        cursor = self.conn.cursor()
        current_time = datetime.now().isoformat()
        kwargs['updated_at'] = current_time
        
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(task_id)
        
        cursor.execute(f'''
            UPDATE tasks SET {set_clause} WHERE id = ?
        ''', values)
        
        self.conn.commit()
    
    def delete_task(self, task_id: int):
        """Delete a task from database."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
    
    def get_categories(self) -> List[Dict]:
        """Get all categories."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def add_category(self, name: str, color: str = "#3498db"):
        """Add a new category."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name, color) VALUES (?, ?)
        ''', (name, color))
        self.conn.commit()
    
    def get_task_statistics(self) -> Dict:
        """Get task statistics for dashboard."""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN priority = 1 AND completed = 0 THEN 1 ELSE 0 END) as high_priority,
                SUM(CASE WHEN due_date IS NOT NULL AND due_date < date('now') AND completed = 0 THEN 1 ELSE 0 END) as overdue
            FROM tasks
        ''')
        
        stats = cursor.fetchone()
        return {
            'total': stats[0] or 0,
            'completed': stats[1] or 0,
            'high_priority': stats[2] or 0,
            'overdue': stats[3] or 0,
            'pending': (stats[0] or 0) - (stats[1] or 0)
        }
    
    def close(self):
        """Close database connection."""
        self.conn.close()