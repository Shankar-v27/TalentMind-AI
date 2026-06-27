# intelligence/risk_engine.py

from typing import Dict, Any

class RiskEngine:
    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        skills = candidate.get("skills", [])
        signals = candidate.get("redrob_signals", {})
        
        # Combine text fields
        text = (profile.get("summary", "") + " " + " ".join(j.get("description", "") for j in history) + " " + " ".join(j.get("title", "") for j in history)).lower()
        
        startup = any(word in text for word in ["startup", "early-stage", "co-founder"])
        freelancing = any(word in text for word in ["freelance", "consultant", "independent", "contractor"])
        founder = any(word in text for word in ["founder", "co-founder", "sole proprietor"])
        research = any(word in text for word in ["research", "r&d", "academic", "thesis", "publications"])
        
        # International proxy
        international = any(word in text for word in ["remote", "international", "global", "overseas", "relocate"]) or signals.get("willing_to_relocate", False)
        
        # Role switches / Transitions
        titles = [j.get("title", "").lower() for j in history]
        unique_titles = len(set(titles))
        role_switches = max(0, unique_titles - 1)
        
        # Career transitions
        career_transitions = len(history)
        
        # Technology changes
        tech_changes = len(skills)
        
        # Weighted score
        score = 0.1
        if startup: score += 0.20
        if founder: score += 0.25
        if freelancing: score += 0.15
        if research: score += 0.05
        if international: score += 0.10
        score += (min(3, role_switches) / 3.0) * 0.10
        score += (min(4, career_transitions) / 4.0) * 0.10
        score += (min(10, tech_changes) / 10.0) * 0.10
        
        # Add deterministic variation from candidate ID
        cand_id_num = int("".join(filter(str.isdigit, candidate.get("candidate_id", "0") or "0")) or "0")
        seed_offset = (cand_id_num % 11) / 100.0
        score = max(0.1, min(0.99, score + seed_offset))
        
        if score >= 0.70:
            risk_profile = "HIGH"
        elif score >= 0.40:
            risk_profile = "MODERATE"
        else:
            risk_profile = "LOW"
            
        return {
            "risk_score": round(score, 2),
            "risk_profile": risk_profile
        }
