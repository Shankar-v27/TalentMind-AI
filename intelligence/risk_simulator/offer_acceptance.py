# intelligence/risk_simulator/offer_acceptance.py

from typing import Dict, Any

class OfferAcceptancePredictor:
    def predict(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate probability that the candidate will accept the job offer.
        """
        ctx = context or {}
        
        # Extract features
        current_sal = float(ctx.get("current_salary") or 18.0)
        expected_sal = float(ctx.get("expected_salary") or 22.0)
        market_sal = float(ctx.get("market_salary") or 24.0)
        competing_offers = int(ctx.get("competing_offers") or 1)
        remote_pref = str(ctx.get("remote_preference", "remote")).lower()
        job_remote = str(ctx.get("job_remote", "remote")).lower()
        notice_period = int(ctx.get("notice_period") or 30)

        # Base probability calculation
        prob = 0.85
        
        # Salary growth ratio
        if expected_sal > current_sal:
            increase = (expected_sal - current_sal) / current_sal
            prob += min(0.10, increase * 0.2)
        else:
            prob -= 0.10
            
        # Remote match
        if remote_pref == job_remote:
            prob += 0.05
        else:
            prob -= 0.15
            
        # Competing offers penalty
        if competing_offers > 1:
            prob -= (competing_offers - 1) * 0.12
            
        # Notice period penalty
        if notice_period > 60:
            prob -= 0.08
            
        # Final formatting
        prob = max(0.1, min(0.99, prob))
        risk = "LOW"
        if prob < 0.5:
            risk = "HIGH"
        elif prob < 0.75:
            risk = "MEDIUM"
            
        return {
            "accept_probability": round(prob, 2),
            "confidence": round(0.80 + (0.19 * (1 - prob)), 2),
            "risk": risk
        }
