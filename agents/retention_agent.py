# agents/retention_agent.py

from typing import Dict, Any

class RetentionAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate and forecast candidate tenure stability.
        """
        dna = candidate.get("candidate_dna", {})
        stability = float(dna.get("stability", 0.80) or 0.80)
        
        return {
            "retention": round(stability, 2)
        }
