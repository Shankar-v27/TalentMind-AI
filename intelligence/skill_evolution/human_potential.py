# intelligence/skill_evolution/human_potential.py

from typing import Dict, Any

class HumanPotentialEngine:
    def calculate(self, candidate: Dict[str, Any], velocity: float) -> Dict[str, Any]:
        """
        Evaluate final overall human potential score.
        """
        score = float(candidate.get("score", 85))
        
        # Incorporate learning velocity into overall potential value
        potential = (score / 100.0) * 0.8 + (velocity / 5.0) * 0.2
        potential = min(0.99, max(0.10, potential))
        
        return {
            "human_potential": round(potential, 2)
        }
