# agents/future_agent.py

from typing import Dict, Any

class FutureAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate future progression, roles, and promotion rates.
        """
        dna = candidate.get("candidate_dna", {})
        learning = float(dna.get("learning", 0.75) or 0.75)
        leadership = float(dna.get("leadership", 0.60) or 0.60)
        
        promotion_prob = max(0.10, min(0.99, (learning * 0.5 + leadership * 0.5)))
        
        future_role = "Senior Engineer"
        if leadership > 0.80:
            future_role = "Engineering Manager"
        elif leadership > 0.68:
            future_role = "Technical Lead"
            
        return {
            "future_role": future_role,
            "promotion_probability": round(promotion_prob, 2),
            "leadership": round(leadership, 2)
        }
