# intelligence/time_machine/sensitivity_engine.py

from typing import Dict, List, Any
import copy

class SensitivityEngine:
    def analyze_sensitivity(
        self,
        candidates: List[Dict[str, Any]],
        state: Dict[str, Any],
        ranker: Any,
        weight_engine: Any,
        constraint_engine: Any
    ) -> Dict[str, float]:
        """
        Perturbs each variable to calculate the sensitivity index (rank shift delta).
        Returns percentage sensitivity impact for each key variable.
        """
        variables = ["experience", "skills", "salary", "joining", "leadership"]
        base_weights = weight_engine.calculate_weights(state)
        base_constraints = constraint_engine.check_constraints(candidates[0] if candidates else {}, state)
        
        # Calculate baseline ranking
        baseline_ranks = ranker.rank_candidates(candidates, state, base_weights, state)
        baseline_positions = {item["candidate_id"]: idx for idx, item in enumerate(baseline_ranks)}
        
        sensitivity_scores = {}
        
        for var in variables:
            temp_state = copy.deepcopy(state)
            
            # Apply perturbation
            if var == "experience":
                temp_state["experience_weight"] = float(state.get("experience_weight", 0.2)) + 0.3
            elif var == "skills":
                temp_state["skill_weight"] = float(state.get("skill_weight", 0.3)) + 0.3
            elif var == "salary":
                temp_state["risk"] = float(state.get("risk", 0.5)) + 0.3 # Proxy for cost/stability risk
            elif var == "joining":
                temp_state["retention"] = float(state.get("retention", 0.5)) + 0.3 # Proxy for immediate timeline
            elif var == "leadership":
                temp_state["leadership"] = float(state.get("leadership", 0.3)) + 0.3
                
            temp_weights = weight_engine.calculate_weights(temp_state)
            perturbed_ranks = ranker.rank_candidates(candidates, temp_state, temp_weights, temp_state)
            
            # Compute total rank movement
            total_shift = 0
            for idx, item in enumerate(perturbed_ranks):
                c_id = item["candidate_id"]
                if c_id in baseline_positions:
                    total_shift += abs(baseline_positions[c_id] - idx)
                    
            sensitivity_scores[var] = total_shift
            
        # Normalize to percentages
        total_shifts = sum(sensitivity_scores.values()) or 1.0
        normalized_sensitivity = {
            k: round((v / total_shifts) * 100.0, 1) for k, v in sensitivity_scores.items()
        }
        
        return normalized_sensitivity
