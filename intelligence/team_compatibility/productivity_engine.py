# intelligence/team_compatibility/productivity_engine.py

from typing import Dict, Any

class ProductivityEngine:
    def evaluate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate candidate contributions to team throughput.
        """
        cand_reliability = candidate_dna["reliability"]
        cand_execution = candidate_dna["problem_solving"]
        
        gain = (cand_reliability + cand_execution) * 0.10
        
        return {
            "productivity_gain": round(min(0.99, gain), 2)
        }
