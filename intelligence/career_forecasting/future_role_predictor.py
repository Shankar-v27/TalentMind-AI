# intelligence/career_forecasting/future_role_predictor.py

from typing import Dict, Any

class FutureRolePredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Predict the next vertical step in the career graph.
        """
        score = float(candidate.get("score") or 85.0)
        dna = candidate.get("candidate_dna", {})
        leadership = float(dna.get("leadership", 0.60) or 0.60)
        
        next_role = "tech_lead"
        probability = 0.60 + (score / 100.0) * 0.25
        timeline = "18 months"
        
        if leadership > 0.80:
            next_role = "manager"
            timeline = "12 months"
        elif leadership < 0.50:
            next_role = "staff_engineer"
            timeline = "24 months"
            
        return {
            "next_role": next_role,
            "probability": round(min(0.99, probability), 2),
            "timeline": timeline
        }
