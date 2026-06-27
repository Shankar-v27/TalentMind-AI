# intelligence/recruiter_memory/pattern_engine.py

from typing import Dict, List, Any

class PatternEngine:
    def discover_patterns(
        self,
        actions: List[Dict[str, Any]],
        candidates_map: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Discovers patterns of candidates who were hired or shortlisted.
        For example: experience levels, key skill matches, communication levels.
        """
        success_actions = [a for a in actions if a["action"] in ["hired", "shortlisted"]]
        if not success_actions:
            return [{"pattern": "general", "confidence": 0.5, "description": "Insufficient history to trace preference patterns."}]
            
        # Count occurrences of specific flags
        has_git_count = 0
        has_os_count = 0
        high_lead_count = 0
        total = len(success_actions)
        
        for act in success_actions:
            cand = candidates_map.get(act["candidate_id"], {})
            signals = cand.get("redrob_signals", {})
            lead = float(cand.get("leadership_score", 50.0))
            
            if signals.get("github_activity_score") and signals.get("github_activity_score") > 70:
                has_git_count += 1
            if signals.get("has_open_source_contributions"):
                has_os_count += 1
            if lead > 75:
                high_lead_count += 1
                
        patterns = []
        if has_git_count / total >= 0.6:
            patterns.append({
                "pattern": "github_activity",
                "confidence": round(has_git_count / total, 2),
                "description": "Strong preference for candidates with active GitHub profiles."
            })
        if has_os_count / total >= 0.5:
            patterns.append({
                "pattern": "opensource_contributions",
                "confidence": round(has_os_count / total, 2),
                "description": "Strong preference for candidates with open-source project contributions."
            })
        if high_lead_count / total >= 0.6:
            patterns.append({
                "pattern": "leadership_skills",
                "confidence": round(high_lead_count / total, 2),
                "description": "Strong preference for candidates exhibiting robust leadership capability."
            })
            
        if not patterns:
            patterns.append({
                "pattern": "general_competence",
                "confidence": 0.7,
                "description": "Prefers general competence, matching candidate scores above 80."
            })
            
        return patterns
