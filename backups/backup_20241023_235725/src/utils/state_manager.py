
from copy import deepcopy
from typing import Optional, Any, List
from datetime import datetime

class StateManager:
    def __init__(self, max_states: int = 10):
        self.states: List[dict] = []
        self.max_states = max_states
        
    def push_state(self, state: dict):
        """Save a new state"""
        if len(self.states) >= self.max_states:
            self.states.pop(0)
        self.states.append({
            'data': deepcopy(state),
            'timestamp': datetime.now()
        })
    
    def get_previous_state(self) -> Optional[dict]:
        """Get the previous state without removing it"""
        return self.states[-2]['data'] if len(self.states) > 1 else None
    
    def rollback(self) -> Optional[dict]:
        """Rollback to previous state and return it"""
        if self.states:
            return self.states.pop()['data']
        return None
    
    def clear_history(self):
        """Clear state history"""
        self.states = []
