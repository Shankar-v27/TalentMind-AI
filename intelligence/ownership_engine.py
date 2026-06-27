# intelligence/ownership_engine.py

from typing import Dict, Any

class OwnershipEngine:
    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        signals = candidate.get("redrob_signals", {})
        
        # Combine text fields for keyword searching
        text = (profile.get("summary", "") + " " + " ".join(j.get("description", "") for j in history) + " " + " ".join(j.get("title", "") for j in history)).lower()
        
        founder = any(word in text for word in ["founder", "co-founder", "own business", "sole proprietor"])
        team_lead = any(word in text for word in ["lead", "manager", "director", "head", "VP"])
        ownership_keywords = sum(1 for word in ["led", "managed", "owned", "architected", "built", "spearheaded", "designed", "responsible for"] if word in text)
        freelancing = any(word in text for word in ["freelance", "consultant", "independent", "contractor"])
        open_source = any(word in text for word in ["maintainer", "creator", "open source", "open-source", "oss"]) or signals.get("github_activity_score", 0) > 60
        startup = any(word in text for word in ["startup", "early-stage", "series-a", "series-b", "co-founder"])
        mentorship = any(word in text for word in ["mentor", "mentored", "mentoring", "coach", "coached", "coaching", "advise"])
        decision = any(word in text for word in ["decision", "strategy", "strategist", "head of", "executive"])
        
        score = 0.1
        if founder: score += 0.35
        if team_lead: score += 0.20
        if open_source: score += 0.15
        if startup: score += 0.10
        if mentorship: score += 0.10
        if decision: score += 0.10
        score += (min(5, ownership_keywords) / 5.0) * 0.15
        if freelancing: score += 0.05
        
        # Add deterministic variation from candidate ID
        cand_id_num = int("".join(filter(str.isdigit, candidate.get("candidate_id", "0") or "0")) or "0")
        seed_offset = (cand_id_num % 19) / 100.0
        score = max(0.1, min(0.99, score + seed_offset))
        
        if score >= 0.80:
            ownership_type = "HIGH_OWNER"
        elif score >= 0.50:
            ownership_type = "MODERATE_OWNER"
        else:
            ownership_type = "INDIVIDUAL_CONTRIBUTOR"
            
        return {
            "ownership": round(score, 2),
            "ownership_type": ownership_type
        }
