# intelligence/recruiter_memory/recommendation_engine.py

from typing import Dict, List, Any

class RecruiterRecommendationEngine:
    def generate_recommendations(
        self,
        personalized_candidates: List[Dict[str, Any]],
        preferences: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Builds strategic candidate recommendation groups aligned to high preference parameters.
        """
        # Determine highest preferences
        sorted_prefs = sorted(preferences.items(), key=lambda x: x[1], reverse=True)
        top_pref = sorted_prefs[0][0] if sorted_prefs else "quality"
        
        recs = []
        for cand in personalized_candidates[:3]:
            recs.append({
                "candidate_id": cand.get("candidate_id") or cand.get("id"),
                "name": cand.get("name"),
                "match_reason": f"Highly recommended because this candidate aligns with your top preference: '{top_pref.upper()}'."
            })
            
        return {
            "top_preference": top_pref,
            "recommendations": recs
        }
