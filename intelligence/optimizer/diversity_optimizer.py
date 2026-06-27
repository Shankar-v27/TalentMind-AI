# intelligence/optimizer/diversity_optimizer.py

from typing import Dict, List, Any

class DiversityOptimizer:
    def optimize_diversity(
        self,
        candidate: Dict[str, Any],
        current_team: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Recommends hires based on filling balance gaps in skills, experience, and domains.
        """
        # Count team roles
        role_counts = {}
        for member in current_team:
            role = member.get("role", "Backend").lower()
            role_counts[role] = role_counts.get(role, 0) + 1
            
        # Determine current primary concentration
        primary_concentration = max(role_counts, key=role_counts.get) if role_counts else "backend"
        
        # Candidate roles/skills
        cand_role = candidate.get("role", "ML Engineer").lower()
        
        # If candidate fills a sparse role, give diversity bonus
        diversity_score = 70.0
        recommendation_reason = "Adds standard domain expertise."
        
        if cand_role != primary_concentration:
            diversity_score += 25.0
            recommendation_reason = f"Highly recommended: candidate adds '{candidate.get('role', 'ML Engineer')}' domain diversity to a team concentrated in '{primary_concentration.upper()}' roles."
        else:
            diversity_score -= 10.0
            recommendation_reason = f"Concentration alert: candidate matches existing '{primary_concentration.upper()}' team core; may lead to redundancy."
            
        return {
            "candidate_id": candidate.get("candidate_id"),
            "name": candidate.get("name"),
            "diversity_score": min(100.0, max(0.0, diversity_score)) / 100.0,
            "recommendation": recommendation_reason
        }
