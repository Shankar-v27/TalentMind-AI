# intelligence/optimizer/team_optimizer.py

from typing import Dict, List, Any

class TeamOptimizer:
    def optimize_team(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates team fit metrics: happiness index, productivity, knowledge sharing, conflict reduction.
        """
        objs = candidate.get("objectives", {})
        team_comp = objs.get("team", 78.0) / 100.0
        culture_fit = objs.get("culture", 80.0) / 100.0
        
        happiness = round((team_comp * 0.6 + culture_fit * 0.4), 2)
        productivity = round((team_comp * 0.7 + culture_fit * 0.3), 2)
        sharing = round((team_comp * 0.5 + culture_fit * 0.5), 2)
        conflict_reduction = round((team_comp * 0.8), 2)
        
        team_score = round((happiness + productivity + sharing + conflict_reduction) / 4.0, 2)
        
        return {
            "candidate_id": candidate.get("candidate_id"),
            "name": candidate.get("name"),
            "team_score": team_score,
            "metrics": {
                "team_happiness": happiness,
                "team_productivity": productivity,
                "knowledge_sharing": sharing,
                "conflict_reduction": conflict_reduction
            }
        }
