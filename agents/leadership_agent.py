# agents/leadership_agent.py

from typing import Dict, Any

class LeadershipAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate leadership capacity indicators.
        """
        dna = candidate.get("candidate_dna", {})
        leadership = float(dna.get("leadership", 0.65) or 0.65)
        
        return {
            "leadership": round(leadership, 2)
        }
