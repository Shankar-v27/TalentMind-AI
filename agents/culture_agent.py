# agents/culture_agent.py

from typing import Dict, Any

class CultureAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate organizational DNA and communication compatibility score.
        """
        dna_match = candidate.get("dna_match", {})
        org_match = float(dna_match.get("organization_match", 0.85) or 0.85)
        
        return {
            "culture_fit": round(org_match, 2)
        }
