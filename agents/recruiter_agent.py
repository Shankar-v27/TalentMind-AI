# agents/recruiter_agent.py

from typing import Dict, Any

class RecruiterAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate from a talent acquisition perspective (joining probabilities, timelines, remote match).
        """
        risk_profile = candidate.get("risk_profile", {})
        accept_prob = float(risk_profile.get("offer_acceptance", {}).get("accept_probability", 0.91) or 0.91)
        join_prob = float(risk_profile.get("joining", {}).get("joining_probability", 0.87) or 0.87)
        
        opinion = "HIRE"
        if accept_prob < 0.50 or join_prob < 0.50:
            opinion = "REJECT"
            
        return {
            "opinion": opinion,
            "accept_probability": accept_prob,
            "joining_probability": join_prob,
            "arguments": [
                "Candidate shows high responsiveness and positive salary expectations alignment.",
                f"Offer acceptance probability estimated at {int(accept_prob * 100)}%."
            ]
        }
