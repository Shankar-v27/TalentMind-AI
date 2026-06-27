# intelligence/optimizer/future_value_optimizer.py

from typing import Dict, List, Any

class FutureValueOptimizer:
    def optimize_future_value(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compares Current Value vs Future Value.
        Returns candidate with highest future forecast.
        """
        best_future_cand = None
        max_future = 0.0
        
        results = []
        for cand in candidates:
            objs = cand.get("objectives", {})
            current_v = objs.get("quality", 70.0)
            future_v = objs.get("future", 72.0)
            leadership_v = objs.get("leadership", 65.0)
            innovation_v = objs.get("innovation", 68.0)
            business_v = objs.get("business_value", 70.0)
            
            results.append({
                "candidate_id": cand.get("candidate_id"),
                "name": cand.get("name"),
                "current_value": current_v,
                "future_value": future_v,
                "leadership_value": leadership_v,
                "innovation_value": innovation_v,
                "business_value": business_v
            })
            
            if future_v > max_future:
                max_future = future_v
                best_future_cand = cand
                
        return {
            "best_future": best_future_cand.get("candidate_id") if best_future_cand else None,
            "best_candidate_name": best_future_cand.get("name") if best_future_cand else "N/A",
            "max_future_score": max_future,
            "forecast_list": sorted(results, key=lambda x: x["future_value"], reverse=True)
        }
