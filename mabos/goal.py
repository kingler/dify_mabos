class Goal:
    def __init__(self, goal_id: str, description: str, priority: int):
        self.goal_id = goal_id
        self.description = description
        self.priority = priority

    def is_achieved(self) -> bool:
        # Implement logic to check if the goal is achieved
        pass