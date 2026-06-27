# intelligence/retention_engine.py

from typing import Dict, Any

class RetentionEngine:
    def calculate(self, candidate: Dict[str, Any], career_sim: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates retention probability and attrition risks based on job history,
        average tenure, active search indicators, and response statistics.
        """
        signals = candidate.get("redrob_signals", {})
        career = candidate.get("career_history", [])
        
        # Calculate experience years
        experience = float(candidate.get("experience", 0.0) or 0.0)
        num_jobs = len(career)
        if experience <= 0:
            experience = max(1.0, num_jobs * 2.0)
            
        if num_jobs <= 1:
            avg_tenure = experience
        else:
            avg_tenure = experience / num_jobs
            
        # Tenure mapping: 3+ years is stable retention, <1 year indicates switching risks
        if avg_tenure >= 3.0:
            tenure_score = 0.95
        elif avg_tenure >= 2.0:
            tenure_score = 0.82
        elif avg_tenure >= 1.2:
            tenure_score = 0.65
        else:
            tenure_score = 0.35
            
        # Response characteristics
        offer_acc = float(signals.get("offer_acceptance_rate", 0.5))
        response_rate = float(signals.get("recruiter_response_rate", 0.5))
        
        # Career growth acceleration risk (high acceleration can lead to hopping if not promoted)
        velocity = career_sim.get("career_acceleration", 0.5)
        
        # Current job hunting signals
        open_to_work = signals.get("open_to_work_flag", False)
        apps_submitted = float(signals.get("applications_submitted_30d", 0))
        
        job_hunting_risk = 0.0
        if open_to_work:
            job_hunting_risk += 0.25
        if apps_submitted > 5:
            job_hunting_risk += 0.15
        elif apps_submitted > 0:
            job_hunting_risk += 0.05
            
        # Calculate weighted retention score
        retention_base = (tenure_score * 0.4) + (offer_acc * 0.3) + ((1.0 - (response_rate * 0.5)) * 0.3)
        # Higher velocity slightly lowers baseline retention unless matching a high level
        if velocity > 0.7:
            retention_base -= 0.05
            
        # Deduct active search risk
        retention_prob = round(max(0.1, min(0.99, retention_base - (job_hunting_risk * 0.35))), 2)
        attrition_risk = round(1.0 - retention_prob, 2)
        
        return {
            "retention_probability": retention_prob,
            "attrition_risk": attrition_risk,
            "avg_tenure_years": round(avg_tenure, 1),
            "job_hopper_flag": avg_tenure < 1.2
        }
