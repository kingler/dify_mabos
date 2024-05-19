from ..agents.agent import Agent
from ..task_management.task import Task
from typing import List

class Goal:
    def __init__(self, goal_id: str, description: str, priority: int, parent_goal: 'Goal' = None, goal_type: str = None, preconditions: List[str] = None, postconditions: List[str] = None, effects: List[str] = None, metrics: List[str] = None):
        self.goal_id = goal_id
        self.description = description
        self.goal_type = goal_type
        self.priority = priority
        self.preconditions = preconditions
        self.postconditions = postconditions
        self.effects = effects
        self.metrics = metrics
        self.parent_goal = parent_goal
        self.sub_goals: List['Goal'] = []
        self.parent_goal = None  # Add this line to define the parent_goal attribute
        
    def add_sub_goal(self, sub_goal: 'Goal'):
        self.sub_goals.append(sub_goal)
        sub_goal.parent_goal = self    

    def is_achieved(self) -> bool:
        for task in self.tasks:
            if not task.is_completed:
                return False
        return True
    
    def add_task(self, task: Task):
        self.tasks.append(task)
        
    def is_achieved(self, agent: Agent) -> bool:
        for task in self.tasks:
            if not task.is_completed:
                return False
        return True
    
    def set_and_decomposition(self, sub_goals: List['Goal']):
        self.sub_goals = sub_goals
        for sub_goal in sub_goals:
            sub_goal.parent_goal = self

    def set_or_decomposition(self, sub_goals: List['Goal']):
        self.sub_goals = sub_goals
        for sub_goal in sub_goals:
            sub_goal.parent_goal = self

    def add_dependency(self, dependent_goal: 'Goal'):
        self.dependencies.append(dependent_goal)
        
    def update_status(self):
        if all(sub_goal.is_achieved() for sub_goal in self.sub_goals):
            self.status = "achieved"
        elif any(sub_goal.status == "in_progress" for sub_goal in self.sub_goals):
            self.status = "in_progress"
        else:
            self.status = "pending"    
            
    def update_priority(self, new_priority: int):
        self.priority = new_priority
        # Propagate priority changes to sub-goals if necessary
    def update_priority(self, new_priority: int):
        self.priority = new_priority
        
        # Propagate priority changes to sub-goals
        for sub_goal in self.sub_goals:
            sub_goal.update_priority(new_priority)
        
    def detect_conflicts(self, other_goal: 'Goal') -> bool:
        # Check for conflicts based on goal descriptions, preconditions, or effects
        # Check for conflicts based on goal descriptions
        if self.description == other_goal.description:
            return True
        
        # Check for conflicts based on preconditions
        for precondition in self.preconditions:
            if precondition in other_goal.preconditions:
                return True
        
        # Check for conflicts based on effects
        for effect in self.effects:
            if effect in other_goal.effects:
                return True
        
        return False

    def resolve_conflict(self, other_goal: 'Goal'):
        # Implement conflict resolution strategies, such as goal negotiation or replanning
        pass            