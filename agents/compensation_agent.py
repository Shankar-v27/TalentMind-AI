# agents/compensation_agent.py

from typing import Dict, Any

class CompensationAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate compensation fit and recruitment budget ROI.
        """
        # Seed values based on score
        score = float(candidate.get("score") or 85.0)
        fit = 0.80 + (score / 100.0) * 0.15
        
        return {
            "salary_fit": round(min(0.99, fit), 2)
        }
