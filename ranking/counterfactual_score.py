# ranking/counterfactual_score.py

from typing import Dict, Any

class CounterfactualScorer:
    def calculate(self, metrics: Dict[str, Any]) -> float:
        """
        Formula:
        Counterfactual Score =
            Current Score * 0.35 +
            Future Score * 0.30 +
            Improvement Cost (scaled 0-100) * -0.10 +
            Improvement Time (scaled 0-100) * -0.10 +
            Success Probability * 0.15 * 100 +
            Leadership Growth * 0.10 * 100
        """
        curr_score = float(metrics.get("current_score", 75.0))
        fut_score = float(metrics.get("future_score", 90.0))
        
        # Scale Cost (0 to 100,000 INR -> 0 to 100)
        cost_raw = float(metrics.get("cost_numeric", 15000.0))
        cost_scaled = min(100.0, cost_raw / 1000.0)
        
        # Scale Time (0 to 24 months -> 0 to 100)
        time_raw = float(metrics.get("months_numeric", 6.0))
        time_scaled = min(100.0, time_raw * 4.0)
        
        success_prob = float(metrics.get("success_probability", 0.85)) * 100.0
        leadership = float(metrics.get("leadership_growth", 0.70)) * 100.0
        
        comp_score = (
            (curr_score * 0.35) +
            (fut_score * 0.30) -
            (cost_scaled * 0.10) -
            (time_scaled * 0.10) +
            (success_prob * 0.15) +
            (leadership * 0.10)
        )
        
        return round(max(0.0, min(100.0, comp_score)), 1)
