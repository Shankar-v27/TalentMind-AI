# intelligence/team_compatibility/leadership_engine.py

from typing import Dict, Any

class LeadershipEngine:
    def evaluate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate leadership capacity alignments to avoid power struggles.
        """
        cand_lead = candidate_dna["leadership"]
        team_lead = team_dna["leadership"]
        
        # High leadership in both candidate and team lead creates power friction
        conflict = 0.05
        if cand_lead > 0.75 and team_lead > 0.75:
            conflict = 0.35 + (cand_lead * team_lead) * 0.4
            
        balance = 1.0 - conflict
        
        return {
            "leadership_balance": round(min(0.99, balance), 2),
            "leadership_conflict": round(min(0.99, conflict), 2)
        }
