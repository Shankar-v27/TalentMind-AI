# intelligence/recruiter_memory/explainability_engine.py

from typing import Dict, Any

class RecruiterExplainabilityEngine:
    def explain_personalization(
        self,
        candidate_name: str,
        preferences: Dict[str, float],
        candidate: Dict[str, Any],
        boost: float
    ) -> Dict[str, Any]:
        """
        Formulates explainable rationale regarding why the candidate is boosted.
        """
        comm = preferences.get("communication", 0.5) * 100.0
        lead = preferences.get("leadership", 0.5) * 100.0
        git = preferences.get("github", 0.5) * 100.0
        opens = preferences.get("opensource", 0.5) * 100.0
        
        narrative = (
            f"Candidate '{candidate_name}' ranked higher due to recruiter personalization boost.\n\n"
            f"Recruiter Historical Preferences:\n"
            f"- GitHub Activity: {round(git)}%\n"
            f"- Leadership focus: {round(lead)}%\n"
            f"- Communication preference: {round(comm)}%\n"
            f"- Open Source contributions: {round(opens)}%\n\n"
            f"Candidate Match Quality:\n"
            f"- Communication alignment: {candidate.get('communication_score', 80)}%\n"
            f"- Leadership alignment: {candidate.get('leadership_score', 75)}%\n\n"
            f"Personalization Boost Applied: +{boost} points."
        )
        
        return {
            "candidate_name": candidate_name,
            "explanation": narrative,
            "boost": boost
        }
