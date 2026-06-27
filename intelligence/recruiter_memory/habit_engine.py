# intelligence/recruiter_memory/habit_engine.py

from typing import Dict, Any, List

class HabitEngine:
    def compile_recruiter_dna(
        self,
        preferences: Dict[str, float],
        behavior: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive DNA overview including a numerical vector representation.
        """
        risk = behavior.get("risk_tolerance", 0.5)
        innov = behavior.get("innovation_preference", 0.5)
        lead = preferences.get("leadership", 0.5)
        ret = preferences.get("stability", 0.5)
        cost = behavior.get("cost_sensitivity", 0.5)
        
        # DNA Vector representation
        dna_vector = [risk, innov, lead, ret, cost]
        
        return {
            "dna_vector": [round(x, 2) for x in dna_vector],
            "metrics": {
                "risk_taking": "High" if risk > 0.65 else "Low" if risk < 0.35 else "Medium",
                "innovation": "High" if innov > 0.65 else "Low" if innov < 0.35 else "Medium",
                "leadership": "High" if lead > 0.65 else "Low" if lead < 0.35 else "Medium",
                "retention": "High" if ret > 0.65 else "Low" if ret < 0.35 else "Medium",
                "salary_sensitivity": "High" if cost > 0.65 else "Low" if cost < 0.35 else "Medium"
            }
        }
