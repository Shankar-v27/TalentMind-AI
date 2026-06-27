# intelligence/learning_velocity.py

from typing import Dict, Any

class LearningVelocityEngine:
    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates learning speed, consistency, diversity, and acceleration.
        Formula: learning velocity = (skill growth + certifications + projects + github + tech diversity) / experience
        """
        skills = candidate.get("skills", [])
        career = candidate.get("career_history", [])
        signals = candidate.get("redrob_signals", {})
        
        # Estimate experience years from career history if not directly present
        experience = float(candidate.get("experience", 0.0) or 0.0)
        if experience <= 0:
            experience = max(1.0, len(career) * 1.5)
            
        # Skill Growth (based on number of skills)
        num_skills = len(skills)
        skill_growth = min(1.0, num_skills / 8.0)
        
        # Certifications (estimated from education profile and skills count)
        certifications = 0.1
        degree_str = ""
        for edu in candidate.get("education", []):
            degree_str += edu.get("degree", "").lower()
        if "certified" in degree_str or "cert" in degree_str:
            certifications += 0.4
        certifications = min(1.0, certifications + (num_skills * 0.05))
        
        # Projects & GitHub
        github_score = float(signals.get("github_activity_score", 0)) / 100.0
        github_score = min(1.0, max(0.0, github_score))
        
        # Technology diversity
        unique_skills = set(s.get("name", "").lower() for s in skills if s.get("name"))
        tech_diversity = min(1.0, len(unique_skills) / 6.0)
        
        # Project complexity
        proj_complexity = 0.5
        for job in career:
            desc = job.get("description", "").lower()
            if any(kw in desc for kw in ["lead", "architect", "scale", "optimize", "redesign", "senior", "neural", "deep"]):
                proj_complexity += 0.15
        proj_complexity = min(1.0, proj_complexity)
        
        # Experience-based normalized formula
        numerator = skill_growth + certifications + proj_complexity + github_score + tech_diversity
        # Normalize experience division to prevent decay to zero for seniors
        raw_velocity = numerator / (1.5 + (experience * 0.15))
        learning_velocity = round(min(1.0, max(0.1, raw_velocity)), 2)
        
        # Determine learning type
        if learning_velocity >= 0.75:
            learning_type = "FAST_LEARNER"
        elif learning_velocity >= 0.45:
            learning_type = "STEADY_DEVELOPER"
        else:
            learning_type = "CONVENTIONAL_PACER"
            
        return {
            "learning_velocity": learning_velocity,
            "learning_type": learning_type,
            "future_learning_capacity": round(min(1.0, learning_velocity * 1.15), 2),
            "learning_consistency": round(0.5 + (github_score * 0.5), 2),
            "learning_diversity": round(tech_diversity, 2),
            "learning_acceleration": round(min(1.0, learning_velocity * 1.05), 2)
        }
