# ranking/risk_score.py

from typing import Dict, Any

class RiskScorer:
    def calculate(self, metrics: Dict[str, Any]) -> float:
        """
        Formula:
        Risk Score =
            Offer Acceptance * 0.10 * 100 +
            Joining * 0.10 * 100 +
            Retention (12 months) * 0.20 * 100 +
            Promotion * 0.15 * 100 +
            Leadership * 0.10 * 100 +
            Success * 0.15 * 100 -
            Burnout * 0.05 * 100 -
            Resignation * 0.05 * 100 -
            Switching * 0.05 * 100 -
            Conflict * 0.05 * 100 +
            Survival * 0.10 * 100
        """
        offer_acc = float(metrics.get("accept_probability", 0.85)) * 100
        joining = float(metrics.get("joining_probability", 0.85)) * 100
        retention = float(metrics.get("retention_12", 0.85)) * 100
        promotion = float(metrics.get("promotion_probability", 0.80)) * 100
        leadership = float(metrics.get("future_leader", 0.75)) * 100
        success = float(metrics.get("success_probability", 0.80)) * 100
        
        burnout = float(metrics.get("burnout_probability", 0.20)) * 100
        resignation = float(metrics.get("resignation_probability", 0.20)) * 100
        switching = float(metrics.get("switch_probability", 0.25)) * 100
        conflict = float(metrics.get("conflict_probability", 0.10)) * 100
        
        survival = float(metrics.get("survival_probability", 0.80)) * 100
        
        score = (
            (offer_acc * 0.10) +
            (joining * 0.10) +
            (retention * 0.20) +
            (promotion * 0.15) +
            (leadership * 0.10) +
            (success * 0.15) -
            (burnout * 0.05) -
            (resignation * 0.05) -
            (switching * 0.05) -
            (conflict * 0.05) +
            (survival * 0.10)
        )
        
        return round(max(0.0, min(100.0, score)), 1)
