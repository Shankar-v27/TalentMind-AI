# intelligence/team_compatibility/innovation_engine.py

from typing import Dict, Any

class InnovationEngine:
    def evaluate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate innovation boost rate.
        """
        cand_innov = candidate_dna["innovation"]
        cand_create = candidate_dna["creativity"]
        
        boost = (cand_innov + cand_create) * 0.15
        
        return {
            "innovation_boost": round(min(0.99, boost), 2)
        }
