# intelligence/skill_evolution/future_skill_predictor.py

from typing import Dict, List, Any

class FutureSkillPredictor:
    def predict_future_skills(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forecast future skill milestones.
        """
        return {
            "future_skills": [
                "kubernetes",
                "terraform",
                "cloud_architecture"
            ]
        }

    def forecast_strengths(self, initial_skills: Dict[str, int]) -> Dict[str, Dict[str, int]]:
        """
        Forecast strengths at NOW, 6M, 12M, and 24M for all key skills.
        """
        forecasts = {}
        for skill, val in initial_skills.items():
            forecasts[skill] = {
                "now": val,
                "m6": min(99, int(val + 5)),
                "m12": min(99, int(val + 12)),
                "m24": min(99, int(val + 22))
            }
            
        # Ensure we have defaults if some target keys are missing
        for skill in ["python", "aws", "docker", "leadership", "architecture"]:
            if skill not in forecasts:
                base = 32 if skill == "leadership" else (18 if skill == "architecture" else 50)
                forecasts[skill] = {
                    "now": base,
                    "m6": base + 10,
                    "m12": base + 22,
                    "m24": base + 35
                }
                
        return forecasts
