# intelligence/recruiter_memory/preference_engine.py

from typing import Dict, List, Any

class PreferenceEngine:
    def calculate_preferences(self, actions: List[Dict[str, Any]], candidates_map: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """
        Derives recruiter preference weights based on positive vs negative actions.
        Positive actions (hired, shortlisted, saved) boost preferences; negatives lower them.
        """
        preferences = {
            "communication": 0.5,
            "leadership": 0.5,
            "github": 0.5,
            "opensource": 0.5,
            "learning": 0.5,
            "stability": 0.5
        }
        
        counts = {k: 0 for k in preferences}
        
        for act in actions:
            action_type = act["action"]
            cand_id = act["candidate_id"]
            cand = candidates_map.get(cand_id, {})
            
            # Extract candidate metrics
            c_comm = float(cand.get("communication_score", 50.0)) / 100.0
            c_lead = float(cand.get("leadership_score", 50.0)) / 100.0
            c_learn = float(cand.get("learning_velocity", 0.5))
            c_stable = float(cand.get("retention_probability", 0.5))
            
            # GitHub & OpenSource
            signals = cand.get("redrob_signals", {})
            c_git = 1.0 if signals.get("github_activity_score") and signals.get("github_activity_score") > 70 else 0.4
            c_os = 1.0 if signals.get("has_open_source_contributions") else 0.3
            
            # Action weight
            weight = 1.0
            if action_type in ["hired", "shortlisted"]:
                weight = 1.5
            elif action_type == "rejected":
                weight = -1.2
            elif action_type == "ignored":
                weight = -0.5
                
            preferences["communication"] += c_comm * weight
            preferences["leadership"] += c_lead * weight
            preferences["github"] += c_git * weight
            preferences["opensource"] += c_os * weight
            preferences["learning"] += c_learn * weight
            preferences["stability"] += c_stable * weight
            
            for k in counts:
                counts[k] += 1
                
        # Normalize to [0.0, 1.0] range
        for key in preferences:
            val = preferences[key]
            # Softmax or simple bounding
            preferences[key] = round(min(1.0, max(0.0, val / max(1.0, counts[key] * 0.8))), 2)
            
        return preferences
