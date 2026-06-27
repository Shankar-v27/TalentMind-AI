# intelligence/optimizer/decision_engine.py

from typing import Dict, List, Any

class DecisionEngine:
    def recommend_decision(
        self,
        candidates: List[Dict[str, Any]],
        strategy: str = "future_growth"
    ) -> Dict[str, Any]:
        """
        Determines the single best candidate based on strategic filters.
        """
        if not candidates:
            return {"strategy": strategy, "candidate": None, "name": "N/A"}
            
        best_cand = None
        best_score = -999999.0
        
        for cand in candidates:
            objs = cand.get("objectives", {})
            score = 0.0
            
            if strategy == "best_quality":
                score = objs.get("quality", 70.0)
            elif strategy == "future_growth":
                score = objs.get("future", 70.0)
            elif strategy == "best_value":
                # ROI = quality / salary
                score = objs.get("quality", 70.0) / max(1.0, objs.get("salary", 15.0)) * 10.0
            elif strategy == "fastest_joining":
                score = 100.0 - objs.get("joining", 30)
            elif strategy == "lowest_risk":
                score = 100.0 - objs.get("attrition", 15) - objs.get("burnout", 15)
            elif strategy == "highest_innovation":
                score = objs.get("innovation", 70.0)
            elif strategy == "best_leadership":
                score = objs.get("leadership", 70.0)
            elif strategy == "highest_retention":
                score = objs.get("retention", 80.0)
            elif strategy == "best_team_fit":
                score = objs.get("team", 70.0)
            elif strategy == "best_organization_fit":
                score = objs.get("business_value", 70.0)
            else:
                score = objs.get("quality", 70.0)
                
            if score > best_score:
                best_score = score
                best_cand = cand
                
        return {
            "strategy": strategy,
            "candidate_id": best_cand.get("candidate_id") if best_cand else None,
            "name": best_cand.get("name") if best_cand else "N/A",
            "score": round(best_score, 2)
        }
