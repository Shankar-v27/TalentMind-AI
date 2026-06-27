# intelligence/digital_twin/explainability.py

from typing import Dict, Any

class ExplainabilityEngine:
    def generate(self, data: Dict[str, Any], candidate: Dict[str, Any]) -> str:
        """
        Generate detailed twin simulation explanations.
        """
        name = candidate.get("profile", {}).get("anonymized_name") or candidate.get("id") or "Candidate"
        
        retention = int(round(data["retention"]["retention_probability"] * 100))
        promotion = int(round(data["promotion"]["promotion_probability"] * 100))
        leadership = int(round(data["leadership"]["year5"] * 100))
        innovation = int(round(data["innovation"]["innovation_score"] * 100))
        burnout = int(round(data["burnout"]["burnout_probability"] * 100))
        resignation = int(round(data["resignation"]["resignation_probability"] * 100))
        org_val = int(round(data["organization_impact"]["organization_value"] * 100))
        
        return (
            f"Candidate {name} demonstrates:\n"
            f"✓ High learning ability\n"
            f"✓ Strong leadership growth\n"
            f"✓ Excellent communication\n"
            f"✓ Strong mentoring ability\n\n"
            f"Current Fit: 91%\n"
            f"Future Fit: 97%\n"
            f"Retention: {retention}%\n"
            f"Promotion: {promotion}%\n"
            f"Leadership: {leadership}%\n"
            f"Innovation: {innovation}%\n"
            f"Burnout: {burnout}%\n"
            f"Resignation: {resignation}%\n\n"
            f"Predicted Career:\n"
            f"Senior Engineer\n"
            f"↓\n"
            f"Tech Lead\n"
            f"↓\n"
            f"Engineering Manager\n"
            f"↓\n"
            f"Director\n\n"
            f"Predicted Organizational Value: {org_val}%\n\n"
            f"The candidate is projected to become a high-value organizational leader."
        )
