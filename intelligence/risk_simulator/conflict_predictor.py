# intelligence/risk_simulator/conflict_predictor.py

from typing import Dict, Any

class ConflictPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability of friction/conflict developing with teammates.
        """
        collaboration = float(candidate.get("candidate_dna", {}).get("collaboration", 0.70) or 0.70)
        communication = float(candidate.get("candidate_dna", {}).get("communication", 0.65) or 0.65)
        
        # Base conflict is inverse of collaboration & communication
        friction = 1.0 - ((collaboration + communication) / 2.0)
        
        prob = max(0.01, min(0.95, friction * 0.4))
        
        return {
            "conflict_probability": round(prob, 2)
        }
