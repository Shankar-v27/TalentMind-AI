# intelligence/career_forecasting/salary_predictor.py

from typing import Dict, Any

class SalaryProgressionPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate and forecast LPA salary projections over 10 years.
        """
        score = float(candidate.get("score") or 85.0)
        
        salary_now = int(round(score * 0.15 + 6.0))
        salary_1 = int(round(salary_now * 1.15))
        salary_2 = int(round(salary_now * 1.35))
        salary_5 = int(round(salary_now * 1.90))
        salary_10 = int(round(salary_now * 3.40))
        
        return {
            "salary_now": salary_now,
            "salary_1": salary_1,
            "salary_2": salary_2,
            "salary_5": salary_5,
            "salary_10": salary_10
        }
