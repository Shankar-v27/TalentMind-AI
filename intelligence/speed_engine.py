# intelligence/speed_engine.py

from typing import Dict, Any

class SpeedEngine:
    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        profile = candidate.get("profile", {})
        skills = candidate.get("skills", [])
        history = candidate.get("career_history", [])
        signals = candidate.get("redrob_signals", {})
        
        # Calculate experience years
        total_months = sum(skill.get("duration_months", 0) for skill in skills)
        exp_years = max(1.0, total_months / 12.0)
        
        # Projects per year (proxy from job changes)
        num_jobs = len(history)
        projects_per_year = num_jobs / exp_years
        
        # Skills acquired per year
        skills_per_year = len(skills) / exp_years
        
        # Tech transitions
        tech_transitions = len(skills)
        
        # GitHub activity and commits proxy
        github_score = float(signals.get("github_activity_score", 0)) / 100.0
        
        # Hackathons, research publications, freelancing projects search in summary/description
        text = (profile.get("summary", "") + " " + " ".join(j.get("description", "") for j in history) + " " + " ".join(j.get("title", "") for j in history)).lower()
        
        hackathons = text.count("hackathon") + text.count("competition")
        publications = text.count("publication") + text.count("research paper") + text.count("patent")
        freelancing = text.count("freelance") + text.count("consultant") + text.count("contract")
        
        # Promotions
        senior_roles = sum(1 for j in history if any(term in j.get("title", "").lower() for term in ["lead", "senior", "principal", "manager", "head", "director"]))
        promotions_per_year = senior_roles / exp_years
        
        # Combine into score
        speed_score = (
            (min(2.0, projects_per_year) / 2.0) * 0.15 +
            (min(5.0, skills_per_year) / 5.0) * 0.15 +
            (min(1.0, promotions_per_year) / 1.0) * 0.10 +
            (min(15.0, tech_transitions) / 15.0) * 0.10 +
            github_score * 0.20 +
            (min(3, hackathons) / 3.0) * 0.10 +
            (min(3, publications) / 3.0) * 0.10 +
            (min(3, freelancing) / 3.0) * 0.10
        )
        
        # Add deterministic variation from candidate ID
        cand_id_num = int("".join(filter(str.isdigit, candidate.get("candidate_id", "0") or "0")) or "0")
        seed_offset = (cand_id_num % 17) / 100.0
        speed_score = max(0.1, min(0.99, speed_score + seed_offset))
        
        if speed_score >= 0.75:
            work_speed = "FAST"
        elif speed_score >= 0.50:
            work_speed = "STEADY"
        else:
            work_speed = "CONVENTIONAL"
            
        return {
            "speed_score": round(speed_score, 2),
            "work_speed": work_speed
        }
