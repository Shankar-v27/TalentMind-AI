# intelligence/optimizer/objective_engine.py

from typing import Dict, Any

class ObjectiveEngine:
    def calculate_objectives(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """
        Extracts and calculates 16 objective scores for a candidate.
        Scores are normalized to [0, 100] (or actual value e.g. LPA / notice period days).
        """
        score = float(candidate.get("score", 75.0) or 75.0)
        signals = candidate.get("redrob_signals", {})
        
        # 1. Quality
        quality = float(candidate.get("quality_score", score * 1.05))
        
        # 2. Future Potential
        future = float(candidate.get("future_score", score * 1.10))
        
        # 3. Leadership
        leadership = float(candidate.get("leadership_score", score * 0.95))
        
        # 4. Innovation
        innovation = float(candidate.get("innovation_score", score * 0.98))
        
        # 5. Retention
        retention = float(candidate.get("retention_probability", 0.85)) * 100.0
        
        # 6. Learning Speed
        learning = float(candidate.get("learning_velocity", 0.75)) * 100.0
        
        # 7. Culture Fit
        culture = float(candidate.get("culture_fit", 78.0))
        
        # 8. Team Compatibility
        team_comp = float(candidate.get("team_compatibility", 76.0))
        
        # 9. Salary (LPA or thousands) - lower is better for optimization
        salary = float(candidate.get("salary", signals.get("salary_requirement", 18.0) or 18.0))
        
        # 10. Joining Time (notice period in days) - lower is better
        joining = float(candidate.get("notice_period", signals.get("notice_period_days", 30) or 30))
        
        # 11. Attrition Risk - lower is better
        attrition = float(candidate.get("attrition_risk", 100.0 - retention))
        
        # 12. Burnout Risk - lower is better
        burnout = float(candidate.get("burnout_probability", 0.15)) * 100.0
        
        # 13. Promotion Probability
        promotion = float(candidate.get("promotion_probability", 0.65)) * 100.0
        
        # 14. Business Value
        business_val = float(candidate.get("business_value", score * 1.02))
        
        # 15. Human Potential
        human_potential = float(candidate.get("human_potential", score * 1.08))
        
        # 16. Knowledge Diversity
        knowledge_div = float(candidate.get("knowledge_diversity", 72.0))
        
        return {
            "quality": round(min(100.0, max(0.0, quality)), 1),
            "future": round(min(100.0, max(0.0, future)), 1),
            "leadership": round(min(100.0, max(0.0, leadership)), 1),
            "innovation": round(min(100.0, max(0.0, innovation)), 1),
            "retention": round(min(100.0, max(0.0, retention)), 1),
            "learning": round(min(100.0, max(0.0, learning)), 1),
            "culture": round(min(100.0, max(0.0, culture)), 1),
            "team": round(min(100.0, max(0.0, team_comp)), 1),
            "salary": round(salary, 2),
            "joining": round(joining, 1),
            "attrition": round(min(100.0, max(0.0, attrition)), 1),
            "burnout": round(min(100.0, max(0.0, burnout)), 1),
            "promotion": round(min(100.0, max(0.0, promotion)), 1),
            "business_value": round(min(100.0, max(0.0, business_val)), 1),
            "human_potential": round(min(100.0, max(0.0, human_potential)), 1),
            "knowledge_diversity": round(min(100.0, max(0.0, knowledge_div)), 1)
        }
