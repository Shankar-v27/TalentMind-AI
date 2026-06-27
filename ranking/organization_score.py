# ranking/organization_score.py

from typing import Dict, Any

class OrganizationScorer:
    def calculate(
        self,
        skill_match: float,
        organization_match: float,
        leadership: float,
        innovation: float,
        communication: float,
        learning: float,
        retention: float,
        team_compatibility: float
    ) -> Dict[str, float]:
        """
        Calculates the Final Organization Score using the exact weighted formula:
        - Skill Match: 30%
        - Organization DNA Match: 25%
        - Leadership: 10%
        - Innovation: 10%
        - Communication: 10%
        - Learning: 5%
        - Retention: 5%
        - Team Compatibility: 5%
        """
        score = (
            skill_match * 0.30 +
            organization_match * 0.25 +
            leadership * 0.10 +
            innovation * 0.10 +
            communication * 0.10 +
            learning * 0.05 +
            retention * 0.05 +
            team_compatibility * 0.05
        )
        return {
            "organization_score": round(score * 100.0, 1)
        }
