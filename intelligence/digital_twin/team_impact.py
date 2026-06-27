# intelligence/digital_twin/team_impact.py

from typing import Dict, Any

class TeamImpactEngine:
    def predict_impact(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate productivity and innovation value gains for the target team.
        """
        score = float(candidate.get("score", 85))
        
        prod_gain = round(1.0 + (score / 100.0) * 0.18, 2)
        innov_gain = round(1.0 + (score / 100.0) * 0.24, 2)
        
        return {
            "team_productivity": prod_gain,
            "team_innovation": innov_gain
        }
