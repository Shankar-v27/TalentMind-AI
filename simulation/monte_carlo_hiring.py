# simulation/monte_carlo_hiring.py

import random
from typing import Dict, Any

class MonteCarloHiringSimulator:
    def simulate(self, candidate: Dict[str, Any], runs: int = 10000) -> Dict[str, Any]:
        """
        Run 10,000 simulations tracking post-hiring events (promotions, burnout, resignation, leadership).
        """
        # Get baseline probabilities
        learning = float(candidate.get("candidate_dna", {}).get("learning", 0.75) or 0.75)
        stability = float(candidate.get("candidate_dna", {}).get("stability", 0.70) or 0.70)
        risk = float(candidate.get("candidate_dna", {}).get("risk", 0.40) or 0.40)
        leadership = float(candidate.get("candidate_dna", {}).get("leadership", 0.60) or 0.60)
        
        success_count = 0
        burnout_count = 0
        resignation_count = 0
        leadership_count = 0
        
        for _ in range(runs):
            # Upskilling / Performance success simulation
            v_success = random.uniform(0.1, 1.0)
            if v_success < learning * 0.95:
                success_count += 1
                
            # Stress / Burnout simulation
            v_burnout = random.uniform(0.1, 1.0)
            if v_burnout < risk * 0.50:
                burnout_count += 1
                
            # Retention / Resignation simulation
            v_resign = random.uniform(0.1, 1.0)
            if v_resign > stability * 0.90:
                resignation_count += 1
                
            # Managerial / Leadership simulation
            v_leader = random.uniform(0.1, 1.0)
            if v_leader < leadership * 0.85:
                leadership_count += 1
                
        return {
            "success": int(round((success_count / runs) * 100)),
            "burnout": int(round((burnout_count / runs) * 100)),
            "resignation": int(round((resignation_count / runs) * 100)),
            "leadership": int(round((leadership_count / runs) * 100))
        }
