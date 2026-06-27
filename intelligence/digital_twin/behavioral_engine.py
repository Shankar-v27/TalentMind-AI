# intelligence/digital_twin/behavioral_engine.py

from typing import Dict, Any

class BehavioralProfileEngine:
    def predict_profile(self, candidate: Dict[str, Any]) -> Dict[str, str]:
        """
        Classify work style and collaboration profiles.
        """
        score = candidate.get("score", 85)
        
        work_style = "collaborative" if score >= 80 else "independent"
        learning_style = "fast" if score >= 85 else "steady"
        risk = "moderate" if score >= 75 else "low"
        
        return {
            "work_style": work_style,
            "learning_style": learning_style,
            "risk": risk,
            "collaboration_style": "active peer support",
            "communication_style": "transparent",
            "leadership_style": "democratic coaching",
            "decision_style": "data driven",
            "stress_response": "highly resilient"
        }
