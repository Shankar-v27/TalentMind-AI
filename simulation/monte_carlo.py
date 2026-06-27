# simulation/monte_carlo.py

import random
from typing import Dict, List, Any

class MonteCarloSimulator:
    def simulate(self, current_score: float, scenarios: List[Dict[str, Any]], runs: int = 10000) -> Dict[str, Any]:
        """
        Simulate 10,000+ improvement runs using randomized learning velocities, effort coefficients, and success weights.
        """
        scores = []
        if not scenarios:
            return {
                "best_score": current_score,
                "average_score": current_score,
                "probability": 1.0
            }
            
        max_gain = max(s["total_gain"] for s in scenarios) if scenarios else 0
        
        for _ in range(runs):
            # Randomize success completion probability for the path
            learning_velocity = random.uniform(0.6, 1.0)
            completion_ratio = random.uniform(0.5, 1.0)
            # Calculate simulated score
            gain = max_gain * completion_ratio * learning_velocity
            sim_score = min(100.0, current_score + gain)
            scores.append(sim_score)
            
        best_score = max(scores)
        avg_score = sum(scores) / len(scores)
        
        # Probability of achieving at least the average projected score
        success_threshold = current_score + (max_gain * 0.5)
        successful_runs = sum(1 for s in scores if s >= success_threshold)
        probability = successful_runs / runs
        
        return {
            "best_score": round(best_score, 1),
            "average_score": round(avg_score, 1),
            "probability": round(probability, 2)
        }
