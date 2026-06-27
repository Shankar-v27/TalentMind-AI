# intelligence/perturbation_engine.py

from typing import Dict, List, Any
import itertools

class PerturbationEngine:
    def generate_scenarios(self, gaps: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate scenarios of combinations of improvements to test.
        """
        possible_improvements = []
        
        # Skill improvements
        for skill in gaps.get("missing_skills", []):
            possible_improvements.append({
                "type": "skill",
                "name": skill,
                "score_gain": 5 if skill in ["kubernetes", "docker", "fastapi"] else 3
            })
            
        # Certifications
        for cert in gaps.get("missing_certifications", []):
            possible_improvements.append({
                "type": "certification",
                "name": cert,
                "score_gain": 4
            })
            
        # Projects
        for proj in gaps.get("missing_projects", []):
            possible_improvements.append({
                "type": "project",
                "name": proj,
                "score_gain": 6
            })
            
        # Leadership
        if gaps.get("missing_leadership"):
            possible_improvements.append({
                "type": "leadership",
                "name": "Lead mentorship and project execution",
                "score_gain": 7
            })

        # Generate combinations (limit to max combinations to avoid explosion)
        scenarios = []
        # Add baseline (empty improvements scenario)
        scenarios.append({
            "improvements": [],
            "total_gain": 0
        })
        
        # Max of 4 base elements to avoid exponential growth (16 combinations max)
        base_elements = possible_improvements[:4]
        
        for r in range(1, len(base_elements) + 1):
            for combo in itertools.combinations(base_elements, r):
                scenarios.append({
                    "improvements": list(combo),
                    "total_gain": sum(x["score_gain"] for x in combo)
                })
                
        return scenarios
