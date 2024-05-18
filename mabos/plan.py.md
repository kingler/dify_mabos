

```python
from typing import List
from .action import Action

class Plan:
    def __init__(self, plan_id: str, goal_id: str, actions: List[Action]):
        self.plan_id = plan_id
        self.goal_id = goal_id
        self.actions = actions

    def execute(self, agent: 'Agent'):
        for action in self.actions:
            action.execute(agent)
```