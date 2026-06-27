# intelligence/skill_evolution/leadership_growth.py

from typing import Dict, Any

class LeadershipGrowthEngine:
    def predict_growth(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate leadership capacity progression over a 24-month horizon.
        """
        score = candidate.get("score", 85)
        
        lead_now = int(score * 0.38)
        lead_24m = int(min(99, lead_now + (score * 0.50)))
        
        return {
            "leadership_now": lead_now,
            "leadership_24m": lead_24m
        }
