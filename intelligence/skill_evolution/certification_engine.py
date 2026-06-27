# intelligence/skill_evolution/certification_engine.py

from typing import Dict, Any

class CertificationEngine:
    def predict_path(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict certification-backed transition tracks.
        """
        skills = [s.lower() for s in candidate.get("skills", [])]
        
        path = "Cloud Architect"
        if any("ml" in s or "ai" in s for s in skills):
            path = "AI Engineer"
        elif any("security" in s for s in skills):
            path = "Security Architect"
        elif any("platform" in s or "devops" in s for s in skills):
            path = "Platform Architect"
            
        return {
            "future_path": path
        }
