# intelligence/time_machine/impact_engine.py

from typing import Dict, List, Any

class ImpactEngine:
    def calculate_impact(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculates organizational synergy and team compatibility metrics for the candidate.
        """
        cand_score = float(candidate.get("score", 80))
        
        # Calculate impact indexes
        innovation_impact = round(max(0.1, min(0.99, (cand_score * 1.08) / 100.0)), 2)
        team_synergy = round(max(0.1, min(0.99, (cand_score * 0.95 + 10.0) / 100.0)), 2)
        retention_stability = float(candidate.get("retention_probability", 0.88))
        productivity_boost = round(max(0.1, min(0.99, (cand_score * 1.15) / 100.0)), 2)
        leadership_growth = round(max(0.1, min(0.99, (cand_score * 0.92) / 100.0)), 2)
        
        return {
            "innovation": innovation_impact,
            "team": team_synergy,
            "retention": retention_stability,
            "productivity": productivity_boost,
            "leadership": leadership_growth
        }
