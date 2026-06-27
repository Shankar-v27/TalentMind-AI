# intelligence/career_forecasting/career_velocity.py

from typing import Dict, Any
from intelligence.career_forecasting.career_graph import CAREER_LEVELS

class CareerVelocityEngine:
    def calculate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate vertical career movement levels per year of experience.
        """
        experience_years = float(candidate.get("experience", 4.0) or 4.0)
        if experience_years <= 0:
            experience_years = 1.0
            
        history = candidate.get("career_history", [])
        
        # Calculate level progression from first job to current
        start_level = CAREER_LEVELS["engineer"]
        end_level = CAREER_LEVELS["senior_engineer"]
        
        if len(history) >= 2:
            first_role = history[-1].get("role", "").lower()
            last_role = history[0].get("role", "").lower()
            
            for key, val in CAREER_LEVELS.items():
                if key in first_role:
                    start_level = val
                if key in last_role:
                    end_level = val
                    
        level_delta = max(1, end_level - start_level)
        velocity = level_delta / experience_years
        
        classification = "STEADY_GROWTH"
        if velocity > 0.75:
            classification = "HYPER_GROWTH"
        elif velocity > 0.50:
            classification = "FAST_GROWTH"
        elif velocity < 0.25:
            classification = "STAGNANT"
            
        return {
            "velocity": round(velocity, 2),
            "classification": classification
        }
