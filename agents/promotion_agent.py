# agents/promotion_agent.py

from typing import Dict, Any

class PromotionAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate horizontal/vertical career progression probabilities.
        """
        risk_profile = candidate.get("risk_profile", {})
        prom_prob = float(risk_profile.get("promotion", {}).get("promotion_probability", 0.81) or 0.81)
        mgr_prob = float(risk_profile.get("manager", {}).get("manager_probability", 0.71) or 0.71)
        
        return {
            "promotion": prom_prob,
            "manager": mgr_prob
        }
