# counterfactual/future_counterfactual.py

from typing import Dict, Any

class FutureCounterfactual:
    def evaluate(self, current_score: float, optimal_path_gain: float) -> Dict[str, Any]:
        """
        Predict future score development over 6, 12, 24, 36, and 60 months assuming path execution.
        """
        return {
            "6_months": round(min(100.0, current_score + (optimal_path_gain * 0.40)), 1),
            "12_months": round(min(100.0, current_score + (optimal_path_gain * 0.65)), 1),
            "24_months": round(min(100.0, current_score + (optimal_path_gain * 0.85)), 1),
            "36_months": round(min(100.0, current_score + (optimal_path_gain * 0.95)), 1),
            "60_months": round(min(100.0, current_score + (optimal_path_gain * 1.00)), 1)
        }
