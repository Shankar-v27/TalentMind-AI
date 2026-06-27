# intelligence/learning_engine.py

from typing import Dict, Any

class LearningEngine:
    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        skills = candidate.get("skills", [])
        signals = candidate.get("redrob_signals", {})
        
        # Combine text fields
        text = (profile.get("summary", "") + " " + " ".join(j.get("description", "") for j in history) + " " + " ".join(j.get("title", "") for j in history)).lower()
        
        certs = any(word in text for word in ["certif", "certificate", "certified", "aws certified", "pmp", "scrum master"])
        courses = any(word in text for word in ["course", "training", "udemy", "coursera", "edx", "nanodegree"])
        research = any(word in text for word in ["research", "publication", "paper", "thesis", "academic"])
        
        # Technology diversity
        tech_diversity = len(skills)
        
        # Learning consistency (average duration of skills)
        avg_months = sum(skill.get("duration_months", 0) for skill in skills) / max(1, len(skills))
        consistency_score = min(1.0, avg_months / 48.0)
        
        # Skill transitions
        exp_years = max(1.0, sum(skill.get("duration_months", 0) for skill in skills) / 12.0)
        transitions = tech_diversity / exp_years
        
        # GitHub activity proxy
        github = float(signals.get("github_activity_score", 0)) / 100.0
        
        # Weighted score
        score = 0.1
        if certs: score += 0.20
        if courses: score += 0.15
        if research: score += 0.15
        score += (min(10, tech_diversity) / 10.0) * 0.15
        score += consistency_score * 0.15
        score += (min(3.0, transitions) / 3.0) * 0.10
        score += github * 0.10
        
        # Add deterministic variation from candidate ID
        cand_id_num = int("".join(filter(str.isdigit, candidate.get("candidate_id", "0") or "0")) or "0")
        seed_offset = (cand_id_num % 13) / 100.0
        score = max(0.1, min(0.99, score + seed_offset))
        
        if score >= 0.75:
            learning_type = "FAST"
        elif score >= 0.50:
            learning_type = "STEADY"
        else:
            learning_type = "CONVENTIONAL"
            
        return {
            "learning": round(score, 2),
            "learning_type": learning_type
        }
