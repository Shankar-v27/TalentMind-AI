# agents/judge_agent.py

from typing import Dict, Any

class JudgeAgent:
    def evaluate(self, debate_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produce final judgment by reviewing arguments from all sides.
        """
        consensus = debate_summary.get("consensus", {})
        decision = consensus.get("decision", "HIRE")
        confidence = float(consensus.get("consensus_percentage", 80)) / 100.0
        
        reason = "Technical capability, learning speed and leadership attributes outweigh delivery risks."
        if decision == "REJECT":
            reason = "Critical infrastructure gaps and career transitions raise delivery risks beyond acceptable levels."
            
        return {
            "decision": decision,
            "confidence": round(confidence, 2),
            "reason": reason
        }
