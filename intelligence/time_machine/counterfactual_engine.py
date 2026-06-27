# intelligence/time_machine/counterfactual_engine.py

from typing import Dict, List, Any

class CounterfactualEngine:
    def explain_how_to_win(
        self,
        candidate_id: str,
        candidates: List[Dict[str, Any]],
        state: Dict[str, Any],
        ranker: Any,
        weight_engine: Any
    ) -> Dict[str, Any]:
        """
        Calculates actionable improvements (counterfactual additions) that would promote 
        the candidate to Rank 1 under the current state.
        """
        # Find candidate and best score
        target_cand = None
        for c in candidates:
            if (c.get("candidate_id") or c.get("id")) == candidate_id:
                target_cand = c
                break
                
        if not target_cand:
            return {"candidate_id": candidate_id, "rank1_conditions": ["Candidate not found"]}
            
        weights = weight_engine.calculate_weights(state)
        current_ranks = ranker.rank_candidates(candidates, state, weights, state)
        
        best_score = current_ranks[0]["score"] if current_ranks else 100.0
        
        # Check current candidate score
        cand_rank_info = next((item for item in current_ranks if item["candidate_id"] == candidate_id), None)
        if not cand_rank_info:
            return {"candidate_id": candidate_id, "rank1_conditions": ["Ineligible in current configuration"]}
            
        cand_score = cand_rank_info["score"]
        if cand_score >= best_score:
            return {
                "candidate_id": candidate_id,
                "current_score": cand_score,
                "rank1_conditions": ["Already Rank 1 in this universe"]
            }
            
        score_gap = best_score - cand_score
        conditions = []
        
        # Scenario A: Experience addition
        req_exp = float(state.get("experience", 5))
        cand_exp = float(target_cand.get("experience", 0.0) or 0.0)
        if cand_exp < req_exp:
            diff = req_exp - cand_exp
            conditions.append(f"Acquire {diff:.1f} more years of experience (to satisfy mandatory minimum)")
        else:
            needed_exp_gain = score_gap / max(1.0, weights.get("experience", 0.2) * 8.0)
            conditions.append(f"Add {needed_exp_gain:.1f} years of relevant experience")
            
        # Scenario B: Skills addition
        req_skills = [s.lower() for s in state.get("skills", [])]
        cand_skills = [s.get("name", "").lower() for s in target_cand.get("skills", []) if s.get("name")]
        missing = [s for s in req_skills if s not in cand_skills]
        if missing:
            conditions.append(f"Obtain core skills: {', '.join(missing).upper()}")
        else:
            # Recommend preferred high-gain certifications
            conditions.append("Acquire AWS or Kubernetes Certified Administrator (CKA) certification")
            
        # Scenario C: Leadership upskilling
        if target_cand.get("leadership_score", 70) < 85:
            conditions.append("Complete Leadership Management Academy / Mentor training")
            
        return {
            "candidate_id": candidate_id,
            "candidate_name": target_cand.get("name", "Candidate"),
            "current_score": cand_score,
            "best_score_to_beat": best_score,
            "score_gap": round(score_gap, 2),
            "rank1_conditions": conditions
        }
