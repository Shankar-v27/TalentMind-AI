# intelligence/recruiter_memory/behavior_engine.py

from typing import Dict, List, Any

class BehaviorEngine:
    def calculate_behavior(
        self,
        actions: List[Dict[str, Any]],
        candidates_map: Dict[str, Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Calculates risk tolerance, cost sensitivity, joining speed sensitivity,
        and innovation/future potential preferences.
        """
        behavior = {
            "risk_tolerance": 0.5,
            "cost_sensitivity": 0.5,
            "speed_preference": 0.5,
            "innovation_preference": 0.5,
            "future_potential_preference": 0.5
        }
        
        if not actions:
            return behavior
            
        risk_vals = []
        cost_vals = []
        speed_vals = []
        innov_vals = []
        future_vals = []
        
        for act in actions:
            if act["action"] not in ["hired", "shortlisted", "saved"]:
                continue
                
            cand = candidates_map.get(act["candidate_id"], {})
            signals = cand.get("redrob_signals", {})
            
            # Risk: high risk tolerance means hiring candidates with lower predicted retention or high attrition risk
            retention = float(cand.get("retention_probability", 0.8))
            risk_vals.append(1.0 - retention)
            
            # Cost: high cost sensitivity means hiring low salary candidates
            salary = float(cand.get("salary", signals.get("salary_requirement", 18.0) or 18.0))
            cost_vals.append(1.0 / max(1.0, salary))
            
            # Speed: high speed preference means hiring candidates with small notice periods
            notice = float(cand.get("notice_period", signals.get("notice_period_days", 30) or 30))
            speed_vals.append(1.0 - min(1.0, notice / 90.0))
            
            # Innovation preference
            innov = float(cand.get("innovation_score", 70.0)) / 100.0
            innov_vals.append(innov)
            
            # Future potential
            future = float(cand.get("future_score", 70.0)) / 100.0
            future_vals.append(future)
            
        if risk_vals:
            behavior["risk_tolerance"] = round(sum(risk_vals) / len(risk_vals), 2)
        if cost_vals:
            behavior["cost_sensitivity"] = round(sum(cost_vals) / len(cost_vals), 2)
        if speed_vals:
            behavior["speed_preference"] = round(sum(speed_vals) / len(speed_vals), 2)
        if innov_vals:
            behavior["innovation_preference"] = round(sum(innov_vals) / len(innov_vals), 2)
        if future_vals:
            behavior["future_potential_preference"] = round(sum(future_vals) / len(future_vals), 2)
            
        return behavior
