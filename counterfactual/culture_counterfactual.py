# counterfactual/culture_counterfactual.py

from typing import Dict, Any

class CultureCounterfactual:
    def evaluate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates organizational culture alignment changes and required behavioral adjustments.
        """
        org_fit = float(candidate.get("dna_match", {}).get("organization_match", 0.8) or 0.8)
        
        target_fit = min(0.99, org_fit + 0.14)
        
        return {
            "communication": 10,
            "leadership": 7,
            "culture_fit": round(target_fit, 2)
        }
