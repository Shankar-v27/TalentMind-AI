# intelligence/optimizer/pareto_engine.py

from typing import Dict, List, Any
import numpy as np

class ParetoEngine:
    def find_pareto_frontier(
        self,
        candidates: List[Dict[str, Any]],
        objectives_list: List[str],
        maximize_flags: List[bool]
    ) -> List[Dict[str, Any]]:
        """
        Identifies candidates on the Pareto-optimal frontier.
        objectives_list: list of objective keys (e.g. ['quality', 'salary'])
        maximize_flags: list of boolean values, True = maximize, False = minimize
        """
        if not candidates:
            return []
            
        # Extract candidate objective values as a NumPy array
        n_candidates = len(candidates)
        n_objectives = len(objectives_list)
        values = np.zeros((n_candidates, n_objectives))
        
        for i, cand in enumerate(candidates):
            obj_vals = cand.get("objectives", {})
            for j, obj_key in enumerate(objectives_list):
                val = obj_vals.get(obj_key, 0.0)
                # If minimizing, invert to simplify dominance calculation
                if not maximize_flags[j]:
                    values[i, j] = -val
                else:
                    values[i, j] = val
                    
        # Determine dominance
        pareto_indices = []
        for i in range(n_candidates):
            dominated = False
            for j in range(n_candidates):
                if i == j:
                    continue
                # i is dominated by j if:
                # 1. j is at least as good as i in all objectives: all(j >= i)
                # 2. j is strictly better than i in at least one objective: any(j > i)
                if np.all(values[j] >= values[i]) and np.any(values[j] > values[i]):
                    dominated = True
                    break
            if not dominated:
                pareto_indices.append(i)
                
        frontier = [candidates[idx] for idx in pareto_indices]
        return frontier

    def calculate_crowding_distance(
        self,
        frontier: List[Dict[str, Any]],
        objectives_list: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Calculates crowding distance to preserve diversity along the Pareto frontier.
        """
        n = len(frontier)
        if n == 0:
            return []
        if n <= 2:
            for item in frontier:
                item["crowding_distance"] = float("inf")
            return frontier
            
        # Initialize distance to 0
        for item in frontier:
            item["crowding_distance"] = 0.0
            
        for obj_key in objectives_list:
            # Sort by objective value
            frontier_sorted = sorted(
                enumerate(frontier),
                key=lambda x: x[1].get("objectives", {}).get(obj_key, 0.0)
            )
            
            # Boundary points have infinite distance
            frontier[frontier_sorted[0][0]]["crowding_distance"] = float("inf")
            frontier[frontier_sorted[-1][0]]["crowding_distance"] = float("inf")
            
            # Normalize step
            min_val = frontier_sorted[0][1].get("objectives", {}).get(obj_key, 0.0)
            max_val = frontier_sorted[-1][1].get("objectives", {}).get(obj_key, 0.0)
            norm_range = max_val - min_val
            if norm_range == 0:
                continue
                
            for k in range(1, n - 1):
                idx = frontier_sorted[k][0]
                prev_val = frontier_sorted[k - 1][1].get("objectives", {}).get(obj_key, 0.0)
                next_val = frontier_sorted[k + 1][1].get("objectives", {}).get(obj_key, 0.0)
                frontier[idx]["crowding_distance"] += (next_val - prev_val) / norm_range
                
        return frontier
