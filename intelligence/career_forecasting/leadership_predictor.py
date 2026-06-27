# intelligence/career_forecasting/leadership_predictor.py

from typing import Dict, Any

class LeadershipPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Model future leadership index metrics over 10 years.
        """
        dna = candidate.get("candidate_dna", {})
        base_leader = float(dna.get("leadership", 0.60) or 0.60) * 100.0
        
        return {
            "current": int(round(base_leader)),
            "year_2": int(round(min(99.0, base_leader + 10.0))),
            "year_5": int(round(min(99.0, base_leader + 22.0))),
            "year_10": int(round(min(99.0, base_leader + 31.0)))
        }
