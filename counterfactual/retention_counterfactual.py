# counterfactual/retention_counterfactual.py

from typing import Dict, Any

class RetentionCounterfactual:
    def evaluate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate retention outcomes under different interventions (salary, remote, stock options).
        """
        stability = float(candidate.get("candidate_dna", {}).get("stability", 0.7) or 0.7)
        
        # Strategies and potential retention gains
        strategies = [
            {"name": "salary increase", "gain": 0.15},
            {"name": "promotion", "gain": 0.22},
            {"name": "remote work", "gain": 0.18},
            {"name": "hybrid work", "gain": 0.10},
            {"name": "leadership role", "gain": 0.20},
            {"name": "stock options", "gain": 0.16}
        ]
        
        # Select best strategy
        best = max(strategies, key=lambda x: x["gain"])
        final_retention = min(0.99, stability + best["gain"])
        
        return {
            "best_strategy": best["name"],
            "retention": round(final_retention, 2)
        }
