# agents/hr_agent.py

from typing import Dict, Any

class HRAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate behavioral adaptability, communication competence, and cultural alignment.
        """
        dna = candidate.get("candidate_dna", {})
        collab = float(dna.get("collaboration", 0.70) or 0.70)
        comm = float(dna.get("communication", 0.70) or 0.70)
        
        opinion = "HIRE"
        if collab < 0.55 or comm < 0.55:
            opinion = "REJECT"
            
        return {
            "opinion": opinion,
            "collaboration": collab,
            "communication": comm,
            "arguments": [
                f"Candidate exhibits comfortable teamwork dynamics with a collaboration index of {int(collab * 100)}%.",
                f"Excellent communication markers ({int(comm * 100)}%) ensure alignment in remote setups."
            ]
        }
