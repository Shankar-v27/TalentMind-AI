# intelligence/digital_twin/monte_carlo.py

import random
from typing import Dict, Any

class MonteCarloSimulator:
    def simulate(self, score: float) -> Dict[str, Any]:
        """
        Run 10,000 simulations of future trajectories.
        """
        cto = 0
        architect = 0
        manager = 0
        founder = 0
        
        for _ in range(10000):
            val = random.random() * (score / 100.0)
            if val > 0.77:
                cto += 1
            elif val > 0.52:
                architect += 1
            elif val > 0.27:
                manager += 1
            else:
                founder += 1
                
        return {
            "cto": int(round((cto / 10000) * 100)),
            "architect": int(round((architect / 10000) * 100)),
            "manager": int(round((manager / 10000) * 100)),
            "founder": int(round((founder / 10000) * 100))
        }
