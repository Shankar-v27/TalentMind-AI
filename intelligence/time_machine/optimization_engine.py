# intelligence/time_machine/optimization_engine.py

from typing import Dict, List, Any

class OptimizationEngine:
    def optimize_hiring(self, candidates: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Determines the single best candidate profile optimized for specific categories.
        """
        if not candidates:
            return {}
            
        best_future = None
        best_future_score = -1.0
        
        best_cost = None
        best_cost_val = 99999.0
        
        best_joining = None
        best_joining_days = 999.0
        
        best_retention = None
        best_retention_prob = -1.0
        
        best_innovation = None
        best_inno_score = -1.0
        
        best_leadership = None
        best_lead_score = -1.0
        
        for cand in candidates:
            name = cand.get("name", "Unknown Candidate")
            cand_signals = cand.get("redrob_signals", {})
            
            # Future Potential
            fut = float(cand.get("future_score", cand.get("score", 70) * 1.05))
            if fut > best_future_score:
                best_future_score = fut
                best_future = name
                
            # Cost (lower is better)
            sal = float(cand.get("salary", cand_signals.get("salary_requirement", 15.0) or 15.0))
            if sal < best_cost_val:
                best_cost_val = sal
                best_cost = name
                
            # Joining Notice Period (lower is better)
            notice = float(cand.get("notice_period", cand_signals.get("notice_period_days", 30) or 30))
            if notice < best_joining_days:
                best_joining_days = notice
                best_joining = name
                
            # Retention
            ret = float(cand.get("retention_probability", 0.85))
            if ret > best_retention_prob:
                best_retention_prob = ret
                best_retention = name
                
            # Innovation
            inno = float(cand.get("innovation_score", cand.get("score", 70) * 0.98))
            if inno > best_inno_score:
                best_inno_score = inno
                best_innovation = name
                
            # Leadership
            lead = float(cand.get("leadership_score", cand.get("score", 70) * 0.95))
            if lead > best_lead_score:
                best_lead_score = lead
                best_leadership = name
                
        return {
            "best_future": best_future,
            "best_cost": best_cost,
            "best_joining": best_joining,
            "best_retention": best_retention,
            "best_innovation": best_innovation,
            "best_leadership": best_leadership
        }
