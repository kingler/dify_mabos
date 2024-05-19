from typing import List
from ..task_management.action import Action
from ..knowledge_management.reasoning_engine import Reasoning
from ..knowledge_management.core.knowledge_base import KnowledgeBase
from ..knowledge_management.core.knowledge_graph import KnowledgeGraph

class Intention:
    def __init__(self, intention_id: str, description: str, actions: List[Action], goal, preconditions, postconditions, status: str, knowledge_base: KnowledgeBase, knowledge_graph: KnowledgeGraph):
        self.intention_id = intention_id
        self.description = description
        self.actions = actions
        self.goal = goal
        self.preconditions = preconditions
        self.postconditions = postconditions
        self.status = status
        self.reasoning = Reasoning(knowledge_base, knowledge_graph)

    def activate_intention(self):
        self.status = "active"

    def suspend_intention(self):
        self.status = "suspended"

    def complete_intention(self):
        self.status = "completed"

    def revise_beliefs(self, new_beliefs):
        self.reasoning.belief_revision(new_beliefs)

    def generate_desires(self):
        desires = self.reasoning.desire_generation(self.goal, self.reasoning.knowledge_base.beliefs)
        prioritized_desires = self.reasoning.desire_prioritization(desires)
        return prioritized_desires

    def select_intention(self, desires, plans):
        selected_intention = self.reasoning.intention_selection(desires, plans)
        return selected_intention

    def execute_intention(self):
        self.reasoning.intention_execution(self)

    def learn(self, feedback):
        self.reasoning.belief_accuracy_learning(feedback)
        self.reasoning.desire_relevance_learning(feedback)
        self.reasoning.intention_effectiveness_learning(feedback)