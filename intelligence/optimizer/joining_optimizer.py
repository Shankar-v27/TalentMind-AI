# intelligence/optimizer/joining_optimizer.py

from typing import Dict, List, Any

class JoiningOptimizer:
    def optimize_joining(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ranks candidates by fastest availability.
        """
        results = []
        for cand in candidates:
            objs = cand.get("objectives", {})
            joining = objs.get("joining", 30)
            
            results.append({
                "candidate_id": cand.get("candidate_id"),
                "name": cand.get("name"),
                "joining_days": joining
            })
            
        sorted_res = sorted(results, key=lambda x: x["joining_days"])
        return {
            "fastest_candidate": sorted_res[0]["candidate_id"] if sorted_res else None,
            "fastest_candidate_name": sorted_res[0]["name"] if sorted_res else "N/A",
            "joining_ranking": sorted_res
        }
