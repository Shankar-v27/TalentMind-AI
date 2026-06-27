# intelligence/risk_simulator/burnout_predictor.py

from typing import Dict, Any

class BurnoutPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will experience significant career burnout.
        """
        speed = float(candidate.get("candidate_dna", {}).get("speed", 0.6) or 0.6)
        risk = float(candidate.get("candidate_dna", {}).get("risk", 0.4) or 0.4)
        
        # High speed + high risk leads to higher burnout probability
        prob = (speed * 0.5) + (risk * 0.4)
        prob = max(0.05, min(0.95, prob))
        
        severity = "LOW"
        if prob > 0.6:
            severity = "HIGH"
        elif prob > 0.3:
            severity = "MEDIUM"
            
        return {
            "burnout_probability": round(prob, 2),
            "severity": severity
        }
