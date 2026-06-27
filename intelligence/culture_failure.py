# intelligence/culture_failure.py

from typing import Dict, Any

class CultureFailurePredictor:
    def calculate(self, candidate_dna: Dict[str, float], organization_match_data: Dict[str, float], team_compatibility_data: Dict[str, Any]) -> Dict[str, Any]:
        mismatch = 1.0 - organization_match_data.get("organization_match", 0.70)
        
        stability = candidate_dna.get("stability", 0.5)
        resignation_risk = round(max(0.01, min(0.99, mismatch * 0.7 + (1.0 - stability) * 0.3)), 2)
        
        c_speed = candidate_dna.get("speed", 0.5)
        c_learning = candidate_dna.get("learning", 0.5)
        burnout_risk = round(max(0.01, min(0.99, c_speed * 0.4 + c_learning * 0.3 + mismatch * 0.3)), 2)
        
        conflict_risk = team_compatibility_data.get("conflict_probability", 0.10)
        culture_mismatch = round(mismatch, 2)
        perf_degradation = round(max(0.01, min(0.99, mismatch * 0.8 + (1.0 - candidate_dna.get("execution", 0.5)) * 0.2)), 2)
        leadership_mismatch = round(1.0 - organization_match_data.get("leadership_match", 0.70), 2)
        
        culture_failure = round(
            0.30 * culture_mismatch +
            0.20 * resignation_risk +
            0.15 * burnout_risk +
            0.15 * conflict_risk +
            0.10 * perf_degradation +
            0.10 * leadership_mismatch,
            2
        )
        
        if culture_failure >= 0.65:
            risk = "HIGH"
        elif culture_failure >= 0.35:
            risk = "MEDIUM"
        else:
            risk = "LOW"
            
        return {
            "culture_failure": culture_failure,
            "risk": risk,
            "resignation_risk": resignation_risk,
            "burnout_risk": burnout_risk,
            "conflict_risk": conflict_risk,
            "culture_mismatch": culture_mismatch,
            "performance_degradation": perf_degradation,
            "leadership_mismatch": leadership_mismatch
        }
