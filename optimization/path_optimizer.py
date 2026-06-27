# optimization/path_optimizer.py

from typing import Dict, List, Any

class PathOptimizer:
    def optimize(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates different optimization paths (fastest, cheapest, highest ROI, etc.)
        """
        paths = []
        for idx, scenario in enumerate(scenarios):
            if not scenario["improvements"]:
                continue
                
            total_cost = 0
            total_months = 0
            total_gain = scenario["total_gain"]
            names = []
            
            for item in scenario["improvements"]:
                names.append(item["name"])
                # Estimate cost and time per item type
                if item["type"] == "skill":
                    total_cost += 5000
                    total_months += 3
                elif item["type"] == "certification":
                    total_cost += 15000
                    total_months += 2
                elif item["type"] == "project":
                    total_cost += 10000
                    total_months += 4
                elif item["type"] == "leadership":
                    total_cost += 0
                    total_months += 6

            roi = round((total_gain * 1000) / (total_cost + 1), 2)
            paths.append({
                "path_name": f"Scenario {idx}",
                "improvements": names,
                "cost": total_cost,
                "months": total_months,
                "score_gain": total_gain,
                "roi": roi
            })
            
        if not paths:
            return {
                "cheapest": {"improvements": [], "cost": 0, "months": 0, "roi": 0},
                "fastest": {"improvements": [], "cost": 0, "months": 0, "roi": 0},
                "highest_roi": {"improvements": [], "cost": 0, "months": 0, "roi": 0},
                "maximum_score": {"improvements": [], "cost": 0, "months": 0, "roi": 0}
            }
            
        cheapest = min(paths, key=lambda x: x["cost"])
        fastest = min(paths, key=lambda x: x["months"])
        highest_roi = max(paths, key=lambda x: x["roi"])
        maximum_score = max(paths, key=lambda x: x["score_gain"])
        
        return {
            "cheapest": cheapest,
            "fastest": fastest,
            "highest_roi": highest_roi,
            "maximum_score": maximum_score
        }
