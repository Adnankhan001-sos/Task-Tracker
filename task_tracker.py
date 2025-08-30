import streamlit as st
import pandas as pd
import json
from datetime import datetime, date, timedelta
from pathlib import Path
import uuid

# Configuration
TASKS_FILE = "tasks.json"
PRIORITY_LEVELS = ["High", "Medium", "Low"]
PRIORITY_COLORS = {
    "High": "🔴",
    "Medium": "🟡", 
    "Low": "🟢"
}

class TaskManager:
    """Handles task operations and persistence"""
    
    def __init__(self, file_path=TASKS_FILE):
        self.file_path = file_path
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if Path(self.file_path).exists():
                with open(self.file_path, 'r') as f:
                    tasks_data = json.load(f)
                    # Convert date strings back to date objects
                    for task in tasks_data:
                        task['due_date'] = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                    return tasks_data
            return []
        except Exception as e:
            st.error(f"Error loading tasks: {e}")
            return []
    
    def save_tasks(self, tasks):
        """Save tasks to JSON file"""
        try:
            # Convert date objects to strings for JSON serialization
            tasks_to_save = []
            for task in tasks:
                task_copy = task.copy()
                task_copy['due_date'] = task['due_date'].strftime('%Y-%m-%d')
                tasks_to_save.append(task_copy)
            
            with open(self.file_path, 'w') as f:
                json.dump(tasks_to_save, f, indent=2)
        except Exception as e:
            st.error(f"Error saving tasks: {e}")
    
    def add_task(self, name, due_date, priority):
        """Add a new task"""
        task = {
            'id': str(uuid.uuid4()),
            'name': name,
            'due_date': due_date,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return task
    
    def mark_completed(self, task_id, tasks):
        """Mark a task as completed"""
        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = True
                break
        return tasks
    
    def delete_task(self, task_id, tasks):
        """Delete a task"""
        return [task for task in tasks if task['id'] != task_id]

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'tasks' not in st.session_state:
        task_manager = TaskManager()
        st.session_state.tasks = task_manager.load_tasks()
    
    if 'task_manager' not in st.session_state:
        st.session_state.task_manager = TaskManager()

def filter_tasks(tasks, priority_filter=None, date_filter=None):
    """Filter tasks based on priority and date"""
    filtered_tasks = tasks.copy()
    
    # Filter by priority
    if priority_filter and priority_filter != "All":
        filtered_tasks = [task for task in filtered_tasks if task['priority'] == priority_filter]
    
    # Filter by date
    if date_filter:
        today = date.today()
        if date_filter == "Today":
            filtered_tasks = [task for task in filtered_tasks if task['due_date'] == today]
        elif date_filter == "This Week":
            week_end = today + timedelta(days=7)
            filtered_tasks = [task for task in filtered_tasks if today <= task['due_date'] <= week_end]
        elif date_filter == "Overdue":
            filtered_tasks = [task for task in filtered_tasks if task['due_date'] < today]
    
    return filtered_tasks

def display_tasks_table(tasks, show_actions=True):
    """Display tasks in a table format"""
    if not tasks:
        st.info("No tasks to display")
        return
    
    # Prepare data for display
    display_data = []
    for task in tasks:
        priority_icon = PRIORITY_COLORS.get(task['priority'], "")
        due_date_str = task['due_date'].strftime('%Y-%m-%d')
        
        # Check if task is overdue
        is_overdue = task['due_date'] < date.today() and not task['completed']
        overdue_indicator = "⚠️" if is_overdue else ""
        
        display_data.append({
            'Task': task['name'] if not task['completed'] else f"~~{task['name']}~~",
            'Due Date': f"{overdue_indicator} {due_date_str}",
            'Priority': f"{priority_icon} {task['priority']}",
            'Status': "✅ Completed" if task['completed'] else "⏳ Pending",
            'ID': task['id']
        })
    
    df = pd.DataFrame(display_data)
    
    if show_actions:
        # Display with action buttons
        for i, task in enumerate(tasks):
            cols = st.columns([4, 1, 1])
            
            with cols[0]:
                task_style = "text-decoration: line-through; opacity: 0.6;" if task['completed'] else ""
                priority_icon = PRIORITY_COLORS.get(task['priority'], "")
                is_overdue = task['due_date'] < date.today() and not task['completed']
                overdue_text = " (OVERDUE)" if is_overdue else ""
                
                st.markdown(f"""
                <div style="{task_style}">
                    <strong>{task['name']}</strong><br>
                    📅 {task['due_date']} {overdue_text}<br>
                    {priority_icon} {task['priority']} Priority
                </div>
                """, unsafe_allow_html=True)
            
            with cols[1]:
                if not task['completed']:
                    if st.button(f"✅", key=f"complete_{task['id']}", help="Mark as completed"):
                        st.session_state.tasks = st.session_state.task_manager.mark_completed(
                            task['id'], st.session_state.tasks
                        )
                        st.session_state.task_manager.save_tasks(st.session_state.tasks)
                        st.rerun()
            
            with cols[2]:
                if st.button(f"🗑️", key=f"delete_{task['id']}", help="Delete task"):
                    st.session_state.tasks = st.session_state.task_manager.delete_task(
                        task['id'], st.session_state.tasks
                    )
                    st.session_state.task_manager.save_tasks(st.session_state.tasks)
                    st.rerun()
            
            st.divider()
    else:
        # Simple table display
        st.dataframe(df.drop('ID', axis=1), use_container_width=True)

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Task Tracker",
        page_icon="📋",
        layout="wide"
    )
    
    initialize_session_state()
    
    st.title("📋 Task Tracker")
    st.markdown("Manage your tasks efficiently with priorities and due dates!")
    
    # Sidebar for adding new tasks
    with st.sidebar:
        st.header("➕ Add New Task")
        
        with st.form("add_task_form"):
            task_name = st.text_input("Task Name", placeholder="Enter task description...")
            due_date = st.date_input("Due Date", min_value=date.today())
            priority = st.selectbox("Priority Level", PRIORITY_LEVELS)
            
            submitted = st.form_submit_button("Add Task", use_container_width=True)
            
            if submitted and task_name:
                new_task = st.session_state.task_manager.add_task(task_name, due_date, priority)
                st.session_state.tasks.append(new_task)
                st.session_state.task_manager.save_tasks(st.session_state.tasks)
                st.success(f"Task '{task_name}' added successfully!")
                st.rerun()
            elif submitted and not task_name:
                st.error("Please enter a task name!")
        
        st.divider()
        
        # Task statistics
        st.header("📊 Task Statistics")
        total_tasks = len(st.session_state.tasks)
        completed_tasks = len([t for t in st.session_state.tasks if t['completed']])
        pending_tasks = total_tasks - completed_tasks
        overdue_tasks = len([t for t in st.session_state.tasks 
                           if t['due_date'] < date.today() and not t['completed']])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Tasks", total_tasks)
            st.metric("Completed", completed_tasks)
        with col2:
            st.metric("Pending", pending_tasks)
            st.metric("Overdue", overdue_tasks, delta=f"-{overdue_tasks}" if overdue_tasks > 0 else "0")
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.header("🔍 Filters")
        
        priority_filter = st.selectbox("Filter by Priority", 
                                     ["All"] + PRIORITY_LEVELS, 
                                     key="priority_filter")
        
        date_filter = st.selectbox("Filter by Date", 
                                 ["All", "Today", "This Week", "Overdue"], 
                                 key="date_filter")
        
        if st.button("Clear Filters", use_container_width=True):
            st.session_state.priority_filter = "All"
            st.session_state.date_filter = "All"
            st.rerun()
    
    with col1:
        # Filter tasks
        pending_tasks = [task for task in st.session_state.tasks if not task['completed']]
        completed_tasks = [task for task in st.session_state.tasks if task['completed']]
        
        # Apply filters to pending tasks
        if priority_filter != "All" or date_filter != "All":
            pending_tasks = filter_tasks(pending_tasks, 
                                       priority_filter if priority_filter != "All" else None,
                                       date_filter if date_filter != "All" else None)
        
        # Display pending tasks
        st.header(f"⏳ Pending Tasks ({len(pending_tasks)})")
        if pending_tasks:
            display_tasks_table(pending_tasks, show_actions=True)
        else:
            st.info("No pending tasks match the current filters.")
        
        st.divider()
        
        # Display completed tasks
        st.header(f"✅ Completed Tasks ({len(completed_tasks)})")
        if completed_tasks:
            with st.expander("Show Completed Tasks", expanded=False):
                display_tasks_table(completed_tasks, show_actions=True)
        else:
            st.info("No completed tasks yet.")
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tip**: Tasks are automatically saved to `tasks.json` and will persist between app runs!")

if __name__ == "__main__":
    main()