# intelligence/optimizer/salary_optimizer.py

from typing import Dict, List, Any

class SalaryOptimizer:
    def optimize_salary(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates Hiring ROI = Quality / Salary.
        Returns candidate with highest ROI.
        """
        best_roi = 0.0
        best_cand = None
        
        results = []
        for cand in candidates:
            objs = cand.get("objectives", {})
            quality = objs.get("quality", 75.0)
            salary = objs.get("salary", 15.0) or 1.0
            
            roi = round(quality / max(1.0, salary), 2)
            results.append({
                "candidate_id": cand.get("candidate_id"),
                "name": cand.get("name"),
                "quality": quality,
                "salary": salary,
                "roi": roi
            })
            
            if roi > best_roi:
                best_roi = roi
                best_cand = cand
                
        return {
            "best_roi": best_cand.get("candidate_id") if best_cand else None,
            "best_candidate_name": best_cand.get("name") if best_cand else "N/A",
            "max_roi": best_roi,
            "roi_breakdown": sorted(results, key=lambda x: x["roi"], reverse=True)
        }
