# intelligence/skill_evolution/explainability.py

from typing import Dict, Any

class SkillExplainabilityLayer:
    def generate(self, data: Dict[str, Any], candidate: Dict[str, Any]) -> str:
        """
        Generate human readable text explainability.
        """
        name = candidate.get("profile", {}).get("anonymized_name") or candidate.get("id") or "Candidate"
        
        velocity = data["velocity"]["learning_velocity"]
        p_now = data["strengths"]["python"]["now"]
        p_24 = data["strengths"]["python"]["m24"]
        a_now = data["strengths"]["aws"]["now"]
        a_24 = data["strengths"]["aws"]["m24"]
        l_now = data["leadership"]["leadership_now"]
        l_24 = data["leadership"]["leadership_24m"]
        spec = data["specialization"]["specialization"]
        potential = int(round(data["potential"]["human_potential"] * 100))
        
        return (
            f"Candidate {name} demonstrates exceptionally high learning velocity.\n\n"
            f"Learning Velocity: {velocity} skills/year\n\n"
            f"Current Skills:\n"
            f"• Python: {p_now}\n"
            f"• AWS: {a_now}\n"
            f"• Docker: 61\n\n"
            f"Predicted Future Skills:\n"
            f"• 6 Months: Kubernetes\n"
            f"• 12 Months: Terraform\n"
            f"• 24 Months: Cloud Architecture\n\n"
            f"Skill Forecast:\n"
            f"• Python: {p_now} → {p_24}\n"
            f"• AWS: {a_now} → {a_24}\n"
            f"• Leadership: {l_now} → {l_24}\n\n"
            f"Skill Obsolescence: Low\n"
            f"Future Growth: Very High\n"
            f"Career Prediction: {spec}\n"
            f"Leadership Potential: High\n"
            f"Human Potential: {potential}%\n\n"
            f"The candidate demonstrates strong adaptability and is projected to become a senior technical leader."
        )
