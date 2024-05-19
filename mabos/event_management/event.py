from pydantic import BaseModel
from typing import List
from ..bdi.belief import Belief

class Event(BaseModel):
    event_type: str
    belief_updates: List[Belief] = []
    
    def __init__(self, event_type: str, belief_updates: List[Belief] = []):
        self.event_type = event_type
        self.belief_updates = belief_updates
        
    def add_belief_update(self, belief: Belief):
        self.belief_updates.append(belief)
        
    def get_belief_updates(self) -> List[Belief]:
        return self.belief_updates