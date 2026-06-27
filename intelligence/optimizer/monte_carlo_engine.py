# intelligence/optimizer/monte_carlo_engine.py

from typing import Dict, List, Any
import random

class MonteCarloOptimizerEngine:
    def simulate_workforce(
        self,
        candidates: List[Dict[str, Any]],
        runs: int = 10000
    ) -> Dict[str, Any]:
        """
        Runs 10,000 workforce simulation paths.
        Evaluates long-term stability and ROI value probability.
        """
        strategy_wins = {
            "max_quality": 0,
            "future_growth": 0,
            "budget_roi": 0,
            "retention_focused": 0
        }
        
        # Candidate dictionary maps
        cand_by_id = {c.get("candidate_id") or c.get("id"): c for c in candidates}
        
        for _ in range(runs):
            # Introduce stochastic shocks (e.g. market crash, tech shift, team conflict)
            market_tech_shift = random.choice([True, False])
            team_conflict_level = random.uniform(0.1, 0.9)
            attrition_prob_offset = random.uniform(-0.1, 0.2)
            
            # Evaluate fitness of each strategy under this state
            scores = {}
            for strat in strategy_wins:
                scores[strat] = 0.0
                
            for c_id, cand in cand_by_id.items():
                objs = cand.get("objectives", {})
                
                # Max Quality strategy
                q_fit = objs.get("quality", 70.0) - (20.0 if team_conflict_level > 0.7 else 0)
                
                # Future Growth strategy
                fg_fit = objs.get("future", 70.0) + (15.0 if market_tech_shift else 0)
                
                # Budget ROI
                sal = objs.get("salary", 15.0) or 1.0
                roi_fit = (objs.get("quality", 70.0) / max(1.0, sal)) * 10.0
                
                # Retention Focused
                ret = objs.get("retention", 80.0) - attrition_prob_offset * 100.0
                
                # Add to accumulators
                if q_fit > scores["max_quality"]:
                    scores["max_quality"] = q_fit
                if fg_fit > scores["future_growth"]:
                    scores["future_growth"] = fg_fit
                if roi_fit > scores["budget_roi"]:
                    scores["budget_roi"] = roi_fit
                if ret > scores["retention_focused"]:
                    scores["retention_focused"] = ret
                    
            # Best strategy wins this run
            best_strat = max(scores, key=scores.get)
            strategy_wins[best_strat] += 1
            
        # Convert to percentages
        final_wins = {k: round((v / runs) * 100.0, 1) for k, v in strategy_wins.items()}
        best_strategy = max(final_wins, key=final_wins.get)
        
        return {
            "strategy_distribution": final_wins,
            "best_strategy": best_strategy
        }
