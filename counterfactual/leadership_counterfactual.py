# counterfactual/leadership_counterfactual.py

from typing import Dict, Any

class LeadershipCounterfactual:
    def evaluate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines the actions required to transition to a management/leadership tier.
        """
        curr_lead = float(candidate.get("candidate_dna", {}).get("leadership", 0.5) or 0.5)
        
        target_leadership = min(0.99, curr_lead + 0.3)
        mentor_count = 2 if curr_lead < 0.6 else 1
        lead_proj_count = 1 if curr_lead >= 0.6 else 2
        
        return {
            "mentor": mentor_count,
            "lead_projects": lead_proj_count,
            "future_leadership": round(target_leadership, 2)
        }
