# agents/debate_engine.py

from typing import Dict, List, Any

class DebateEngine:
    def simulate_debate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None, *args, **kwargs) -> List[Dict[str, Any]]:
        """
        Run a simulated multi-round debate between Hire and Reject agents.
        """
        name = candidate.get("profile", {}).get("anonymized_name") or candidate.get("id") or "Candidate"
        
        # Round 1: Initial Opinions
        r1_messages = [
            {"agent": "Hire Agent", "message": f"{name} shows outstanding coding foundations and rapid adaptiveness."},
            {"agent": "Reject Agent", "message": f"Wait, {name} lacks direct exposure to Kubernetes infrastructure setups."}
        ]
        
        # Round 2: Rebuttals
        r2_messages = [
            {"agent": "Hire Agent", "message": "Although Kubernetes is missing, the candidate's learning velocity is in the top 5%. They can easily upskill in 4 weeks."},
            {"agent": "Reject Agent", "message": "We have critical production deadlines next month. We cannot afford 4 weeks of basic upskilling training."}
        ]
        
        # Round 3: Defenses
        r3_messages = [
            {"agent": "Hire Agent", "message": "The candidate has built scalable APIs in FastAPI and Python. This architectural grounding is far harder to hire than basic container configs."},
            {"agent": "Reject Agent", "message": "True, but the lack of infrastructure ownership remains a concern for our lean DevOps team."}
        ]
        
        # Round 4: Compromise & Consensus
        r4_messages = [
            {"agent": "Hire Agent", "message": "What if we offer a conditional hire where they complete a Kubernetes certification during onboarding?"},
            {"agent": "Reject Agent", "message": "A conditional offer with structured upskilling makes sense and offsets the delivery risk."}
        ]
        
        return [
            {"round": 1, "topic": "Initial Opinions", "messages": r1_messages},
            {"round": 2, "topic": "Rebuttals & Critiques", "messages": r2_messages},
            {"round": 3, "topic": "Defensive Arguments", "messages": r3_messages},
            {"round": 4, "topic": "Compromise & Consensus", "messages": r4_messages}
        ]
