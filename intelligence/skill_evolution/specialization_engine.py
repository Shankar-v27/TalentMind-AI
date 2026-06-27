# intelligence/skill_evolution/specialization_engine.py

from typing import Dict, Any

class SpecializationEngine:
    def predict_specialization(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate candidate archetype path for deep specialization.
        """
        skills = [s.lower() for s in candidate.get("skills", [])]
        
        spec = "Platform Architect"
        if any("ml" in s or "ai" in s for s in skills):
            spec = "AI Specialist"
        elif any("security" in s for s in skills):
            spec = "Security Engineer"
            
        return {
            "specialization": spec
        }
