# intelligence/risk_simulator/director_predictor.py

from typing import Dict, Any

class DirectorPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will mature to Director/VP tier.
        """
        ownership = float(candidate.get("candidate_dna", {}).get("ownership", 0.6) or 0.6)
        leadership = float(candidate.get("candidate_dna", {}).get("leadership", 0.5) or 0.5)
        exp = float(candidate.get("profile", {}).get("years_of_experience", 3.0) or 3.0)
        
        prob = (ownership * 0.5) + (leadership * 0.5)
        prob = max(0.01, min(0.90, prob * 0.85)) # Directors are rarer
        
        expected_years = max(4, int(round(max(2.0, 14.0 - exp))))
        
        return {
            "director_probability": round(prob, 2),
            "expected_years": expected_years
        }
