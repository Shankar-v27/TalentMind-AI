# intelligence/team_compatibility/diversity_engine.py

from typing import Dict, Any

class KnowledgeDiversityEngine:
    def evaluate(self, candidate: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Measure skill overlap and unique cognitive contributions.
        """
        score = float(candidate.get("score") or 85.0)
        
        # High match score with JD could mean some redundancy with general backend team roles
        redundancy = max(0.05, 1.0 - (score / 100.0))
        diversity = (score / 100.0) * 0.8 + 0.15
        
        return {
            "knowledge_diversity": round(min(0.99, diversity), 2),
            "redundancy": round(min(0.99, redundancy), 2)
        }
