# intelligence/risk_simulator/joining_predictor.py

from typing import Dict, Any

class JoiningPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will actually join on the start date.
        """
        ctx = context or {}
        
        # Extract features
        has_accepted = bool(ctx.get("offer_accepted", True))
        has_counter_offer = bool(ctx.get("counter_offers", False))
        notice_period = int(ctx.get("notice_period") or 30)
        relocation_required = bool(ctx.get("relocation_required", False))
        
        prob = 0.90
        
        if not has_accepted:
            prob -= 0.60
            
        if has_counter_offer:
            prob -= 0.25
            
        if notice_period > 60:
            prob -= 0.10
            
        if relocation_required:
            prob -= 0.12
            
        prob = max(0.01, min(0.99, prob))
        return {
            "joining_probability": round(prob, 2)
        }
