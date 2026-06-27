# intelligence/risk_simulator/manager_predictor.py

from typing import Dict, Any

class ManagerPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will secure an Engineering Manager/Management role.
        """
        management = float(candidate.get("candidate_dna", {}).get("management", 0.5) or 0.5)
        collaboration = float(candidate.get("candidate_dna", {}).get("collaboration", 0.6) or 0.6)
        exp = float(candidate.get("profile", {}).get("years_of_experience", 3.0) or 3.0)
        
        prob = (management * 0.70) + (collaboration * 0.30)
        prob = max(0.05, min(0.95, prob))
        
        expected_years = max(2, int(round(max(1.0, 9.0 - exp))))
        
        return {
            "manager_probability": round(prob, 2),
            "expected_years": expected_years
        }
