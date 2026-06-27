# intelligence/risk_simulator/salary_predictor.py

from typing import Dict, Any

class SalaryPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate and project compensation progression (LPA) over 1, 2, 5, and 10 years.
        """
        # Deduce current salary
        score = float(candidate.get("score") or 85.0)
        base_salary = 18.0
        if score > 90:
            base_salary = 26.0
        elif score > 80:
            base_salary = 20.0
            
        learning = float(candidate.get("candidate_dna", {}).get("learning", 0.7) or 0.7)
        growth_rate = 1.07 + (learning * 0.12) # 7% to 19% yearly increases
        
        sal1 = base_salary * growth_rate
        sal2 = sal1 * growth_rate
        sal5 = sal2 * (growth_rate ** 3)
        sal10 = sal5 * (growth_rate ** 5)
        
        return {
            "salary_1": int(round(sal1)),
            "salary_2": int(round(sal2)),
            "salary_5": int(round(sal5)),
            "salary_10": int(round(sal10))
        }
