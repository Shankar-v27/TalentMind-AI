# intelligence/team_compatibility/role_predictor.py

from typing import Dict, Any

class TeamRolePredictor:
    def predict(self, candidate_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify candidate's primary behavioral archetype role.
        """
        leadership = candidate_dna["leadership"]
        mentoring = candidate_dna["mentoring"]
        innovation = candidate_dna["innovation"]
        
        future_role = "COLLABORATOR"
        
        if mentoring > 0.80:
            future_role = "MENTOR"
        elif leadership > 0.82:
            future_role = "LEADER"
        elif innovation > 0.80:
            future_role = "INNOVATOR"
            
        return {
            "future_team_role": future_role
        }
