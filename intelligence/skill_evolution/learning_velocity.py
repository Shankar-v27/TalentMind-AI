# intelligence/skill_evolution/learning_velocity.py

from typing import Dict, Any

class LearningVelocityEngine:
    def calculate(self, timeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate learning velocity based on skill timelines.
        """
        timeline = timeline_data.get("timeline", [])
        if not timeline:
            return {"learning_velocity": 1.0, "category": "STANDARD"}
            
        years = max(1, timeline[-1]["year"] - timeline[0]["year"])
        num_skills = len(timeline)
        
        velocity = round(num_skills / float(years), 1)
        
        category = "STANDARD"
        if velocity >= 3.0:
            category = "HIGH"
        elif velocity >= 2.0:
            category = "MODERATE"
            
        return {
            "learning_velocity": velocity,
            "category": category
        }
