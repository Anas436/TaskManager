# 🚀 Task Manager

A sophisticated desktop task management application built with PyQt6 and SQLite, designed to help millions of users worldwide organize their tasks efficiently and boost productivity.

## 🚀 Demo

![](https://github.com/Anas436/TaskManager/blob/main/image/Pending_Tasks.png)

<hr>

![](https://github.com/Anas436/TaskManager/blob/main/image/Completed_Tasks.png)

<hr>

![](https://github.com/Anas436/TaskManager/blob/main/image/Search.png)

## 📁 Project Structure

```
task_manager/
├── build/              # Build files of PyInstaller
├── dist/               # Distributions files of PyInstaller
├── assets/             # Necessary icons of the project
├── image/              # Necessary images for demo
├── InnoSetup           # Inno Setup and License files
├── utils.py            # Utiliy functions for the assets folder
├── main.py             # Main application entry point
├── database.py         # Database operations and management
├── models.py           # Data models (Task, Category)
├── widgets.py          # Custom UI widgets (TaskWidget, StatisticsWidget)
├── styles.py           # Application styling and themes
├── TaskManager.spec    # Desktop Application Setup Wizard
├── TaskManagersetup_v1.0.exe # Production ready file for Installing in Windows
├── tasks.db            # Database of the project
├── requirements.text   # Dependencies of the project
└── README.md           # Project documentation
```

## ✨ Features

### 🎯 Core Functionality

- **Task Management**: Create, read, update, and delete tasks with ease
- **Priority Levels**: Categorize tasks as High, Medium, or Low priority
- **Due Dates**: Set deadlines with date and time precision
- **Categories**: Organize tasks into customizable categories
- **Completion Tracking**: Mark tasks as complete with visual feedback

### 🎨 User Experience

- **Modern UI**: Clean, intuitive interface with professional styling
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Real-time Statistics**: Dashboard with comprehensive task analytics
- **Quick Add**: Rapid task entry with keyboard shortcuts
- **Responsive Design**: Adapts to different screen sizes

### 🔧 Advanced Features

- **Auto-save**: Automatic data persistence every 30 seconds
- **Task Filtering**: Filter by category and completion status
- **Overdue Detection**: Visual indicators for overdue tasks
- **Data Export/Import**: Backup and restore functionality
- **Keyboard Navigation**: Full keyboard support for power users

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project

```bash
git clone <repository-url>
cd task_manager
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.text
```

### Step 4: Run the Application

```bash
python main.py
```

## 🎮 Usage Guide

### Adding Tasks

1. Click "New Task" from File menu (Ctrl+N)
2. Enter task details (title, description, priority, due date)
3. Click OK to save

### Quick Add

- Type in the "Quick add task..." field and press Enter

### Managing Tasks

- Click checkbox to mark tasks complete
- Use Delete button to remove tasks
- Tasks automatically move to Completed tab when marked done

### Categories

- Pre-defined categories: Work, Personal, Shopping, Health, Finance
- Add custom categories via Tools → Add Category
- Filter tasks by category using the dropdown

## 📊 Statistics Dashboard

The application provides real-time statistics:

- Total tasks count
- Pending vs completed tasks
- High priority tasks
- Overdue tasks
- Completion percentage

## 🛠️ Building Executable

### Using PyInstaller

#### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

#### Step 2: Create Executable **TaskManager.spec** File

#### Step 3: Make Utitlity Function Fetch Files

Like the **utils.py** file has been done.

```bash
import os
import sys

# Call 'resource_path' function everywhere in the code during use the 'icons' & 'assests' folder.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
```

#### Step 4: Run the **TaskManager.spec** File

```bash
pyinstaller TaskManager.spec
```

#### Step 5: Go to the **dist** Folder and Run **TaskManager.exe** File

#### Step 6: Visit the __Inno Setup__ to [Downloads](https://jrsoftware.org/isdl.php) the Installer and perform necessary customization

#### Step 7: Visit the [MIT License](https://opensource.org/license/MIT) to use it for production

#### Step 8: Navigate the root directory and run the .exe  setup file to install in Windows

## 🏗️ Architecture

### Data Layer

- **SQLite Database**: Lightweight, file-based storage
- **DatabaseManager Class**: Handles all CRUD operations
- **Data Models**: Task and Category classes with business logic

### Presentation Layer

- **PyQt6 Framework**: Modern, native desktop UI
- **Custom Widgets**: Reusable UI components
- **MVVM Pattern**: Clean separation of concerns

### Business Logic

- **Task Validation**: Ensures data integrity
- **Statistics Engine**: Real-time analytics
- **Theme Management**: Dynamic styling system

## 🔧 Technical Highlights

### Performance Optimizations

- Lazy loading of task lists
- Efficient database queries with indexing
- Memory management with proper widget cleanup
- Background auto-save without UI blocking

### Reliability Features

- Transaction-based database operations
- Error handling with user-friendly messages
- Data validation before persistence
- Regular auto-save to prevent data loss

### Scalability Considerations

- Modular architecture for easy feature addition
- Database schema designed for future enhancements
- Configurable through code constants
- Easy theming system

## 📈 Business Impact

This application solves real-world problems:

### For Individuals

- **Time Management**: Prioritize tasks effectively
- **Stress Reduction**: Never miss deadlines
- **Productivity Boost**: Visual progress tracking
- **Organization**: Centralized task repository

### For Teams (Potential Extension)

- **Collaboration**: Shared task boards
- **Accountability**: Task assignment and tracking
- **Reporting**: Team productivity analytics
- **Integration**: Calendar and email sync

## 🚀 Future Roadmap

### Version 2.0 Planned Features

- [ ] Cloud synchronization
- [ ] Mobile companion app
- [ ] Team collaboration features
- [ ] Calendar integration
- [ ] Email notifications
- [ ] Advanced reporting
- [ ] API for third-party integration

### Version 1.1 Enhancements

- [ ] Task templates
- [ ] Recurring tasks
- [ ] Search functionality
- [ ] Data backup to cloud
- [ ] Additional export formats (CSV, JSON)

## 🐛 Troubleshooting

### Common Issues & Solutions

1. **Application won't start**

   - Ensure PyQt6 is installed: `pip install PyQt6`
   - Check Python version: Requires 3.8+

2. **Database errors**

   - Delete `tasks.db` file to reset
   - Check file permissions in application directory

3. **UI rendering issues**

   - Update graphics drivers
   - Try different Qt styles: `app.setStyle("Fusion")`

4. **Executable too large**
   - Use UPX compression
   - Exclude unnecessary packages

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏆 Recognition

This application demonstrates:

- **Professional-grade desktop development**
- **Database design and management**
- **Modern UI/UX principles**
- **Software architecture patterns**
- **Cross-platform deployment**

## 📞 Support

For issues, questions, or suggestions:

1. Check the documentation
2. Look at existing issues
3. Create a new issue with detailed description
4. Email: support@taskmanager.com

## 🚀 Reference
- Python to exe to setup wizard [Link](https://www.youtube.com/watch?v=p3tSLatmGvU&t=809s)
- How to include an image in the exe file [Link](https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file)

---
