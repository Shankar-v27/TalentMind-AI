# intelligence/digital_twin/personality_engine.py

from typing import Dict, Any

class PersonalityEngine:
    def estimate_traits(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Estimate standard OCEAN traits.
        """
        score = float(candidate.get("score", 85))
        
        return {
            "openness": round((score / 100.0) * 0.88 + 0.10, 2),
            "conscientiousness": round((score / 100.0) * 0.74 + 0.15, 2),
            "extroversion": round((score / 100.0) * 0.61 + 0.20, 2),
            "agreeableness": round((score / 100.0) * 0.78 + 0.12, 2),
            "neuroticism": round(1.0 - ((score / 100.0) * 0.85), 2)
        }
