# intelligence/digital_twin/candidate_dna.py

from typing import Dict, Any

class CandidateDnaEngine:
    def extract_dna(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract multi-dimensional digital twin DNA scores.
        """
        score = float(candidate.get("score", 85))
        
        return {
            "leadership": round((score / 100.0) * 0.42 + 0.10, 2),
            "communication": round((score / 100.0) * 0.91 + 0.05, 2),
            "learning": round((score / 100.0) * 0.94 + 0.05, 2),
            "innovation": round((score / 100.0) * 0.82 + 0.10, 2),
            "adaptability": round((score / 100.0) * 0.89 + 0.05, 2),
            "mentorship": round((score / 100.0) * 0.88 + 0.08, 2),
            "ownership": round((score / 100.0) * 0.85 + 0.10, 2),
            "stress_handling": round((score / 100.0) * 0.80 + 0.15, 2)
        }
