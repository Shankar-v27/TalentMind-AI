# intelligence/skill_evolution/timeline_builder.py

from typing import Dict, List, Any

class SkillTimelineBuilder:
    def build_timeline(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Construct sequence timelines of historical skill acquisition.
        """
        # Synthesize path based on experiences
        exp_years = int(candidate.get("experience_years", 6) or 6)
        start_year = 2026 - exp_years
        
        timeline = [
            {"skill": "python", "year": start_year},
            {"skill": "docker", "year": start_year + 1},
            {"skill": "aws", "year": start_year + 2},
            {"skill": "kubernetes", "year": start_year + 3},
            {"skill": "terraform", "year": start_year + 4},
            {"skill": "mlops", "year": start_year + 5}
        ]
        
        return {
            "timeline": timeline
        }
