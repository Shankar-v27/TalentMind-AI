# intelligence/optimizer/retention_optimizer.py

from typing import Dict, List, Any

class RetentionOptimizer:
    def optimize_retention(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predicts attrition retention percentages across multiple key milestones.
        """
        objs = candidate.get("objectives", {})
        baseline_retention = objs.get("retention", 85.0) / 100.0
        
        # Apply exponential decay to project across timeline increments
        r_6m = round(baseline_retention ** 0.1, 3)
        r_12m = round(baseline_retention ** 0.25, 3)
        r_24m = round(baseline_retention ** 0.5, 3)
        r_60m = round(baseline_retention ** 1.5, 3)
        
        return {
            "candidate_id": candidate.get("candidate_id"),
            "name": candidate.get("name"),
            "retention": baseline_retention,
            "milestones": {
                "6_months": r_6m,
                "12_months": r_12m,
                "24_months": r_24m,
                "60_months": r_60m
            }
        }
