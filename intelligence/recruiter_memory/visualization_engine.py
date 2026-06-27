# intelligence/recruiter_memory/visualization_engine.py

from typing import Dict, List, Any

class RecruiterVisualizationEngine:
    def format_visualization(
        self,
        preferences: Dict[str, float],
        behavior: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Prepares standard radar chart coordinates, timelines, and heatmaps.
        """
        # Radar chart points
        radar_data = [
            {"subject": "Leadership", "value": round(preferences.get("leadership", 0.5) * 100)},
            {"subject": "Communication", "value": round(preferences.get("communication", 0.5) * 100)},
            {"subject": "GitHub Activity", "value": round(preferences.get("github", 0.5) * 100)},
            {"subject": "Innovation", "value": round(behavior.get("innovation_preference", 0.5) * 100)},
            {"subject": "Retention", "value": round(preferences.get("stability", 0.5) * 100)}
        ]
        
        # Preference Timeline
        timeline = [
            {"year": "2024", "focus": "Communication & Retention stability focus"},
            {"year": "2025", "focus": "GitHub activity & Open Source contributor preference boost"},
            {"year": "2026", "focus": "AI/ML developer velocity & Fast learning capacity"}
        ]
        
        # Hiring Heatmap
        heatmap = [
            {"attribute": "Communication", "value": round(preferences.get("communication", 0.5) * 100)},
            {"attribute": "GitHub", "value": round(preferences.get("github", 0.5) * 100)},
            {"attribute": "Leadership", "value": round(preferences.get("leadership", 0.5) * 100)},
            {"attribute": "Innovation", "value": round(behavior.get("innovation_preference", 0.5) * 100)}
        ]
        
        return {
            "radar": radar_data,
            "timeline": timeline,
            "heatmap": heatmap
        }
