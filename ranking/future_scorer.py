# ranking/future_scorer.py

from typing import Dict, Any

class FutureScorer:
    def calculate(self, current_fit: float, twin: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes the multi-year candidate value score.
        Formula:
        Final Future Score = current_fit * 0.30 + future_fit * 0.25 + learning_velocity * 0.15 +
                             promotion_probability * 0.10 + retention_probability * 0.10 +
                             leadership_potential * 0.05 + culture_fit * 0.05
        """
        learning_velocity = float(twin.get("learning_velocity", 0.5))
        career_acc = float(twin.get("career_acceleration", 0.5))
        promo_prob = float(twin.get("promotion_probability", 0.5))
        retention_prob = float(twin.get("retention_probability", 0.5))
        leadership = float(twin.get("leadership_potential", 0.5))
        culture_fit = float(twin.get("culture_fit", 0.5))
        
        # Calculate future fit projection
        # Higher learning velocity and acceleration boost the long-term relevance score
        future_fit = min(1.0, current_fit + (learning_velocity * 0.12) + (career_acc * 0.08))
        
        # Calculate composite score
        future_score = (
            current_fit * 0.30 +
            future_fit * 0.25 +
            learning_velocity * 0.15 +
            promo_prob * 0.10 +
            retention_prob * 0.10 +
            leadership * 0.05 +
            culture_fit * 0.05
        )
        
        return {
            "current_fit": int(round(current_fit * 100)),
            "future_fit": int(round(future_fit * 100)),
            "future_score": int(round(future_score * 100))
        }
