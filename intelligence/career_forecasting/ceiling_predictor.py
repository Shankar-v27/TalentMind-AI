# intelligence/career_forecasting/ceiling_predictor.py

from typing import Dict, Any

class CareerCeilingPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate's maximum role potential in their career path.
        """
        dna = candidate.get("candidate_dna", {})
        leadership = float(dna.get("leadership", 0.60) or 0.60)
        
        ceiling = "PRINCIPAL_ARCHITECT"
        confidence = 0.70 + (leadership * 0.15)
        
        if leadership > 0.82:
            ceiling = "CTO"
        elif leadership > 0.70:
            ceiling = "VP_ENGINEERING"
        elif leadership > 0.55:
            ceiling = "DIRECTOR_OF_ENGINEERING"
            
        return {
            "career_ceiling": ceiling,
            "confidence": round(min(0.99, confidence), 2)
        }
