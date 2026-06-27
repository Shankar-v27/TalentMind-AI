# intelligence/team_compatibility/compatibility_legacy.py

from typing import Dict, Any

class TeamCompatibilityEngine:
    def calculate(self, team_dna: Dict[str, float], candidate_dna: Dict[str, float]) -> Dict[str, Any]:
        if not team_dna:
            team_dna = {
                "speed": 0.70,
                "ownership": 0.65,
                "leadership": 0.60,
                "innovation": 0.65,
                "learning": 0.70,
                "communication": 0.75,
                "risk": 0.40,
                "adaptability": 0.65,
                "stability": 0.75,
                "collaboration": 0.80,
                "execution": 0.70,
                "research": 0.40,
                "team": 0.80
            }
            
        c_research = candidate_dna.get("research", 0.5)
        t_research = team_dna.get("research", 0.5)
        diff_research = abs(c_research - t_research)
        knowledge_diversity_score = diff_research
        if knowledge_diversity_score >= 0.25:
            knowledge_diversity = "HIGH"
        elif knowledge_diversity_score >= 0.12:
            knowledge_diversity = "MODERATE"
        else:
            knowledge_diversity = "STANDARD"
            
        c_comm = candidate_dna.get("communication", 0.5)
        t_comm = team_dna.get("communication", 0.5)
        comm_fit = round(1.0 - abs(c_comm - t_comm) * 0.4, 2)
        
        c_lead = candidate_dna.get("leadership", 0.5)
        t_lead = team_dna.get("leadership", 0.5)
        c_autonomy = candidate_dna.get("autonomy", 0.5)
        
        conflict_prob = 0.05
        if c_lead > 0.75 and t_lead > 0.75:
            conflict_prob += 0.25
        if c_autonomy > 0.85 and team_dna.get("ownership", 0.5) > 0.80:
            conflict_prob += 0.15
            
        c_collab = candidate_dna.get("collaboration", 0.5)
        conflict_prob = max(0.01, min(0.95, conflict_prob - (c_collab * 0.1)))
        
        synergy = round((c_collab + team_dna.get("collaboration", 0.5)) / 2.0 * 0.9 + 0.1, 2)
        personality_div = round(abs(candidate_dna.get("creativity", 0.5) - team_dna.get("stability", 0.5)), 2)
        inno_contrib = round(max(0.1, min(0.99, candidate_dna.get("innovation", 0.5) * 1.1)), 2)
        
        compatibility = round(
            0.30 * comm_fit +
            0.30 * synergy +
            0.20 * (1.0 - conflict_prob) +
            0.10 * (1.0 - abs(c_lead - t_lead)) +
            0.10 * (c_collab),
            2
        )
        
        return {
            "compatibility": compatibility,
            "conflict_probability": round(conflict_prob, 2),
            "knowledge_diversity": knowledge_diversity,
            "synergy": synergy,
            "personality_diversity": personality_div,
            "innovation_contribution": inno_contrib
        }
