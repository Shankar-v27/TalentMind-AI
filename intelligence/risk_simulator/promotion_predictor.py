# intelligence/risk_simulator/promotion_predictor.py

from typing import Dict, Any

class PromotionPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will earn a promotion within 12-24 months.
        """
        learning = float(candidate.get("candidate_dna", {}).get("learning", 0.75) or 0.75)
        ownership = float(candidate.get("candidate_dna", {}).get("ownership", 0.70) or 0.70)
        execution = float(candidate.get("candidate_dna", {}).get("execution", 0.70) or 0.70)
        
        prob = (learning * 0.4) + (ownership * 0.3) + (execution * 0.3)
        prob = max(0.05, min(0.99, prob))
        
        return {
            "promotion_probability": round(prob, 2)
        }
