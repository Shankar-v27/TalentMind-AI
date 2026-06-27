# explainability/counterfactual_explain.py

from typing import Dict, Any

class CounterfactualExplainabilityEngine:
    def explain(self, data: Dict[str, Any]) -> str:
        """
        Generates natural language paragraphs explaining the counterfactual path optimization.
        """
        name = data.get("name", "Candidate")
        curr_rank = data.get("current_rank", 2)
        curr_score = data.get("current_score", 89)
        potential_score = data.get("potential_score", 98)
        missing_skills = data.get("missing_skills", ["Kubernetes", "Production deployment"])
        cost = data.get("cost", "₹15,000")
        months = data.get("months", 6)
        prob = int(data.get("success_probability", 0.87) * 100)
        future_role = data.get("future_role", "Senior DevOps Architect")
        
        skills_bullet = "\n".join([f"• {s}" for s in missing_skills])
        
        explanation = (
            f"{name} currently ranks #{curr_rank} with a score of {curr_score}%. "
            f"Counterfactual analysis indicates that the candidate lacks:\n"
            f"{skills_bullet}\n\n"
            f"Simulation results show that obtaining {missing_skills[0] if missing_skills else 'required'} certification "
            f"would increase their score. Adding one production deployment project would increase the score further. "
            f"Completing both improvements would increase the score to {potential_score}%, making the candidate rank #1.\n\n"
            f"Estimated completion time: {months} months.\n"
            f"Estimated cost: {cost}.\n"
            f"Success probability: {prob}%.\n"
            f"Predicted future role: {future_role}."
        )
        
        return explanation
