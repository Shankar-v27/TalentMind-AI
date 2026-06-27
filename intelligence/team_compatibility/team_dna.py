# intelligence/team_compatibility/team_dna.py

from typing import Dict, Any

class TeamDNABuilder:
    def build(self, team_profile: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Build target team parameters for compatibility analysis.
        """
        profile = team_profile or {}
        
        return {
            "team_size": int(profile.get("team_size", 6)),
            "backend": int(profile.get("backend", 3)),
            "frontend": int(profile.get("frontend", 2)),
            "devops": int(profile.get("devops", 1)),
            "avg_experience": int(profile.get("avg_experience", 7)),
            "leadership": float(profile.get("leadership", 0.62)),
            "communication": float(profile.get("communication", 0.85)),
            "collaboration": float(profile.get("collaboration", 0.91)),
            "innovation": float(profile.get("innovation", 0.73)),
            "mentoring": float(profile.get("mentoring", 0.68)),
            "risk_appetite": float(profile.get("risk_appetite", 0.41))
        }
