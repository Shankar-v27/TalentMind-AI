# intelligence/communication_engine.py

from typing import Dict, Any

class CommunicationEngine:
    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        skills = candidate.get("skills", [])
        signals = candidate.get("redrob_signals", {})
        
        # Combine text fields
        text = (profile.get("summary", "") + " " + " ".join(j.get("description", "") for j in history) + " " + " ".join(j.get("title", "") for j in history)).lower()
        
        mentoring = any(word in text for word in ["mentor", "mentored", "mentoring", "coach"])
        linkedin = any(word in text for word in ["linkedin", "social media", "blog", "writing"]) or signals.get("github_activity_score", 0) > 40
        speaking = any(word in text for word in ["speaker", "spoke at", "presented", "talk at", "conference", "meetup"])
        leadership = any(word in text for word in ["lead", "manager", "team lead"])
        manager = any(word in text for word in ["manager", "director", "head", "vp"])
        documentation = any(word in text for word in ["documentation", "spec", "specs", "reports", "writing", "blog"])
        presentations = any(word in text for word in ["presentation", "presentations", "slides", "speak", "demo"])
        
        # Endorsements count proxy
        endorsements = sum(skill.get("endorsements", 0) for skill in skills)
        
        # Recruiter response rate proxy
        response_rate = float(signals.get("recruiter_response_rate", 0.5))
        
        # Weighted score
        score = 0.1
        if mentoring: score += 0.15
        if linkedin: score += 0.10
        if speaking: score += 0.15
        if leadership: score += 0.10
        if manager: score += 0.10
        if documentation: score += 0.15
        if presentations: score += 0.10
        score += response_rate * 0.10
        score += (min(30, endorsements) / 30.0) * 0.10
        
        # Add deterministic variation from candidate ID
        cand_id_num = int("".join(filter(str.isdigit, candidate.get("candidate_id", "0") or "0")) or "0")
        seed_offset = (cand_id_num % 5) / 100.0
        score = max(0.1, min(0.99, score + seed_offset))
        
        return {
            "communication": round(score, 2)
        }
