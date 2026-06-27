# intelligence/leadership_engine.py

from typing import Dict, Any

class LeadershipEngine:
    def predict(self, candidate: Dict[str, Any], career_sim: Dict[str, Any], learning_velocity: float) -> Dict[str, float]:
        """
        Projects leadership scoring over 6, 12, and 36 months based on past roles,
        mentorship signals, and velocity variables.
        """
        career = candidate.get("career_history", [])
        
        # Establish base level from current hierarchy depth
        current_level = career_sim.get("current_level", 2)
        base_leadership = 0.25 + (current_level * 0.07)
        
        # Scan job titles and descriptions for management signals
        bonus = 0.0
        for job in career:
            title = job.get("title", "").lower()
            desc = job.get("description", "").lower()
            if any(kw in title for kw in ["lead", "manager", "head", "director", "vp", "chief", "cto", "founder"]):
                bonus += 0.08
            if any(kw in desc for kw in ["mentor", "lead team", "manage", "budget", "supervise", "structure"]):
                bonus += 0.04
                
        current = round(max(0.1, min(0.95, base_leadership + bonus)), 2)
        
        # Calculate velocity factor (how fast does leadership capacity mature?)
        acceleration = career_sim.get("career_acceleration", 0.5)
        growth_rate = 0.04 + (learning_velocity * 0.04) + (acceleration * 0.04)
        
        # Project future state
        proj_6m = round(min(0.99, current + (growth_rate * 0.5)), 2)
        proj_12m = round(min(0.99, current + (growth_rate * 1.0)), 2)
        proj_36m = round(min(0.99, current + (growth_rate * 3.0)), 2)
        
        return {
            "current": current,
            "6_months": proj_6m,
            "12_months": proj_12m,
            "36_months": proj_36m
        }

    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        New interface for Organizational DNA Matching Engine.
        """
        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        signals = candidate.get("redrob_signals", {})
        
        # Combine text fields
        text = (profile.get("summary", "") + " " + " ".join(j.get("description", "") for j in history) + " " + " ".join(j.get("title", "") for j in history)).lower()
        
        # Team size proxy
        team_size = 0
        if "team of" in text:
            import re
            match = re.search(r"team of (\d+)", text)
            if match:
                team_size = int(match.group(1))
        if team_size == 0:
            if "large team" in text: team_size = 15
            elif "team lead" in text or "managed" in text: team_size = 5
            
        mentoring = any(word in text for word in ["mentor", "coached", "mentored", "tutored", "teach"])
        mgmt = any(word in text for word in ["management", "manager", "director", "head", "vp", "lead"])
        
        # promotion speed proxy
        exp_years = max(1.0, sum(skill.get("duration_months", 0) for skill in candidate.get("skills", [])) / 12.0)
        senior_roles = sum(1 for j in history if any(term in j.get("title", "").lower() for term in ["lead", "senior", "principal", "manager", "head", "director"]))
        promotion_speed = senior_roles / exp_years
        
        ownership = any(word in text for word in ["led", "owned", "spearheaded", "architected", "founder"])
        decision = any(word in text for word in ["decision", "budget", "strategy", "hired", "fired", "authorized"])
        comm = float(signals.get("recruiter_response_rate", 0.5))
        conflict = any(word in text for word in ["conflict", "resolution", "negotiated", "facilitated", "collaborated"])
        
        score = 0.1
        if mgmt: score += 0.25
        if mentoring: score += 0.15
        if ownership: score += 0.15
        if decision: score += 0.15
        if conflict: score += 0.10
        score += comm * 0.10
        score += (min(10, team_size) / 10.0) * 0.10
        score += (min(1.0, promotion_speed) / 1.0) * 0.10
        
        # Add deterministic variation from candidate ID
        cand_id_num = int("".join(filter(str.isdigit, candidate.get("candidate_id", "0") or "0")) or "0")
        seed_offset = (cand_id_num % 7) / 100.0
        score = max(0.1, min(0.99, score + seed_offset))
        
        return {
            "leadership": round(score, 2),
            "future_leader": score >= 0.70
        }
