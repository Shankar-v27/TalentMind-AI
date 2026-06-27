# intelligence/time_machine/realtime_ranker.py

from typing import Dict, List, Any
import numpy as np

class RealtimeRanker:
    def rank_candidates(
        self,
        candidates: List[Dict[str, Any]],
        state: Dict[str, Any],
        weights: Dict[str, float],
        constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Ranks all candidates dynamically using the recalculated weights and constraints.
        Returns a sorted list of ranked candidates with breakdown scores.
        """
        ranked_list = []
        
        # Read parameters from state
        required_skills = [s.lower() for s in state.get("skills", [])]
        min_exp = float(state.get("experience", 0))
        max_salary = float(state.get("salary", 999999))
        max_joining = float(state.get("joining", 180))
        
        for cand in candidates:
            # Check constraints
            cand_exp = float(cand.get("experience", 0.0) or 0.0)
            
            # Notice period & Salary
            cand_signals = cand.get("redrob_signals", {})
            cand_salary = float(cand.get("salary", cand_signals.get("salary_requirement", 12.0) or 12.0))
            cand_notice = float(cand.get("notice_period", cand_signals.get("notice_period_days", 30) or 30))
            
            # Constraint flags
            eligible = (cand_exp >= min_exp) and (cand_salary <= max_salary) and (cand_notice <= max_joining)
            
            # 1. Skill Score
            cand_skills = [s.get("name", "").lower() for s in cand.get("skills", []) if s.get("name")]
            skill_match_count = sum(1 for s in required_skills if s in cand_skills)
            skill_score = (skill_match_count / max(1, len(required_skills))) * 100.0
            
            # 2. Experience Score
            if cand_exp >= min_exp:
                exp_score = min(100.0, 60.0 + (cand_exp - min_exp) * 8.0)
            else:
                exp_score = max(0.0, (cand_exp / max(1.0, min_exp)) * 60.0)
                
            # 3. Leadership Score
            leadership_score = float(cand.get("leadership_score", cand.get("score", 70) * 0.95))
            
            # 4. Behavior Score
            behavior_score = float(cand.get("behavior_score", 75.0))
            
            # 5. Retention Score
            retention_prob = float(cand.get("retention_probability", 0.85))
            retention_score = retention_prob * 100.0
            
            # 6. Risk Score
            # Lower risk = higher risk score contribution
            burnout_prob = float(cand.get("burnout_probability", 0.15))
            resignation_prob = float(cand.get("resignation_probability", 0.12))
            risk_score = (1.0 - (burnout_prob + resignation_prob) / 2.0) * 100.0
            
            # 7. Future Score
            future_score = float(cand.get("future_score", cand.get("score", 72) * 1.05))
            
            # 8. Team Score
            team_score = float(cand.get("team_compatibility", 78.0))
            
            # Weighted average
            weighted_score = (
                weights.get("skill", 0.3) * skill_score +
                weights.get("experience", 0.2) * exp_score +
                weights.get("leadership", 0.1) * leadership_score +
                weights.get("future", 0.1) * future_score +
                weights.get("retention", 0.1) * retention_score +
                weights.get("risk", 0.2) * risk_score
            )
            
            # Penalty for ineligible candidates
            if not eligible:
                weighted_score *= 0.5
                
            final_score = round(max(0.0, min(100.0, weighted_score)), 2)
            
            ranked_list.append({
                "candidate_id": cand.get("candidate_id") or cand.get("id"),
                "name": cand.get("name", "Candidate"),
                "score": final_score,
                "eligible": eligible,
                "breakdown": {
                    "skill": round(skill_score, 1),
                    "experience": round(exp_score, 1),
                    "leadership": round(leadership_score, 1),
                    "behavior": round(behavior_score, 1),
                    "retention": round(retention_score, 1),
                    "risk": round(risk_score, 1),
                    "future": round(future_score, 1),
                    "team": round(team_score, 1)
                }
            })
            
        # Sort by score descending
        ranked_list.sort(key=lambda x: x["score"], reverse=True)
        return ranked_list
