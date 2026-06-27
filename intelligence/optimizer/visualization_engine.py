# intelligence/optimizer/visualization_engine.py

from typing import Dict, List, Any

class VisualizationEngine:
    def format_visualization_data(
        self,
        frontier: List[Dict[str, Any]],
        candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Formulates chart coordinates for standard frontend graphs.
        - Pareto frontier points (Quality vs Salary)
        - Tradeoff charts
        """
        pareto_points = []
        for cand in frontier:
            objs = cand.get("objectives", {})
            pareto_points.append({
                "name": cand.get("name"),
                "quality": objs.get("quality", 75.0),
                "salary": objs.get("salary", 15.0),
                "joining": objs.get("joining", 30)
            })
            
        tradeoff_trend = []
        # Sort all candidates by salary to show quality-salary trend
        sorted_by_sal = sorted(candidates, key=lambda x: x.get("objectives", {}).get("salary", 999.0))
        for cand in sorted_by_sal:
            objs = cand.get("objectives", {})
            tradeoff_trend.append({
                "candidate": cand.get("name"),
                "salary": objs.get("salary", 15.0),
                "quality": objs.get("quality", 75.0),
                "retention": objs.get("retention", 85.0),
                "joining": objs.get("joining", 30)
            })
            
        return {
            "pareto_frontier": pareto_points,
            "tradeoff_trend": tradeoff_trend
        }
