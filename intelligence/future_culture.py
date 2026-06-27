# intelligence/future_culture.py

from typing import Dict, Any

class FutureCultureEngine:
    def simulate(self, candidate_dna: Dict[str, float], organization_match_data: Dict[str, float], current_role: str = "Software Engineer") -> Dict[str, Any]:
        match_score = organization_match_data.get("organization_match", 0.75)
        learning = candidate_dna.get("learning", 0.5)
        leadership = candidate_dna.get("leadership", 0.5)
        innovation = candidate_dna.get("innovation", 0.5)
        stability = candidate_dna.get("stability", 0.5)
        
        # Adaptation at 6m
        adapt_6m = round(max(0.1, min(0.99, match_score * 0.6 + learning * 0.4)), 2)
        
        # Growth at 12m
        grow_12m = round(max(0.1, min(0.99, adapt_6m * 0.5 + innovation * 0.3 + candidate_dna.get("collaboration", 0.5) * 0.2)), 2)
        
        # Progression at 24m
        prog_24m = round(max(0.1, min(0.99, grow_12m * 0.4 + leadership * 0.4 + stability * 0.2)), 2)
        
        # Mastery at 36m
        master_36m = round(max(0.1, min(0.99, prog_24m * 0.4 + leadership * 0.4 + learning * 0.2)), 2)
        
        # Predict future role
        future_role = current_role
        if leadership >= 0.75:
            if "engineer" in current_role.lower():
                future_role = "Engineering Manager"
            else:
                future_role = f"Lead {current_role}"
        elif innovation >= 0.75:
            if "engineer" in current_role.lower():
                future_role = "Principal Architect"
            else:
                future_role = f"Senior Innovator"
        else:
            future_role = f"Senior {current_role}"
            
        return {
            "6_months": adapt_6m,
            "12_months": grow_12m,
            "24_months": prog_24m,
            "36_months": master_36m,
            "future_role": future_role,
            "adaptability_forecast": "High" if learning >= 0.70 else "Medium",
            "leadership_forecast": "Leader" if leadership >= 0.70 else "Contributor",
            "innovation_forecast": "Innovator" if innovation >= 0.70 else "Operator",
            "retention_forecast": "Stable" if stability >= 0.60 else "At-Risk"
        }
