# intelligence/optimizer/tradeoff_analyzer.py

from typing import Dict, List, Any

class TradeoffAnalyzer:
    def analyze_tradeoffs(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds a comprehensive comparison matrix of tradeoffs when adjusting options.
        Example: What happens if we switch from a high-quality candidate to a budget-optimal candidate?
        """
        if not candidates or len(candidates) < 2:
            return {"tradeoffs": []}
            
        # Identify top candidate by Quality vs Salary vs Notice period
        by_quality = sorted(candidates, key=lambda x: x.get("objectives", {}).get("quality", 0.0), reverse=True)
        by_salary = sorted(candidates, key=lambda x: x.get("objectives", {}).get("salary", 999.0))
        by_joining = sorted(candidates, key=lambda x: x.get("objectives", {}).get("joining", 999.0))
        
        q_best = by_quality[0]
        s_best = by_salary[0]
        j_best = by_joining[0]
        
        # Calculate percentage differences between Quality-best and Salary-best
        q_objs = q_best.get("objectives", {})
        s_objs = s_best.get("objectives", {})
        
        dq_qual = q_objs.get("quality", 75.0)
        ds_qual = s_objs.get("quality", 75.0)
        qual_drop_pct = round(((dq_qual - ds_qual) / max(1.0, dq_qual)) * 100.0, 1)
        
        dq_sal = q_objs.get("salary", 15.0)
        ds_sal = s_objs.get("salary", 15.0)
        salary_save_pct = round(((dq_sal - ds_sal) / max(1.0, dq_sal)) * 100.0, 1)
        
        dq_join = q_objs.get("joining", 30.0)
        ds_join = s_objs.get("joining", 30.0)
        join_change_pct = round(((dq_join - ds_join) / max(1.0, dq_join)) * 100.0, 1)
        
        dq_ret = q_objs.get("retention", 85.0)
        ds_ret = s_objs.get("retention", 85.0)
        ret_change_pct = round(((dq_ret - ds_ret) / max(1.0, dq_ret)) * 100.0, 1)
        
        return {
            "best_quality_candidate": q_best.get("name"),
            "best_salary_candidate": s_best.get("name"),
            "best_joining_candidate": j_best.get("name"),
            "scenarios": [
                {
                    "title": "Switching from Max Quality to Lowest Salary",
                    "impacts": {
                        "quality_loss": f"-{qual_drop_pct}%",
                        "budget_saved": f"+{salary_save_pct}%",
                        "joining_speed_change": f"{'+' if join_change_pct > 0 else ''}{join_change_pct}%",
                        "retention_change": f"{'+' if ret_change_pct > 0 else ''}{ret_change_pct}%"
                    }
                }
            ],
            "tradeoff_matrix": {
                c.get("name"): {
                    "quality": c.get("objectives", {}).get("quality"),
                    "salary": c.get("objectives", {}).get("salary"),
                    "joining": c.get("objectives", {}).get("joining"),
                    "retention": c.get("objectives", {}).get("retention")
                } for c in candidates[:6]
            }
        }
