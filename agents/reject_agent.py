# agents/reject_agent.py

from typing import Dict, Any

class RejectAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate why we should reject the candidate, highlighting critical gaps.
        """
        score = float(candidate.get("score") or 85.0)
        dna = candidate.get("candidate_dna", {})
        skills = [s.get("name", "").lower() for s in candidate.get("skills", [])]
        
        arguments = []
        
        # Identify missing typical DevOps/Infrastructure skills
        target_skills = ["kubernetes", "docker", "terraform", "aws"]
        missing = [ts for ts in target_skills if ts not in skills]
        for item in missing:
            arguments.append(f"Missing critical skill: {item}")
            
        # Experience tenure analysis
        history = candidate.get("career_history", [])
        if len(history) > 3:
            arguments.append("Potential job-hopping tendencies (frequent transitions)")
            
        stability = float(dna.get("stability", 0.8) or 0.8)
        if stability < 0.70:
            arguments.append("Low tenure stability indicators in career history")
            
        # Confidence calculation
        confidence = max(0.4, min(0.95, (100.0 - score) / 100.0 + 0.3))
        
        return {
            "decision": "REJECT",
            "confidence": round(confidence, 2),
            "arguments": arguments if arguments else ["Candidate experience gaps in scaling systems"]
        }
