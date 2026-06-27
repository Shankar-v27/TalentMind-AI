# counterfactual/salary_counterfactual.py

from typing import Dict, List, Any

class SalaryCounterfactual:
    def evaluate(self, skills_to_learn: List[str]) -> Dict[str, Any]:
        """
        Calculates expected salary increase (LPA) based on skills acquired.
        """
        increase = 0
        for skill in skills_to_learn:
            s_low = skill.lower()
            if "kubernetes" in s_low or "k8s" in s_low:
                increase += 4
            elif "terraform" in s_low or "iac" in s_low:
                increase += 2
            elif "system design" in s_low or "architecture" in s_low:
                increase += 5
            elif "fastapi" in s_low or "python" in s_low:
                increase += 2
            else:
                increase += 1.5
                
        if increase == 0:
            increase = 3.5
            
        return {
            "salary_increase": f"{int(round(increase))} LPA"
        }
