# intelligence/team_compatibility/candidate_dna.py

from typing import Dict, Any

class CandidateDNABuilder:
    def build(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build complete behavioral and capability DNA parameters.
        """
        # Resolve metrics or default to standard base rates
        dna = candidate.get("candidate_dna", {})
        
        return {
            "leadership": float(dna.get("leadership", 0.60) or 0.60),
            "communication": float(dna.get("communication", 0.70) or 0.70),
            "collaboration": float(dna.get("collaboration", 0.80) or 0.80),
            "mentoring": float(dna.get("mentoring", 0.65) or 0.65),
            "innovation": float(dna.get("innovation", 0.60) or 0.60),
            "ownership": float(dna.get("ownership", 0.70) or 0.70),
            "risk_appetite": float(dna.get("risk", 0.40) or 0.40),
            "learning_speed": float(dna.get("learning", 0.75) or 0.75),
            "emotional_intelligence": float(dna.get("eq", 0.68) or 0.68),
            "conflict_tolerance": float(dna.get("conflict_handling", 0.70) or 0.70),
            "adaptability": float(dna.get("adaptability", 0.75) or 0.75),
            "reliability": float(dna.get("reliability", 0.80) or 0.80),
            "creativity": float(dna.get("creativity", 0.65) or 0.65),
            "decision_making": float(dna.get("decision_making", 0.70) or 0.70),
            "problem_solving": float(dna.get("problem_solving", 0.75) or 0.75),
            "stress_handling": float(dna.get("stress_handling", 0.70) or 0.70),
            "team_orientation": float(dna.get("team_orientation", 0.80) or 0.80)
        }
