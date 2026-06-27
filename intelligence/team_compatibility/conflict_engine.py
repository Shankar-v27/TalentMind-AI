# intelligence/team_compatibility/conflict_engine.py

from typing import Dict, Any

class ConflictEngine:
    def evaluate(self, candidate_dna: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate personality and style conflict indices.
        """
        cand_conflict_tol = candidate_dna["conflict_tolerance"]
        cand_eq = candidate_dna["emotional_intelligence"]
        
        # Conflict probability is higher if emotional intelligence and tolerance are very low
        prob = (1.0 - cand_eq) * 0.6 + (1.0 - cand_conflict_tol) * 0.4
        prob = max(0.01, prob * 0.15) # scaled down for reasonable real-world predictions
        
        return {
            "conflict_probability": round(min(0.99, prob), 2)
        }
