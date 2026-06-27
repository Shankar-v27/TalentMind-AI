# intelligence/team_compatibility/monte_carlo.py

import random
from typing import Dict, Any

class TeamMonteCarloSimulator:
    def simulate(self, comp_score: float, conflict_prob: float) -> Dict[str, Any]:
        """
        Run 10,000 team stability simulations.
        """
        success = 0
        conflict = 0
        burnout = 0
        innovation = 0
        
        for _ in range(10000):
            val = random.random()
            if val < comp_score:
                success += 1
            if random.random() < conflict_prob * 3.0: # amplified scale for simulation variance
                conflict += 1
            if random.random() < 0.12:
                burnout += 1
            if random.random() < 0.71:
                innovation += 1
                
        return {
            "success": int(round((success / 10000) * 100)),
            "conflict": int(round((conflict / 10000) * 100)),
            "burnout": int(round((burnout / 10000) * 100)),
            "innovation": int(round((innovation / 10000) * 100))
        }
