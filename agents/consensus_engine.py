# agents/consensus_engine.py

from typing import Dict, Any

class ConsensusEngine:
    def vote(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Synthesize votes from all simulated hiring committee agents.
        """
        score = float(candidate.get("score") or 85.0)
        
        # Simple voting allocation based on score
        if score > 90:
            hire = 10
            reject = 1
            abstain = 1
        elif score > 80:
            hire = 8
            reject = 3
            abstain = 1
        else:
            hire = 6
            reject = 4
            abstain = 2
            
        decision = "HIRE" if hire > reject else "REJECT"
        consensus_score = hire / (hire + reject + abstain)
        
        return {
            "decision": decision,
            "votes": {
                "hire": hire,
                "reject": reject,
                "abstain": abstain
            },
            "consensus_percentage": int(round(consensus_score * 100))
        }
