# intelligence/risk_simulator/switch_predictor.py

from typing import Dict, Any

class SwitchPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will actively initiate job switches in the next 12-18 months.
        """
        stability = float(candidate.get("candidate_dna", {}).get("stability", 0.75) or 0.75)
        learning = float(candidate.get("candidate_dna", {}).get("learning", 0.75) or 0.75)
        
        # High learning velocity + low stability implies a candidate likely to switch often
        prob = (1.0 - stability) * 0.6 + learning * 0.3
        prob = max(0.05, min(0.95, prob))
        
        return {
            "switch_probability": round(prob, 2)
        }
