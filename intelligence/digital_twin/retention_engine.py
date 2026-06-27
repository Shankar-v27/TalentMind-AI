# intelligence/digital_twin/retention_engine.py

from typing import Dict, Any

class RetentionEngine:
    def predict_retention(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate probability of staying in organization.
        """
        score = float(candidate.get("score", 85))
        
        prob = round((score / 100.0) * 0.91 + 0.05, 2)
        
        return {
            "retention_probability": min(0.99, prob)
        }
