# intelligence/team_compatibility/mentorship_engine.py

from typing import Dict, Any

class MentorshipEngine:
    def evaluate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate candidate mentoring capacity.
        """
        cand_mentor = candidate_dna["mentoring"]
        avg_exp = float(team_dna["avg_experience"])
        
        # High experience in the team benefits from higher mentoring capabilities
        score = cand_mentor * 0.8 + (avg_exp / 15.0) * 0.2
        
        return {
            "mentor_score": round(min(0.99, score), 2)
        }
