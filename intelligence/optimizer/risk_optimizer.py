# intelligence/optimizer/risk_optimizer.py

from typing import Dict, Any

class RiskOptimizer:
    def optimize_risk(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predicts attrition risk, resignation likelihood, ghosting probability, and burnout risk.
        Returns a single composite risk factor.
        """
        objs = candidate.get("objectives", {})
        attrition = objs.get("attrition", 15.0) / 100.0
        burnout = objs.get("burnout", 15.0) / 100.0
        
        # Ghosting risk depends on notice period/joining length
        notice = objs.get("joining", 30)
        ghosting = min(0.40, notice * 0.004) # e.g. 90 days notice -> 36% ghosting chance
        
        promotion_failure = 0.12 # baseline default risk
        
        composite_risk = round((attrition * 0.4 + burnout * 0.2 + ghosting * 0.3 + promotion_failure * 0.1), 2)
        
        return {
            "candidate_id": candidate.get("candidate_id"),
            "name": candidate.get("name"),
            "risk": composite_risk,
            "details": {
                "resignation_risk": attrition,
                "burnout_risk": burnout,
                "ghosting_risk": round(ghosting, 2),
                "promotion_failure_risk": promotion_failure
            }
        }
