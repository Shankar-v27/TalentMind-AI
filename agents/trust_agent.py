# agents/trust_agent.py

from typing import Dict, Any

class TrustAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate candidate credibility and resume risk indicators.
        """
        # Baseline trust index
        trust_index = 0.93
        
        # If there are red flags (e.g. extremely short tenures) we can decrease slightly
        history = candidate.get("career_history", [])
        if len(history) > 4:
            trust_index -= 0.05
            
        return {
            "trust": round(max(0.10, trust_index), 2)
        }
