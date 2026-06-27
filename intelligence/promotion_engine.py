# intelligence/promotion_engine.py

from typing import Dict, Any

class PromotionEngine:
    def calculate(self, candidate: Dict[str, Any], career_sim: Dict[str, Any], learning_velocity: float) -> Dict[str, Any]:
        """
        Calculates leadership potential, mentoring, communication, technical depth,
        project ownership, and final promotion probability and timeframe.
        """
        skills = candidate.get("skills", [])
        career = candidate.get("career_history", [])
        signals = candidate.get("redrob_signals", {})
        
        # Technical depth (based on skills and durations)
        num_skills = len(skills)
        total_months = sum(s.get("duration_months", 0) for s in skills)
        avg_duration = total_months / max(1, num_skills)
        technical_depth = min(1.0, (num_skills * 0.04) + (avg_duration / 48.0))
        
        # Leadership, Mentoring, & Project Ownership from career keywords
        leadership_score = 0.3
        mentoring_score = 0.3
        project_ownership = 0.4
        
        for job in career:
            title = job.get("title", "").lower()
            desc = job.get("description", "").lower()
            if any(kw in title for kw in ["lead", "manager", "director", "head", "principal"]):
                leadership_score += 0.2
                project_ownership += 0.15
            if any(kw in desc for kw in ["mentor", "train", "guide", "coach", "lead", "manage"]):
                mentoring_score += 0.15
                leadership_score += 0.1
            if any(kw in desc for kw in ["own", "deliver", "ship", "architect", "deploy", "build"]):
                project_ownership += 0.1
                
        leadership_score = round(min(1.0, leadership_score), 2)
        mentoring_score = round(min(1.0, mentoring_score), 2)
        project_ownership = round(min(1.0, project_ownership), 2)
        
        # Communication indicators
        profile_comp = float(signals.get("profile_completeness_score", 50)) / 100.0
        offer_acc = float(signals.get("offer_acceptance_rate", 0.5))
        communication = round(min(1.0, max(0.2, (profile_comp * 0.5) + (offer_acc * 0.5))), 2)
        
        # Career velocity & growth
        career_velocity = career_sim.get("career_acceleration", 0.5)
        growth_potential = round(min(1.0, (learning_velocity * 0.6) + (career_velocity * 0.4)), 2)
        
        # Overall Promotion Probability (weighted average)
        promotion_prob = round((
            leadership_score * 0.25 + 
            mentoring_score * 0.15 + 
            project_ownership * 0.15 +
            technical_depth * 0.20 + 
            communication * 0.10 + 
            career_velocity * 0.15
        ), 2)
        
        # Identify next role title
        current_level = career_sim.get("current_level", 2)
        next_level = min(8, current_level + 1)
        level_to_role = {
            0: "Junior Engineer",
            1: "Engineer",
            2: "Senior Engineer",
            3: "Tech Lead",
            4: "Engineering Manager",
            5: "Director of Engineering",
            6: "VP of Engineering",
            7: "CTO",
            8: "CTO"
        }
        next_role = level_to_role.get(next_level, "Senior Engineer")
        
        # Set estimated promotion timeline
        if promotion_prob >= 0.8:
            promotion_time = "6 - 12 months"
        elif promotion_prob >= 0.6:
            promotion_time = "12 - 18 months"
        elif promotion_prob >= 0.4:
            promotion_time = "18 - 24 months"
        else:
            promotion_time = "24+ months"
            
        return {
            "promotion_probability": promotion_prob,
            "next_role": next_role,
            "promotion_time": promotion_time,
            "leadership": leadership_score,
            "communication": communication,
            "growth": growth_potential,
            "mentoring": mentoring_score,
            "technical_depth": round(technical_depth, 2),
            "project_ownership": project_ownership,
            "career_velocity": career_velocity
        }
