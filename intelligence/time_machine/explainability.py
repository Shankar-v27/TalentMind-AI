# intelligence/time_machine/explainability.py

from typing import Dict, List, Any

class TimeMachineExplainabilityEngine:
    def explain_shift(
        self,
        candidate_name: str,
        old_rank: int,
        new_rank: int,
        old_state: Dict[str, Any],
        new_state: Dict[str, Any],
        score_diff: float
    ) -> str:
        """
        Generates narrative detailing why a candidate shifted positions.
        """
        direction = "up" if old_rank > new_rank else "down"
        delta = abs(old_rank - new_rank)
        
        if delta == 0:
            return f"Candidate {candidate_name} maintained their position at Rank {new_rank} with stable score indicators."
            
        reasons = []
        
        # Check experience changes
        old_exp = old_state.get("experience", 5)
        new_exp = new_state.get("experience", 5)
        if old_exp != new_exp:
            reasons.append(f"required experience threshold changed from {old_exp} to {new_exp} years")
            
        # Check notice period changes
        old_notice = old_state.get("joining", 60)
        new_notice = new_state.get("joining", 60)
        if old_notice != new_notice:
            reasons.append(f"notice period ceiling updated from {old_notice}d to {new_notice}d")
            
        # Check skill modifications
        old_skills = set(old_state.get("skills", []))
        new_skills = set(new_state.get("skills", []))
        added_skills = new_skills - old_skills
        removed_skills = old_skills - new_skills
        
        if added_skills:
            reasons.append(f"mandatory skill requirement added: {', '.join(added_skills).upper()}")
        if removed_skills:
            reasons.append(f"removed mandatory skill: {', '.join(removed_skills).upper()}")
            
        # Check leadership slider
        old_lead = old_state.get("leadership", 0.3)
        new_lead = new_state.get("leadership", 0.3)
        if old_lead != new_lead:
            reasons.append(f"leadership potential weight shifted from {old_lead} to {new_lead}")
            
        reason_str = "; ".join(reasons)
        sign = "+" if score_diff >= 0 else ""
        
        return (
            f"Candidate {candidate_name} moved {direction} by {delta} position(s) "
            f"(Rank {old_rank} → {new_rank}).\n"
            f"Reasoning: {reason_str}.\n"
            f"Resulting Score Change: {sign}{score_diff:.1f} points."
        )
