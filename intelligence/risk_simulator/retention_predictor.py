# intelligence/risk_simulator/retention_predictor.py

from typing import Dict, Any

class RetentionPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Predict retention probability over multiple milestones.
        """
        # Base stability from candidate DNA or profile
        stability = float(candidate.get("candidate_dna", {}).get("stability", 0.8) or 0.8)
        
        # Adjust based on past tenure stability
        history = candidate.get("career_history", [])
        avg_tenure_years = 2.5
        if history:
            # simple mock calculations
            avg_tenure_years = max(1.0, min(5.0, len(history) * 1.2))
            
        decay_factor = 1.0 - (0.15 / max(1.0, avg_tenure_years))
        
        p3 = min(0.99, stability * 1.1)
        p6 = min(0.99, p3 * decay_factor)
        p12 = min(0.99, p6 * decay_factor)
        p24 = min(0.99, p12 * decay_factor)
        p36 = min(0.99, p24 * decay_factor)
        p60 = min(0.99, p36 * decay_factor)
        
        return {
            "3_months": round(p3, 2),
            "6_months": round(p6, 2),
            "12_months": round(p12, 2),
            "24_months": round(p24, 2),
            "36_months": round(p36, 2),
            "60_months": round(p60, 2)
        }
