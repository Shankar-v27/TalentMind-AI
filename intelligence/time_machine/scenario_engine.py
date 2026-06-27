# intelligence/time_machine/scenario_engine.py

from typing import Dict, Any

class ScenarioEngine:
    SCENARIO_PRESETS = {
        "high_skill": {
            "label": "Scenario A: High Skill Focus",
            "weights": {"skill": 0.70, "experience": 0.10, "leadership": 0.05, "future": 0.05, "retention": 0.05, "risk": 0.05},
            "description": "Prioritizes deep technical skill alignment over all other parameters."
        },
        "fast_hiring": {
            "label": "Scenario B: Urgent Backfill",
            "weights": {"skill": 0.15, "experience": 0.15, "leadership": 0.05, "future": 0.05, "retention": 0.10, "risk": 0.50},
            "description": "Prioritizes fast-onboarding notice periods and immediate availability."
        },
        "future_potential": {
            "label": "Scenario C: Future Leaders",
            "weights": {"skill": 0.10, "experience": 0.10, "leadership": 0.10, "future": 0.60, "retention": 0.05, "risk": 0.05},
            "description": "Optimizes for long-term learning velocity and career acceleration profiles."
        },
        "leadership_focus": {
            "label": "Scenario D: Leadership Capabilities",
            "weights": {"skill": 0.10, "experience": 0.10, "leadership": 0.60, "future": 0.10, "retention": 0.05, "risk": 0.05},
            "description": "Prioritizes strategic management capabilities and organization DNA fit."
        },
        "low_cost": {
            "label": "Scenario E: Budget Optimization",
            "weights": {"skill": 0.20, "experience": 0.10, "leadership": 0.05, "future": 0.05, "retention": 0.30, "risk": 0.30},
            "description": "Prioritizes candidates fitting constrained salary requirements."
        }
    }

    def get_preset(self, scenario_id: str) -> Dict[str, Any]:
        return self.SCENARIO_PRESETS.get(scenario_id, self.SCENARIO_PRESETS["high_skill"])

    def get_all_presets(self) -> Dict[str, Dict[str, Any]]:
        return self.SCENARIO_PRESETS
