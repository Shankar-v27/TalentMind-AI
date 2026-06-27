# intelligence/skill_evolution/career_evolution.py

from typing import List, Dict, Any

class CareerEvolutionEngine:
    def predict_evolution(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate career progression ladder milestones.
        """
        experience = int(candidate.get("experience_years", 6) or 6)
        
        path = ["Junior Engineer", "Engineer"]
        
        if experience >= 8:
            path.extend(["Senior Engineer", "Tech Lead", "Engineering Manager", "Director"])
        elif experience >= 5:
            path.extend(["Senior Engineer", "Tech Lead", "Engineering Manager"])
        else:
            path.extend(["Senior Engineer", "Tech Lead"])
            
        return {
            "career_path": path[2:] # return predicted future nodes
        }
