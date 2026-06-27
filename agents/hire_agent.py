# agents/hire_agent.py

from typing import Dict, Any

class HireAgent:
    def evaluate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate why we should hire the candidate based on profile and scores.
        """
        score = float(candidate.get("score") or 85.0)
        dna = candidate.get("candidate_dna", {})
        skills = [s.get("name", "").lower() for s in candidate.get("skills", [])]
        
        arguments = []
        if score > 80:
            arguments.append(f"Strong overall score of {score}% in candidate matches")
        
        # Skill strengths
        if "python" in skills or any("py" in s for s in skills):
            arguments.append("Strong python programming foundations")
        if "react" in skills or "javascript" in skills:
            arguments.append("Solid modern frontend capability")
            
        # DNA attributes
        learning = float(dna.get("learning", 0.75) or 0.75)
        if learning > 0.70:
            arguments.append("Fast learner with high adaptability indicators")
            
        leadership = float(dna.get("leadership", 0.60) or 0.60)
        if leadership > 0.70:
            arguments.append("Demonstrates clear long-term leadership potential")
            
        innovation = float(dna.get("innovation", 0.60) or 0.60)
        if innovation > 0.70:
            arguments.append("Vibrant innovation orientation and project creativity")

        confidence = max(0.5, min(0.99, score / 100.0))
        
        return {
            "decision": "HIRE",
            "confidence": round(confidence, 2),
            "arguments": arguments if arguments else ["Good general technical foundation"]
        }
