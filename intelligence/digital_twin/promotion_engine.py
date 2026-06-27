# intelligence/digital_twin/promotion_engine.py

from typing import Dict, Any

class PromotionEngine:
    def predict_promotion(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate probability of career level promotion.
        """
        score = float(candidate.get("score", 85))
        
        prob = round((score / 100.0) * 0.84 + 0.08, 2)
        
        return {
            "promotion_probability": min(0.99, prob)
        }
