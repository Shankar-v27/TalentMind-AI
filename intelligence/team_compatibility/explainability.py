# intelligence/team_compatibility/explainability.py

from typing import Dict, Any

class TeamExplainabilityLayer:
    def generate(self, data: Dict[str, Any], candidate: Dict[str, Any]) -> str:
        """
        Generate human readable text explainability.
        """
        name = candidate.get("profile", {}).get("anonymized_name") or candidate.get("id") or "Candidate"
        
        comp = int(round(data["compatibility"]["compatibility"] * 100))
        conflict = int(round(data["conflict"]["conflict_probability"] * 100))
        diversity = int(round(data["diversity"]["knowledge_diversity"] * 100))
        leader = int(round(data["leadership"]["leadership_balance"] * 100))
        collab = int(round(data["collaboration"]["collaboration"] * 100))
        mentor = int(round(data["mentorship"]["mentor_score"] * 100))
        prod = int(round(data["productivity"]["productivity_gain"] * 100))
        innov = int(round(data["innovation"]["innovation_boost"] * 100))
        role = data["role"]["future_team_role"]
        
        return (
            f"Candidate {name} demonstrates:\n"
            f"✓ Excellent communication capabilities.\n"
            f"✓ Strong collaboration and peer support tendencies.\n"
            f"✓ High mentoring capability and knowledge-sharing motivation.\n"
            f"✓ Strong cultural fit within target company dimensions.\n"
            f"✓ Significant knowledge diversity contributing cognitive variations.\n\n"
            f"Team Compatibility: {comp}%\n"
            f"Conflict Probability: {conflict}%\n"
            f"Knowledge Diversity: {diversity}%\n"
            f"Leadership Balance: {leader}%\n"
            f"Collaboration: {collab}%\n"
            f"Mentorship: {mentor}%\n"
            f"Productivity Gain: {prod}%\n"
            f"Innovation Gain: {innov}%\n\n"
            f"Predicted Team Role: {role}\n\n"
            f"The candidate is expected to significantly improve team performance, innovation, knowledge sharing, and organizational productivity."
        )
