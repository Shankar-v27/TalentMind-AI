# intelligence/career_forecasting/plateau_detector.py

from typing import Dict, Any

class CareerPlateauDetector:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate if a candidate shows signs of stagnating in current level brackets.
        """
        dna = candidate.get("candidate_dna", {})
        learning = float(dna.get("learning", 0.75) or 0.75)
        stability = float(dna.get("stability", 0.75) or 0.75)
        
        # Stagnation is high if stability is high but learning velocity is very low
        plateau_risk = (1.0 - learning) * 0.7 + stability * 0.3
        plateau = plateau_risk > 0.60
        
        return {
            "plateau": plateau,
            "risk": round(min(0.99, plateau_risk), 2)
        }
