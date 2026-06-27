# intelligence/risk_simulator/teamlead_predictor.py

from typing import Dict, Any

class TeamLeadPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will secure a Team Lead role, and project expected years.
        """
        leadership = float(candidate.get("candidate_dna", {}).get("leadership", 0.6) or 0.6)
        exp = float(candidate.get("profile", {}).get("years_of_experience", 3.0) or 3.0)
        
        prob = leadership * 0.90
        prob = max(0.1, min(0.99, prob))
        
        # Expected years based on current experience
        expected_years = max(1, int(round(max(0.5, 6.0 - exp))))
        
        return {
            "teamlead_probability": round(prob, 2),
            "expected_years": expected_years
        }
