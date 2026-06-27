# intelligence/career_forecasting/founder_predictor.py

from typing import Dict, Any

class FounderPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate's startup founder branch probability.
        """
        dna = candidate.get("candidate_dna", {})
        innovation = float(dna.get("innovation", 0.60) or 0.60)
        risk_appetite = float(dna.get("risk", 0.40) or 0.40)
        
        prob = (innovation * 0.6 + risk_appetite * 0.4)
        
        return {
            "founder_probability": round(min(0.99, prob), 2)
        }
