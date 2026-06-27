# intelligence/digital_twin/leadership_forecast.py

from typing import Dict, Any

class LeadershipForecastEngine:
    def predict_leadership(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate leadership capacity increases over time.
        """
        score = float(candidate.get("score", 85))
        
        today = round((score / 100.0) * 0.34 + 0.05, 2)
        y2 = round(min(0.99, today + 0.38), 2)
        y5 = round(min(0.99, today + 0.57), 2)
        
        return {
            "today": today,
            "year2": y2,
            "year5": y5
        }
