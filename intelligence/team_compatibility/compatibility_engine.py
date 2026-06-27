# intelligence/team_compatibility/compatibility_engine.py

from typing import Dict, Any

class CompatibilityEngine:
    def calculate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any], org_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate compatibility values across dimensions.
        """
        comm = candidate_dna["communication"] * 0.5 + team_dna["communication"] * 0.5
        collab = candidate_dna["collaboration"] * 0.5 + team_dna["collaboration"] * 0.5
        
        # Leadership balance is high if candidate leadership capacity fills gaps or fits culture
        leader = 1.0 - abs(candidate_dna["leadership"] - team_dna["leadership"])
        behavior = candidate_dna["team_orientation"]
        knowledge = 0.85
        culture = 1.0 - abs(candidate_dna["risk_appetite"] - org_dna["risk"])
        personality = candidate_dna["adaptability"]
        emotion = candidate_dna["emotional_intelligence"]
        
        score = (comm + collab + leader + behavior + knowledge + culture + personality + emotion) / 8.0
        
        return {
            "compatibility": round(min(0.99, score), 2)
        }
