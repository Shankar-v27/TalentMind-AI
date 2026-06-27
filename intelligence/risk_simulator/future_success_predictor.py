# intelligence/risk_simulator/future_success_predictor.py

from typing import Dict, Any

class FutureSuccessPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate becomes a top tier contributor, and classify their trajectory.
        """
        learning = float(candidate.get("candidate_dna", {}).get("learning", 0.7) or 0.7)
        innovation = float(candidate.get("candidate_dna", {}).get("innovation", 0.6) or 0.6)
        score = float(candidate.get("score") or 85.0)
        
        prob = (learning * 0.4) + (innovation * 0.3) + ((score / 100.0) * 0.3)
        prob = max(0.1, min(0.99, prob))
        
        classification = "AVERAGE_EMPLOYEE"
        if prob > 0.88:
            classification = "TOP_TALENT"
        elif prob > 0.78:
            classification = "INNOVATOR"
        elif prob > 0.68:
            classification = "LEADER"
        elif prob > 0.50:
            classification = "HIGH_PERFORMER"
            
        return {
            "success_probability": round(prob, 2),
            "classification": classification
        }
