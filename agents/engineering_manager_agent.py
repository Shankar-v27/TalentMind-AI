# agents/engineering_manager_agent.py

from typing import Dict, Any

class EngineeringManagerAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate system engineering, delivery execution and code scaling capacities.
        """
        score = float(candidate.get("score") or 85.0)
        dna = candidate.get("candidate_dna", {})
        execution = float(dna.get("execution", 0.70) or 0.70)
        
        opinion = "HIRE"
        if score < 75 or execution < 0.60:
            opinion = "REJECT"
            
        return {
            "opinion": opinion,
            "execution_score": execution,
            "arguments": [
                f"Candidate technical capability score of {score}% matches delivery expectations.",
                f"System architectural scaling and execution velocity rated at {int(execution * 100)}%."
            ]
        }
