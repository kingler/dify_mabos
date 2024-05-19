# mabos/process_management/task_manager.py
import threading
from datetime import datetime

class TaskManager:
    def __init__(self, process_instance_repository):
        self.process_instance_repository = process_instance_repository
        # Initialize other attributes and components
    def __init__(self, process_instance_repository):
        self.process_instance_repository = process_instance_repository
        self.tasks = {}  # Dictionary to store tasks
        self.task_lock = threading.Lock()  # Lock for synchronizing access to tasks
        self.task_dependencies = {}  # Dictionary to store task dependencies
        self.task_deadlines = {}  # Dictionary to store task deadlines
        self.task_assignees = {}  # Dictionary to store task assignees
        

    def assign_task(self, task, assignee):
        # Assign a task to an assignee
        with self.task_lock:
            if task not in self.tasks:
                self.tasks[task] = assignee
                self.task_assignees[task] = assignee
                # Notify the assignee (MABOS agent) about the assigned task
                assignee.assign_task(task)
            else:
                raise ValueError(f"Task {task} is already assigned.")

    def complete_task(self, task):
        # Mark a task as completed
        with self.task_lock:
            if task in self.tasks:
                del self.tasks[task]
                del self.task_assignees[task]
                if task in self.task_dependencies:
                    del self.task_dependencies[task]
                if task in self.task_deadlines:
                    del self.task_deadlines[task]
                # Notify the assignee (MABOS agent) about the completed task
                assignee = self.task_assignees[task]
                assignee.complete_task(task)
            else:
                raise ValueError(f"Task {task} is not assigned.")

    def get_task_dependencies(self, task):
        # Retrieve the dependencies of a task
        with self.task_lock:
            if task in self.task_dependencies:
                return self.task_dependencies[task]
            else:
                return []

    def check_task_deadline(self, task):
        # Check if a task has reached its deadline
        with self.task_lock:
            if task in self.task_deadlines:
                deadline = self.task_deadlines[task]
                current_time = datetime.now()
                if current_time > deadline:
                    return True
            return False
