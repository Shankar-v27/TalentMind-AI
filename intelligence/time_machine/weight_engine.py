# intelligence/time_machine/weight_engine.py

from typing import Dict, Any

class WeightEngine:
    def calculate_weights(self, state: Dict[str, Any]) -> Dict[str, float]:
        """
        Dynamically calculates weights for different dimensions based on state priorities.
        Returns a normalized dict of weights that sum to 1.0.
        """
        # Read raw priorities
        skill_p = float(state.get("skill_weight", 0.3))
        exp_p = float(state.get("experience_weight", 0.2))
        lead_p = float(state.get("leadership", 0.3))
        future_p = float(state.get("future_potential", 0.3))
        retention_p = float(state.get("retention", 0.5))
        risk_p = float(state.get("risk", 0.5))
        
        # Calculate raw sum
        raw_weights = {
            "skill": max(0.05, skill_p),
            "experience": max(0.05, exp_p),
            "leadership": max(0.05, lead_p),
            "future": max(0.05, future_p),
            "retention": max(0.05, retention_p),
            "risk": max(0.05, 1.0 - risk_p) # Lower risk = higher weight/score contribution
        }
        
        total = sum(raw_weights.values())
        if total == 0:
            return {k: 1.0 / len(raw_weights) for k in raw_weights}
            
        # Normalize
        return {k: round(v / total, 3) for k, v in raw_weights.items()}
