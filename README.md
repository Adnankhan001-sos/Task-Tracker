[README.md](https://github.com/user-attachments/files/22056289/README.md)
# 📋 Task Tracker

A simple and elegant task management application built with Python and Streamlit. This app allows you to create, organize, and track your tasks with a beautiful and intuitive user interface.

## ✨ Features

### Core Functionality
- **Add Tasks**: Create new tasks with name, due date, and priority level
- **Task Management**: Mark tasks as completed and delete tasks
- **Visual Organization**: Color-coded priority levels (High, Medium, Low)
- **Task Filtering**: Filter tasks by priority and due date
- **Statistics Dashboard**: View task completion metrics and progress

### Advanced Features
- **Data Persistence**: Tasks are automatically saved to a local JSON file
- **Responsive Design**: Clean, modern UI with custom styling
- **State Management**: Uses Streamlit's session state for efficient data handling
- **Date Filtering**: Filter by "Today", "This Week", "Overdue", or view all tasks
- **Completed Tasks Section**: Separate view for completed tasks with strikethrough styling

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project files**
   ```bash
   # If you have the files locally, navigate to the project directory
   cd "path/to/your/project"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open in your default browser
   - Usually at: `http://localhost:8501`

## 📖 How to Use

### Adding Tasks
1. Use the sidebar on the left to add new tasks
2. Enter a task name (required)
3. Select a due date using the date picker
4. Choose a priority level (Low, Medium, High)
5. Click "Add Task" to save

### Managing Tasks
- **Complete a task**: Click the ✅ button next to any active task
- **Delete a task**: Click the 🗑️ button to remove a task permanently
- **View completed tasks**: Scroll down to see the "Completed Tasks" section

### Filtering Tasks
- **By Priority**: Use the "Filter by Priority" dropdown to show only specific priority levels
- **By Date**: Use the "Filter by Date" dropdown to show:
  - Today's tasks
  - This week's tasks
  - Overdue tasks
  - All tasks

### Statistics
The right sidebar shows:
- Number of active tasks
- Number of completed tasks
- Number of overdue tasks
- Overall completion rate

## 🎨 UI Features

### Priority Color Coding
- **High Priority**: Red border and light red background
- **Medium Priority**: Orange border and light orange background
- **Low Priority**: Green border and light green background

### Visual Indicators
- Completed tasks appear with strikethrough text
- Overdue tasks are highlighted in the statistics
- Clean, modern interface with proper spacing and typography

## 💾 Data Storage

- Tasks are automatically saved to `tasks.json` in the project directory
- Data persists between app sessions
- No external database required
- JSON format for easy backup and portability

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web framework
- **Backend**: Python with session state management
- **Storage**: Local JSON file
- **Styling**: Custom CSS with responsive design

### Key Components
- `app.py`: Main application file
- `requirements.txt`: Python dependencies
- `tasks.json`: Data storage file (created automatically)

### State Management
- Uses `st.session_state` for efficient data handling
- Automatic data persistence with JSON file storage
- Real-time updates without page refreshes

## 🔧 Customization

### Adding New Features
The modular code structure makes it easy to extend:
- Add new task properties in the `add_task()` function
- Create new filter types in `filter_tasks_by_date()`
- Modify styling by updating the CSS in the `st.markdown()` section

### Styling Changes
- Modify the CSS section in `app.py` to change colors, fonts, or layout
- Add new CSS classes for different task states
- Customize the priority color scheme

## 🐛 Troubleshooting

### Common Issues

1. **App won't start**
   - Ensure Python 3.7+ is installed
   - Check that all dependencies are installed: `pip install -r requirements.txt`

2. **Tasks not saving**
   - Check file permissions in the project directory
   - Ensure the app has write access to create `tasks.json`

3. **UI not loading properly**
   - Clear browser cache
   - Restart the Streamlit server

### Error Messages
- **"Error loading tasks"**: Check if `tasks.json` is corrupted or has invalid JSON
- **"Error saving tasks"**: Check file permissions and disk space

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application!

---

**Happy Task Tracking!** 🎯
