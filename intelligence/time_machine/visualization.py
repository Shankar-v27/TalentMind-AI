# intelligence/time_machine/visualization.py

from typing import Dict, List, Any

class TimeMachineVisualizationEngine:
    def generate_heatmap_matrix(
        self,
        candidates: List[Dict[str, Any]],
        scenarios_ranks: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Creates heatmaps representing candidate positions across multiple scenarios.
        """
        matrix = []
        for cand in candidates:
            c_id = cand.get("candidate_id") or cand.get("id")
            row = {"candidate_id": c_id, "name": cand.get("name", "Candidate")}
            
            for sc_id, ranked_ids in scenarios_ranks.items():
                try:
                    pos = ranked_ids.index(c_id) + 1
                except ValueError:
                    pos = 999
                row[sc_id] = pos
                
            matrix.append(row)
            
        return {
            "scenarios": list(scenarios_ranks.keys()),
            "matrix": matrix
        }
