# intelligence/digital_twin/resignation_engine.py

from typing import Dict, Any

class ResignationEngine:
    def predict_resignation(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate probability of resignation.
        """
        score = float(candidate.get("score", 85))
        
        prob = round(1.0 - ((score / 100.0) * 0.86), 2)
        
        return {
            "resignation_probability": max(0.01, prob)
        }
