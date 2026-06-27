# intelligence/recruiter_memory/personalization_engine.py

from typing import Dict, List, Any

class PersonalizationEngine:
    def personalize_rankings(
        self,
        candidates: List[Dict[str, Any]],
        preferences: Dict[str, float],
        behavior: Dict[str, float],
        adjustments: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Ranks candidates dynamically, incorporating global metrics, recruiter preferences,
        behavior parameters, and explicit feedback modifiers.
        """
        personalized_list = []
        
        for cand in candidates:
            cand_id = cand.get("candidate_id") or cand.get("id")
            global_score = float(cand.get("score", 75.0) or 75.0)
            
            # 1. Recruiter Preference Alignment
            # Boost matches based on communicator / leadership alignment
            c_comm = float(cand.get("communication_score", 50.0)) / 100.0
            c_lead = float(cand.get("leadership_score", 50.0)) / 100.0
            
            pref_comm = preferences.get("communication", 0.5)
            pref_lead = preferences.get("leadership", 0.5)
            
            pref_boost = (c_comm * pref_comm + c_lead * pref_lead) * 10.0
            
            # 2. Recruiter Behavior Alignment
            # Boost if candidate matches innovation preferences
            c_innov = float(cand.get("innovation_score", 60.0)) / 100.0
            behav_innov = behavior.get("innovation_preference", 0.5)
            behav_boost = (c_innov * behav_innov) * 5.0
            
            # 3. Explicit feedback overrides
            feedback_boost = adjustments.get(cand_id, 0.0)
            
            # 4. Total Personalized Score calculation
            personalized_score = global_score + pref_boost + behav_boost + feedback_boost
            
            cand_copy = cand.copy()
            cand_copy["global_score"] = round(global_score, 1)
            cand_copy["personalized_score"] = round(personalized_score, 1)
            cand_copy["personalization_boost"] = round(pref_boost + behav_boost + feedback_boost, 1)
            
            personalized_list.append(cand_copy)
            
        # Re-sort candidates by personalized score
        personalized_list.sort(key=lambda x: x["personalized_score"], reverse=True)
        return personalized_list
