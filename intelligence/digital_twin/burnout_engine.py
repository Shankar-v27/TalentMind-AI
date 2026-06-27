# intelligence/digital_twin/burnout_engine.py

from typing import Dict, Any

class BurnoutEngine:
    def predict_burnout(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate probability of psychological burnout.
        """
        score = float(candidate.get("score", 85))
        
        prob = round(1.0 - ((score / 100.0) * 0.92), 2)
        
        return {
            "burnout_probability": max(0.01, prob)
        }
