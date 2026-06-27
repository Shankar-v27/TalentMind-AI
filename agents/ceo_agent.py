# agents/ceo_agent.py

from typing import Dict, Any

class CEOAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate ROI and long-term organization value creation.
        """
        dna = candidate.get("candidate_dna", {})
        ownership = float(dna.get("ownership", 0.70) or 0.70)
        innovation = float(dna.get("innovation", 0.70) or 0.70)
        
        opinion = "HIRE"
        if ownership < 0.50:
            opinion = "REJECT"
            
        return {
            "opinion": opinion,
            "ownership": ownership,
            "innovation": innovation,
            "arguments": [
                f"Candidate ownership index of {int(ownership * 100)}% indicates strong initiative-taking attributes.",
                f"Innovation capability rating of {int(innovation * 100)}% aligns with high growth expectations."
            ]
        }
