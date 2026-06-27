# intelligence/team_compatibility/burnout_engine.py

from typing import Dict, Any

class BurnoutEngine:
    def evaluate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate work pressure balance.
        """
        cand_stress = candidate_dna["stress_handling"]
        
        # Risk is lower if candidate handles stress exceptionally well
        risk = (1.0 - cand_stress) * 0.4
        
        return {
            "burnout_risk": round(min(0.99, max(0.01, risk)), 2)
        }
