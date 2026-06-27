# intelligence/team_compatibility/collaboration_engine.py

from typing import Dict, Any

class CollaborationEngine:
    def evaluate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate candidate collaboration indices.
        """
        cand_collab = candidate_dna["collaboration"]
        team_collab = team_dna["collaboration"]
        
        fit = (cand_collab * 0.6 + team_collab * 0.4)
        
        return {
            "collaboration": round(min(0.99, fit), 2)
        }
