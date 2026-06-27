# intelligence/recruiter_memory/feedback_engine.py

from typing import Dict, List, Any

class FeedbackEngine:
    def __init__(self):
        self.feedback_store: List[Dict[str, Any]] = []

    def record_feedback(
        self,
        recruiter_id: str,
        candidate_id: str,
        feedback_type: str, # 'thumbs_up', 'thumbs_down', 'override'
        score_adjustment: float
    ) -> Dict[str, Any]:
        """
        Records manual override actions by recruiters.
        """
        entry = {
            "recruiter_id": recruiter_id,
            "candidate_id": candidate_id,
            "feedback_type": feedback_type,
            "score_adjustment": score_adjustment
        }
        self.feedback_store.append(entry)
        return entry

    def get_recruiter_adjustments(self, recruiter_id: str) -> Dict[str, float]:
        adjustments = {}
        for entry in self.feedback_store:
            if entry["recruiter_id"] == recruiter_id:
                adjustments[entry["candidate_id"]] = entry["score_adjustment"]
        return adjustments
