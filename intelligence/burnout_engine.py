# intelligence/burnout_engine.py

from typing import Dict, Any

class BurnoutEngine:
    def calculate(self, candidate: Dict[str, Any], learning_velocity: float, career_sim: Dict[str, Any], retention_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates burnout probability and risk category by assessing skill overload,
        stagnation, promotion speed, job instability, and activity indicators.
        """
        signals = candidate.get("redrob_signals", {})
        skills = candidate.get("skills", [])
        
        # Workload & Skill overload (more tools = higher workload management demands)
        num_skills = len(skills)
        skill_overload = min(1.0, num_skills / 12.0)
        
        # Rapid promotions (extremely fast scaling induces mental pressure)
        acceleration = career_sim.get("career_acceleration", 0.5)
        rapid_promotions = max(0.0, acceleration - 0.6) * 2.0
        
        # Stagnation (long tenure at low-level roles without progression induces disengagement)
        experience = float(candidate.get("experience", 0.0) or 0.0)
        current_level = career_sim.get("current_level", 2)
        
        stagnation_risk = 0.0
        if experience > 6.0 and current_level <= 2:
            stagnation_risk = min(1.0, (experience - 6.0) * 0.1)
            
        # Career stress indicators (application volumes + github output + learning intensity)
        apps = float(signals.get("applications_submitted_30d", 0))
        github = float(signals.get("github_activity_score", 0)) / 100.0
        
        career_stress = (apps / 25.0 * 0.4) + (github * 0.3) + (learning_velocity * 0.3)
        career_stress = min(1.0, max(0.0, career_stress))
        
        # Job instability (constant job hopping causes stress)
        job_instability = 0.2 if retention_data.get("job_hopper_flag", False) else 0.0
        
        # Composite score
        burnout_base = (
            skill_overload * 0.20 + 
            rapid_promotions * 0.20 + 
            stagnation_risk * 0.20 + 
            career_stress * 0.30 + 
            job_instability
        )
        
        # Cap burnout probability at logical levels (no one is 100% burned out at recruitment stage)
        burnout_prob = round(max(0.02, min(0.85, burnout_base)), 2)
        
        if burnout_prob >= 0.65:
            risk = "HIGH"
        elif burnout_prob >= 0.35:
            risk = "MEDIUM"
        else:
            risk = "LOW"
            
        return {
            "burnout_probability": burnout_prob,
            "risk": risk,
            "career_stress": round(career_stress, 2),
            "skill_overload": round(skill_overload, 2),
            "career_stagnation": round(stagnation_risk, 2)
        }
