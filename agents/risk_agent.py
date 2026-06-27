# agents/risk_agent.py

from typing import Dict, Any

class RiskAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate risks including burnout, resignation, and conflict.
        """
        dna = candidate.get("candidate_dna", {})
        risk = float(dna.get("risk", 0.40) or 0.40)
        stability = float(dna.get("stability", 0.75) or 0.75)
        
        arguments = []
        if risk > 0.5:
            arguments.append("Elevated risk profile with potentially higher workload stress vulnerability")
        if stability < 0.70:
            arguments.append("Potential retention risk indicated by low tenure stability")
            
        calculated_risk = max(0.05, min(0.95, risk * 0.6 + (1.0 - stability) * 0.4))
        
        return {
            "risk": round(calculated_risk, 2),
            "arguments": arguments
        }
