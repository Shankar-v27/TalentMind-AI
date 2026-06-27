# intelligence/skill_evolution/skill_extractor.py

from typing import Dict, Any

class SkillExtractor:
    def extract_skills(self, candidate: Dict[str, Any]) -> Dict[str, int]:
        """
        Extract primary technical and leadership competency scores.
        """
        # Read from candidate fields or default
        skills = candidate.get("skills", [])
        score = candidate.get("score", 85)
        
        extracted = {
            "python": int(score * 0.85),
            "aws": int(score * 0.50),
            "docker": int(score * 0.70),
            "leadership": int(score * 0.38)
        }
        
        # Override if specific skills exist
        for s in skills:
            name = s.lower()
            if "python" in name:
                extracted["python"] = 90
            if "aws" in name or "cloud" in name:
                extracted["aws"] = 75
            if "docker" in name or "kubernetes" in name:
                extracted["docker"] = 80
                
        return extracted
