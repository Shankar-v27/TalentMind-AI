# intelligence/time_machine/state_manager.py

from typing import Dict, List, Any
import datetime

class StateManager:
    def __init__(self):
        self.current_state = {
            "experience": 5,
            "skills": ["python", "aws", "docker"],
            "salary": 20, # In LPA or thousands
            "joining": 60, # Notice period max in days
            "leadership": 0.3,
            "future_potential": 0.5,
            "retention": 0.5,
            "risk": 0.5
        }
        self.history: List[Dict[str, Any]] = []

    def get_state(self) -> Dict[str, Any]:
        return self.current_state

    def update_state(self, new_params: Dict[str, Any]) -> Dict[str, Any]:
        # Save snapshot to history before updating
        snapshot = {
            "timestamp": datetime.datetime.now().isoformat(),
            "state": self.current_state.copy()
        }
        self.history.append(snapshot)
        
        # Merge new parameters
        for k, v in new_params.items():
            if k in self.current_state:
                # Ensure correct type
                if isinstance(self.current_state[k], list) and isinstance(v, list):
                    self.current_state[k] = [str(item).lower() for item in v]
                elif isinstance(self.current_state[k], float):
                    self.current_state[k] = float(v)
                elif isinstance(self.current_state[k], int):
                    self.current_state[k] = int(v)
                else:
                    self.current_state[k] = v
            else:
                self.current_state[k] = v
                
        return self.current_state

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history
