# counterfactual/experience_counterfactual.py

from typing import Dict, Any

class ExperienceCounterfactual:
    def evaluate(self, gaps: Dict[str, Any], current_score: float) -> Dict[str, Any]:
        """
        Determines the additional experience needed in months and the projected score.
        """
        missing_months = gaps.get("missing_experience_months", 0)
        required_months = max(6, missing_months) if missing_months > 0 else 8
        
        future_score = min(100.0, current_score + (required_months * 0.5))
        
        return {
            "required_months": required_months,
            "future_score": round(future_score, 1)
        }
