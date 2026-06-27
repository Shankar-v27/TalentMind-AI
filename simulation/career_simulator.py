# simulation/career_simulator.py

from typing import Dict, List, Any

class CareerSimulator:
    def simulate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate a progressive career timeline based on the candidate profile and learning velocity.
        """
        score = float(candidate.get("score") or 85.0)
        start_year = 2025
        
        path = []
        
        if score > 90:
            path = [
                {"year": start_year, "role": "Lead Systems Engineer"},
                {"year": start_year + 2, "role": "Staff Architect"},
                {"year": start_year + 4, "role": "Director of Engineering"},
                {"year": start_year + 7, "role": "VP of Technology"},
                {"year": start_year + 11, "role": "Chief Technology Officer (CTO)"}
            ]
        elif score > 80:
            path = [
                {"year": start_year, "role": "Senior Software Engineer"},
                {"year": start_year + 2, "role": "Technical Lead"},
                {"year": start_year + 4, "role": "Engineering Manager"},
                {"year": start_year + 7, "role": "Director of Engineering"},
                {"year": start_year + 11, "role": "VP of Engineering"}
            ]
        else:
            path = [
                {"year": start_year, "role": "Software Engineer II"},
                {"year": start_year + 3, "role": "Senior Software Developer"},
                {"year": start_year + 5, "role": "Technical Lead"},
                {"year": start_year + 8, "role": "Engineering Manager"},
                {"year": start_year + 12, "role": "Director of Technology"}
            ]
            
        return {
            "career_path": path
        }
