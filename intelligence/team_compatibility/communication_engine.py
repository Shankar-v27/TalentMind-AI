# intelligence/team_compatibility/communication_engine.py

from typing import Dict, Any

class CommunicationEngine:
    def evaluate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate candidate integration into team communication channels.
        """
        cand_comm = candidate_dna["communication"]
        team_comm = team_dna["communication"]
        
        fit = 1.0 - abs(cand_comm - team_comm) * 0.4
        
        return {
            "communication_fit": round(min(0.99, fit), 2)
        }
