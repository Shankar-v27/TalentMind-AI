# intelligence/cost_engine.py

from typing import Dict, List, Any

class CostEngine:
    def estimate(self, improvements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Estimate training/certification costs and time investment.
        """
        total_cost = 0
        total_months = 0
        
        for item in improvements:
            t = item.get("type", "")
            if t == "skill":
                total_cost += 5000
                total_months += 3
            elif t == "certification":
                total_cost += 15000
                total_months += 2
            elif t == "project":
                total_cost += 10000
                total_months += 4
            elif t == "leadership":
                total_cost += 0
                total_months += 6
                
        if total_cost == 0:
            total_cost = 15000
        if total_months == 0:
            total_months = 6
            
        return {
            "cost": f"₹{total_cost:,}",
            "months": total_months,
            "cost_numeric": total_cost,
            "months_numeric": total_months
        }
