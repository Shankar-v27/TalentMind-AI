# intelligence/career_forecasting/timeline_generator.py

from typing import Dict, List, Any

class CareerTimelineGenerator:
    def generate(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate progression roles milestones for the next 15 years.
        """
        dna = candidate.get("candidate_dna", {})
        leadership = float(dna.get("leadership", 0.60) or 0.60)
        
        timeline = []
        
        # Determine roles based on leadership capacity
        if leadership > 0.75:
            timeline = [
                {"year": 2025, "role": "Senior Engineer"},
                {"year": 2027, "role": "Tech Lead"},
                {"year": 2030, "role": "Engineering Manager"},
                {"year": 2034, "role": "Director"},
                {"year": 2040, "role": "VP Engineering"}
            ]
        else:
            timeline = [
                {"year": 2025, "role": "Senior Engineer"},
                {"year": 2028, "role": "Tech Lead"},
                {"year": 2032, "role": "Architect"},
                {"year": 2036, "role": "Principal Architect"},
                {"year": 2042, "role": "CTO"}
            ]
            
        return {
            "timeline": timeline
        }
