# intelligence/career_forecasting/human_capital_value.py

from typing import Dict, Any

class HumanCapitalValuator:
    def calculate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate human capital valuation index out of 100.
        """
        score = float(candidate.get("score") or 85.0)
        dna = candidate.get("candidate_dna", {})
        learning = float(dna.get("learning", 0.75) or 0.75)
        
        current_value = int(round(score))
        future_value = int(round(min(99.0, score + learning * 15.0)))
        business_value = int(round(score * 0.8 + learning * 20.0))
        
        return {
            "current_value": current_value,
            "future_value": future_value,
            "business_value": business_value
        }
