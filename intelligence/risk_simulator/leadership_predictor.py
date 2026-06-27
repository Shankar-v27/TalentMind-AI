# intelligence/risk_simulator/leadership_predictor.py

from typing import Dict, Any

class LeadershipPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will mature into a significant leadership profile.
        """
        leadership = float(candidate.get("candidate_dna", {}).get("leadership", 0.6) or 0.6)
        communication = float(candidate.get("candidate_dna", {}).get("communication", 0.6) or 0.6)
        
        prob = (leadership * 0.70) + (communication * 0.30)
        prob = max(0.05, min(0.99, prob))
        
        return {
            "future_leader": round(prob, 2)
        }
