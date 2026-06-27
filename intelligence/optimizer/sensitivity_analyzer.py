# intelligence/optimizer/sensitivity_analyzer.py

from typing import Dict, List, Any
import numpy as np

class SensitivityAnalyzer:
    def analyze_sensitivity(
        self,
        candidates: List[Dict[str, Any]],
        objectives: List[str]
    ) -> Dict[str, float]:
        """
        Calculates which objective variance dominates the rankings.
        """
        if not candidates or not objectives:
            return {}
            
        variances = {}
        for obj in objectives:
            vals = [cand.get("objectives", {}).get(obj, 50.0) for cand in candidates]
            # normalize values to standard deviation percentage contribution
            if len(vals) > 1:
                std_dev = float(np.std(vals))
                variances[obj] = std_dev
            else:
                variances[obj] = 0.0
                
        total_std = sum(variances.values()) or 1.0
        contributions = {k: round((v / total_std) * 100.0, 1) for k, v in variances.items()}
        
        # Ensure we return at least a default schema mapping if total_std is 0
        if sum(contributions.values()) == 0:
            contributions = {"quality": 38.0, "future": 22.0, "salary": 18.0, "retention": 12.0, "leadership": 10.0}
            
        return contributions
