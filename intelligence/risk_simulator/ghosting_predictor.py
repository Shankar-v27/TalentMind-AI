# intelligence/risk_simulator/ghosting_predictor.py

from typing import Dict, Any

class GhostingPredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will ghost the interview or communications.
        """
        ctx = context or {}
        
        # Extract features
        response_time_hours = float(ctx.get("response_time_hours") or 4.0)
        email_interactions = int(ctx.get("email_interactions") or 5)
        competing_offers = int(ctx.get("competing_offers") or 1)
        attendance_history = float(ctx.get("attendance_history") or 1.0) # 0 to 1 rate
        
        prob = 0.15
        
        # Long response times indicate lower engagement
        if response_time_hours > 24:
            prob += 0.20
        elif response_time_hours > 12:
            prob += 0.10
            
        # Low communication count increases ghosting risk
        if email_interactions < 3:
            prob += 0.15
            
        # High volume of competing offers
        if competing_offers > 2:
            prob += 0.18
            
        # Poor attendance history
        if attendance_history < 0.9:
            prob += (1.0 - attendance_history) * 0.5
            
        prob = max(0.01, min(0.99, prob))
        risk = "LOW"
        if prob > 0.5:
            risk = "HIGH"
        elif prob > 0.25:
            risk = "MEDIUM"
            
        return {
            "ghost_probability": round(prob, 2),
            "risk": risk
        }
