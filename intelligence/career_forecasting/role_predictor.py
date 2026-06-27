# intelligence/career_forecasting/role_predictor.py

from typing import Dict, Any

class RoleBranchPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Predict alternative branch probabilities (Tech Lead vs Architect vs Manager vs Founder).
        """
        dna = candidate.get("candidate_dna", {})
        leadership = float(dna.get("leadership", 0.60) or 0.60)
        innovation = float(dna.get("innovation", 0.60) or 0.60)
        
        manager_prob = int(round(leadership * 40.0 + 10.0))
        founder_prob = int(round(innovation * 20.0 + 2.0))
        architect_prob = int(round((1.0 - leadership) * 30.0 + 10.0))
        tech_lead_prob = max(10, 100 - (manager_prob + founder_prob + architect_prob))
        
        return {
            "predictions": [
                {"role": "Tech Lead", "probability": tech_lead_prob},
                {"role": "Architect", "probability": architect_prob},
                {"role": "Manager", "probability": manager_prob},
                {"role": "Founder", "probability": founder_prob}
            ]
        }
