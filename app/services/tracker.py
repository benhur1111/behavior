from typing import List
from app.models.behavior import Behavior

# In-memory store (for now)
BEHAVIORS: List[Behavior] = []

def add_behavior(behavior: Behavior):
    BEHAVIORS.append(behavior)
    return behavior

def list_behaviors():
    return BEHAVIORS
