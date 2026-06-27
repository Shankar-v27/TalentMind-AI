# intelligence/recruiter_memory/reinforcement_engine.py

from typing import Dict, Any

class RecruiterReinforcementEngine:
    def __init__(self):
        # Q-table: State (recruiter_id) -> Action -> value
        self.q_table: Dict[str, Dict[str, float]] = {}

    def get_q_values(self, recruiter_id: str) -> Dict[str, float]:
        if recruiter_id not in self.q_table:
            self.q_table[recruiter_id] = {
                "boost_github": 0.0,
                "boost_leadership": 0.0,
                "boost_stability": 0.0,
                "boost_learning": 0.0
            }
        return self.q_table[recruiter_id]

    def learn_from_hiring_outcome(
        self,
        recruiter_id: str,
        action: str, # 'boost_github', etc.
        outcome: str, # 'success_hire', 'retained_24m', 'early_resignation'
        alpha: float = 0.1,
        gamma: float = 0.9
    ) -> float:
        """
        Updates Q-value for actions according to rewards.
        Rewards: success_hire = +100, retained = +80, early_resignation = -100
        """
        rewards = {
            "success_hire": 100.0,
            "retained_24m": 80.0,
            "promotion": 50.0,
            "early_resignation": -100.0
        }
        
        reward = rewards.get(outcome, 0.0)
        q_vals = self.get_q_values(recruiter_id)
        
        # Simple Q update (bellman projection)
        old_val = q_vals.get(action, 0.0)
        max_future_q = max(q_vals.values())
        
        new_val = old_val + alpha * (reward + gamma * max_future_q - old_val)
        q_vals[action] = round(new_val, 2)
        
        return new_val
