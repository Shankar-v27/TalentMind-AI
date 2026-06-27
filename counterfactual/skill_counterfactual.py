# counterfactual/skill_counterfactual.py

from typing import Dict, List, Any

class SkillCounterfactual:
    def evaluate(self, gaps: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines what missing skills are needed to achieve the target rank.
        """
        missing = gaps.get("missing_skills", [])
        required_skills = missing if missing else ["Kubernetes", "Terraform"]
        
        # Format list to proper titles
        formatted = [s.title() if len(s) > 3 else s.upper() for s in required_skills]
        score_gain = len(formatted) * 5
        
        return {
            "required_skills": formatted,
            "score_gain": score_gain,
            "future_rank": 1
        }
