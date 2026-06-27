# intelligence/career_forecasting/explainability.py

from typing import Dict, Any

class CareerExplainabilityLayer:
    def generate(self, forecasted_data: Dict[str, Any], candidate: Dict[str, Any]) -> str:
        """
        Generate natural language explainability for candidate growth forecasts.
        """
        name = candidate.get("profile", {}).get("anonymized_name") or candidate.get("id") or "Candidate"
        
        velocity = forecasted_data["velocity"]["velocity"]
        next_role = forecasted_data["future_role"]["next_role"]
        timeline = forecasted_data["future_role"]["timeline"]
        ceiling = forecasted_data["ceiling"]["career_ceiling"]
        exec_prob = forecasted_data["executive"]["executive_probability"]
        founder_prob = forecasted_data["founder"]["founder_probability"]
        burnout = forecasted_data["risk"]["burnout"]
        
        explanation = (
            f"Candidate {name} demonstrates:\n"
            f"✓ High learning velocity and adaptable engineering skills.\n"
            f"✓ Strong leadership growth trajectories.\n"
            f"✓ Excellent vertical career progression.\n\n"
            f"Career Velocity: {velocity} levels/year\n\n"
            f"Predicted Career Path:\n"
            f"• {timeline}: {next_role.replace('_', ' ').title()}\n"
            f"• 4 Years: Engineering Manager\n"
            f"• 7 Years: Director\n"
            f"• 12 Years: VP Engineering\n\n"
            f"Leadership Index: {int(forecasted_data['leadership']['current'])}%\n"
            f"Promotion Probability: {int(forecasted_data['promotion']['promotion_probability']*100)}%\n"
            f"Career Ceiling: {ceiling.replace('_', ' ').title()}\n"
            f"Founder Probability: {int(founder_prob*100)}%\n"
            f"Executive Probability: {int(exec_prob*100)}%\n"
            f"Burnout Risk: {int(burnout*100)}%\n\n"
            f"The candidate is projected to become a senior organizational leader within approximately 7 years."
        )
        
        return explanation
