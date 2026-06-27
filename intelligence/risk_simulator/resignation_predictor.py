# intelligence/risk_simulator/resignation_predictor.py

from typing import Dict, Any

class ResignationPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will resign within 24 months, and project the expected month of exit.
        """
        stability = float(candidate.get("candidate_dna", {}).get("stability", 0.8) or 0.8)
        burnout = float(candidate.get("candidate_dna", {}).get("risk", 0.4) or 0.4)
        
        # Base resignation probability
        prob = max(0.05, min(0.95, (1.0 - stability) * 0.7 + burnout * 0.3))
        
        # Project expected tenure month (decaying from 48 months downward)
        expected_month = int(round(48.0 * stability))
        expected_month = max(6, min(60, expected_month))
        
        return {
            "resignation_probability": round(prob, 2),
            "expected_month": expected_month
        }
