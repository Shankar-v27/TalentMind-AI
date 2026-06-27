# agents/innovation_agent.py

from typing import Dict, Any

class InnovationAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate creativity and experimentation index.
        """
        dna = candidate.get("candidate_dna", {})
        innovation = float(dna.get("innovation", 0.70) or 0.70)
        
        return {
            "innovation_score": round(innovation, 2)
        }
