from typing import List
from .goal import Goal
from .plan import Plan
from .knowledge_base import KnowledgeBase

class Agent:
    def __init__(self, agent_id: str, beliefs: dict, desires: List[Goal], intentions: List[Plan], knowledge_base: KnowledgeBase):
        self.agent_id = agent_id
        self.beliefs = beliefs
        self.desires = desires
        self.intentions = intentions
        self.knowledge_base = knowledge_base

    def update_beliefs(self, new_beliefs: dict):
        self.beliefs.update(new_beliefs)
        self.knowledge_base.update(new_beliefs)

    def add_desire(self, goal: Goal):
        self.desires.append(goal)

    def add_intention(self, plan: Plan):
        self.intentions.append(plan)

    def remove_intention(self, plan: Plan):
        self.intentions.remove(plan)

    def execute_intentions(self):
        for intention in self.intentions:
            intention.execute(self)

    def communicate(self, message: str, recipient: 'Agent'):
        # Implement agent communication logic
        pass