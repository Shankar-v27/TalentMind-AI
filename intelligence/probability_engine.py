# intelligence/probability_engine.py

from typing import Dict, List, Any

class ProbabilityEngine:
    def calculate(self, candidate: Dict[str, Any], improvements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate success probability of candidate completing the path based on learning velocity.
        """
        learning_velocity = float(candidate.get("candidate_dna", {}).get("learning", 0.75) or 0.75)
        stability = float(candidate.get("candidate_dna", {}).get("stability", 0.8) or 0.8)
        
        # Base probability is the average of learning and stability
        base_prob = (learning_velocity + stability) / 2.0
        
        # Complexity penalty
        complexity_penalty = len(improvements) * 0.03
        
        success_prob = max(0.5, min(0.99, base_prob - complexity_penalty))
        
        return {
            "success_probability": round(success_prob, 2)
        }
