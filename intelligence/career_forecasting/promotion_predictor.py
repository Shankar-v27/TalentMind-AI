# intelligence/career_forecasting/promotion_predictor.py

from typing import Dict, Any

class PromotionPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate short term promotion metrics.
        """
        dna = candidate.get("candidate_dna", {})
        learning = float(dna.get("learning", 0.75) or 0.75)
        ownership = float(dna.get("ownership", 0.70) or 0.70)
        
        prob = (learning * 0.4 + ownership * 0.6)
        expected_months = 18 if prob > 0.70 else 24
        
        return {
            "promotion_probability": round(min(0.99, prob), 2),
            "expected_months": expected_months
        }
