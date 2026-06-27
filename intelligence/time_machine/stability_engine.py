# intelligence/time_machine/stability_engine.py

from typing import Dict, List, Any
import random
import copy

class StabilityEngine:
    def calculate_stability(
        self,
        candidates: List[Dict[str, Any]],
        state: Dict[str, Any],
        ranker: Any,
        weight_engine: Any,
        runs: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Runs multiple rank computations with randomized perturbations to calculate
        the percentage frequency of a candidate retaining a high-percentile position.
        """
        top_k_threshold = max(3, len(candidates) // 4)
        appearances = {c.get("candidate_id") or c.get("id"): 0 for c in candidates}
        
        for _ in range(runs):
            perturbed_state = copy.deepcopy(state)
            
            # Slightly perturb weights randomly
            perturbed_state["skill_weight"] = max(0.05, float(state.get("skill_weight", 0.3)) + random.uniform(-0.15, 0.15))
            perturbed_state["experience_weight"] = max(0.05, float(state.get("experience_weight", 0.2)) + random.uniform(-0.15, 0.15))
            perturbed_state["leadership"] = max(0.05, float(state.get("leadership", 0.3)) + random.uniform(-0.15, 0.15))
            perturbed_state["future_potential"] = max(0.05, float(state.get("future_potential", 0.3)) + random.uniform(-0.15, 0.15))
            
            p_weights = weight_engine.calculate_weights(perturbed_state)
            p_ranks = ranker.rank_candidates(candidates, perturbed_state, p_weights, perturbed_state)
            
            # Record candidates in top group
            for idx, item in enumerate(p_ranks[:top_k_threshold]):
                c_id = item["candidate_id"]
                if c_id in appearances:
                    appearances[c_id] += 1
                    
        # Compute stability percentage
        stability_list = []
        for cand in candidates:
            c_id = cand.get("candidate_id") or cand.get("id")
            count = appearances.get(c_id, 0)
            stability_score = round(count / runs, 2)
            
            stability_list.append({
                "candidate_id": c_id,
                "name": cand.get("name", "Candidate"),
                "stability": stability_score
            })
            
        # Sort by stability descending
        stability_list.sort(key=lambda x: x["stability"], reverse=True)
        return stability_list
