# intelligence/skill_evolution/dependency_graph.py

from typing import Dict, Any

class SkillDependencyEngine:
    def predict_next_skill(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate dependencies to suggest the next logical skill to learn.
        """
        skills = [s.lower() for s in candidate.get("skills", [])]
        
        next_skill = "kubernetes"
        if "kubernetes" in skills:
            next_skill = "terraform"
        if "terraform" in skills:
            next_skill = "platform_architecture"
            
        return {
            "next_skill": next_skill
        }
