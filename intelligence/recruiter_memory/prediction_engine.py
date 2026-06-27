# intelligence/recruiter_memory/prediction_engine.py

from typing import Dict, Any

class HiringPredictionEngine:
    def predict_action(
        self,
        candidate: Dict[str, Any],
        preferences: Dict[str, float],
        behavior: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Uses sigmoid projection of candidate-preferences alignment to predict
        hire, shortlist, interview, and reject probability scales.
        """
        c_comm = float(candidate.get("communication_score", 50.0)) / 100.0
        c_lead = float(candidate.get("leadership_score", 50.0)) / 100.0
        c_innov = float(candidate.get("innovation_score", 50.0)) / 100.0
        
        pref_comm = preferences.get("communication", 0.5)
        pref_lead = preferences.get("leadership", 0.5)
        behav_innov = behavior.get("innovation_preference", 0.5)
        
        # Alignment score
        alignment = (c_comm * pref_comm + c_lead * pref_lead + c_innov * behav_innov) / 3.0
        
        hire_p = min(0.95, max(0.05, alignment * 1.1))
        shortlist_p = min(0.98, max(0.05, alignment * 1.3))
        interview_p = min(0.98, max(0.05, alignment * 1.4))
        reject_p = round(1.0 - shortlist_p, 2)
        
        return {
            "hire_probability": round(hire_p, 2),
            "shortlist_probability": round(shortlist_p, 2),
            "interview_probability": round(interview_p, 2),
            "reject_probability": round(reject_p, 2)
        }
