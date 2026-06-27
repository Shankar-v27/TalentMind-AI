# agents/negotiation_engine.py

from typing import Dict, Any

class NegotiationEngine:
    def negotiate(self, initial_hire: float, initial_reject: float) -> Dict[str, Any]:
        """
        Negotiate scores to find a settled equilibrium point.
        """
        # Simulated negotiation settlement
        hire_settlement = initial_hire * 1.05 if initial_hire > initial_reject else initial_hire * 0.95
        reject_settlement = initial_reject * 0.90 if initial_hire > initial_reject else initial_reject * 1.05
        
        return {
            "hire_score": int(round(max(10, min(99, hire_settlement * 100)))),
            "reject_score": int(round(max(10, min(99, reject_settlement * 100))))
        }
