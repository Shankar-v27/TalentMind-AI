# explainability/risk_explain.py

from typing import Dict, Any

class RiskExplainabilityEngine:
    def explain(self, name: str, metrics: Dict[str, Any]) -> str:
        """
        Generate recruitment workforce outcome explanations.
        """
        tenure_months = metrics.get("expected_month", 36)
        tenure_years = round(tenure_months / 12.0, 1)
        
        offer = int(metrics.get("accept_probability", 0.91) * 100)
        ghost = int(metrics.get("ghosting_probability", 0.04) * 100)
        joining = int(metrics.get("joining_probability", 0.87) * 100)
        retention = int(metrics.get("retention_12", 0.92) * 100)
        promo = int(metrics.get("promotion_probability", 0.84) * 100)
        leader = int(metrics.get("future_leader", 0.81) * 100)
        burn = int(metrics.get("burnout_probability", 0.09) * 100)
        resign = int(metrics.get("resignation_probability", 0.12) * 100)
        teamlead = int(metrics.get("teamlead_probability", 0.79) * 100)
        manager = int(metrics.get("manager_probability", 0.71) * 100)
        success = int(metrics.get("success_probability", 0.90) * 100)
        
        explanation = (
            f"Candidate demonstrates:\n"
            f"✓ Strong ownership\n"
            f"✓ Excellent learning velocity\n"
            f"✓ High leadership potential\n\n"
            f"Risk Analysis:\n"
            f"• Offer Acceptance: {offer}%\n"
            f"• Ghosting: {ghost}%\n"
            f"• Joining: {joining}%\n"
            f"• Retention: {retention}%\n"
            f"• Promotion: {promo}%\n"
            f"• Leadership: {leader}%\n"
            f"• Burnout: {burn}%\n"
            f"• Resignation: {resign}%\n"
            f"• Team Lead: {teamlead}%\n"
            f"• Manager: {manager}%\n"
            f"• Future Success: {success}%\n\n"
            f"The candidate is expected to remain with the organization for approximately "
            f"{tenure_years} years and has a high probability of becoming a technical leader."
        )
        
        return explanation
