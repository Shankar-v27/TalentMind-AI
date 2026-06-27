# counterfactual/career_counterfactual.py

from typing import Dict, List, Any

class CareerCounterfactual:
    def evaluate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate different career paths: Stay current, DevOps, Architect, AI Engineer, Manager.
        """
        role = str(candidate.get("role", "")).lower()
        
        # Deduce current salary tier
        current_salary = 18.0 # default 18 LPA
        if "senior" in role or "lead" in role:
            current_salary = 28.0
        elif "research" in role:
            current_salary = 24.0
            
        # Simulate paths
        paths = [
            {"path": "Stay current role", "multiplier": 1.08, "score": 88},
            {"path": "DevOps Architect", "multiplier": 1.35, "score": 94},
            {"path": "Solutions Architect", "multiplier": 1.45, "score": 96},
            {"path": "Staff AI Engineer", "multiplier": 1.60, "score": 98},
            {"path": "Engineering Manager", "multiplier": 1.50, "score": 95}
        ]
        
        # Pick best path based on max multiplier/score
        best = max(paths, key=lambda x: x["score"])
        future_salary_lpa = int(round(current_salary * best["multiplier"]))
        
        return {
            "best_path": best["path"],
            "future_salary": f"{future_salary_lpa} LPA",
            "future_score": best["score"]
        }
