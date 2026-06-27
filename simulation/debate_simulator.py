# simulation/debate_simulator.py

import random
from typing import Dict, Any

class DebateSimulator:
    def simulate(self, candidate: Dict[str, Any], committees: int = 1000) -> Dict[str, Any]:
        """
        Simulate 1000 hiring committees to deduce likelihood of approval.
        """
        score = float(candidate.get("score") or 85.0)
        base_hire_rate = score / 100.0
        
        hire_count = 0
        reject_count = 0
        
        for _ in range(committees):
            vote_threshold = random.uniform(0.15, 0.95)
            if vote_threshold < base_hire_rate:
                hire_count += 1
            else:
                reject_count += 1
                
        return {
            "hire": int(round((hire_count / committees) * 100)),
            "reject": int(round((reject_count / committees) * 100))
        }
