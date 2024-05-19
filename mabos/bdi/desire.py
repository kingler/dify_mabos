class Desire:
    def __init__(self, desire_id: str, description: str, priority: int, activation_condition, completion_condition, deadline: float):
        self.desire_id = desire_id
        self.description = description
        self.priority = priority
        self.activation_condition = activation_condition
        self.completion_condition = completion_condition
        self.deadline = deadline

    def is_active(self, current_beliefs) -> bool:
        return self.activation_condition(current_beliefs)

    def is_completed(self, current_beliefs) -> bool:
        return self.completion_condition(current_beliefs)