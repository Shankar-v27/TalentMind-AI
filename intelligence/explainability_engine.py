# intelligence/explainability_engine.py

from typing import Dict, Any

class ExplainabilityEngine:
    def explain(
        self,
        candidate_name: str,
        candidate_dna: Dict[str, float],
        sim_data: Dict[str, float],
        personality: Dict[str, str],
        future_data: Dict[str, Any],
        failure_data: Dict[str, Any]
    ) -> str:
        """
        Generates structured, easy-to-read recruiter explanations of alignment,
        matching candidate profile vectors with target organizational configurations.
        """
        ownership_val = candidate_dna.get("ownership", 0.5)
        inno_val = candidate_dna.get("innovation", 0.5)
        adapt_val = candidate_dna.get("adaptability", 0.5)
        lead_val = candidate_dna.get("leadership", 0.5)
        
        ownership_desc = "strong" if ownership_val >= 0.70 else "moderate"
        inno_desc = "high" if inno_val >= 0.70 else "steady"
        adapt_desc = "excellent" if adapt_val >= 0.70 else "solid"
        lead_desc = "strong" if lead_val >= 0.70 else "reliable"
        
        org_match_percent = int(sim_data.get("organization_match", 0.75) * 100)
        retention_percent = int(candidate_dna.get("stability", 0.75) * 100)
        
        primary_persona = personality.get("primary", "Builder")
        secondary_persona = personality.get("secondary", "Innovator")
        
        future_role = future_data.get("future_role", "Engineering Manager")
        failure_risk_label = failure_data.get("risk", "LOW").lower()
        
        explanation = (
            f"Candidate demonstrates {ownership_desc} ownership, "
            f"{inno_desc} innovation capability, "
            f"{adapt_desc} adaptability, "
            f"and {lead_desc} leadership growth. "
            f"Organization DNA similarity is {org_match_percent}%. "
            f"The candidate exhibits a {primary_persona}-{secondary_persona} personality profile, "
            f"matching the company's culture. "
            f"Predicted retention probability is {retention_percent}%. "
            f"Future leadership potential is high, "
            f"with an estimated promotion to {future_role} "
            f"within 18 months. "
            f"Culture failure risk remains {failure_risk_label}."
        )
        return explanation
