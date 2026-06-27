# intelligence/risk_simulator/survival_predictor.py

from typing import Dict, Any

class SurvivalPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will successfully adapt and survive past 1 year inside the company's DNA structure.
        """
        # Read organization matching metrics if present, otherwise default
        dna_match = candidate.get("dna_match", {})
        org_match = float(dna_match.get("organization_match", 0.78) or 0.78)
        stability = float(candidate.get("candidate_dna", {}).get("stability", 0.8) or 0.8)
        
        prob = (org_match * 0.6) + (stability * 0.4)
        prob = max(0.1, min(0.99, prob))
        
        return {
            "survival_probability": round(prob, 2)
        }
