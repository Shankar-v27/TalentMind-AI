# intelligence/time_machine/simulation_engine.py

from typing import Dict, List, Any
import random
import copy

class SimulationEngine:
    def run_monte_carlo(
        self,
        candidates: List[Dict[str, Any]],
        state: Dict[str, Any],
        ranker: Any,
        weight_engine: Any,
        runs: int = 1000
    ) -> Dict[str, float]:
        """
        Runs Monte Carlo simulations over random recruiter state adjustments.
        Computes win frequency (Rank 1 count) for each candidate.
        """
        win_counts = {c.get("candidate_id") or c.get("id"): 0 for c in candidates}
        
        # Optimize loops
        cand_list = list(candidates)
        
        for _ in range(runs):
            sim_state = copy.deepcopy(state)
            
            # Randomize requirements slightly to simulate different universes
            sim_state["experience"] = max(0, int(state.get("experience", 5)) + random.randint(-2, 2))
            sim_state["salary"] = max(5, int(state.get("salary", 20)) + random.randint(-5, 5))
            sim_state["joining"] = max(15, int(state.get("joining", 60)) + random.randint(-30, 30))
            
            # Dynamic weights
            sim_state["skill_weight"] = max(0.05, float(state.get("skill_weight", 0.3)) + random.uniform(-0.2, 0.2))
            sim_state["experience_weight"] = max(0.05, float(state.get("experience_weight", 0.2)) + random.uniform(-0.2, 0.2))
            sim_state["leadership"] = max(0.05, float(state.get("leadership", 0.3)) + random.uniform(-0.2, 0.2))
            sim_state["future_potential"] = max(0.05, float(state.get("future_potential", 0.3)) + random.uniform(-0.2, 0.2))
            
            weights = weight_engine.calculate_weights(sim_state)
            ranks = ranker.rank_candidates(cand_list, sim_state, weights, sim_state)
            
            if ranks:
                winner_id = ranks[0]["candidate_id"]
                if winner_id in win_counts:
                    win_counts[winner_id] += 1
                    
        # Convert to percentages
        results = {}
        for c_id, wins in win_counts.items():
            pct = round((wins / runs) * 100.0, 1)
            results[c_id] = pct
            
        return results
