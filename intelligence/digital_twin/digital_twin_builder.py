# intelligence/digital_twin/digital_twin_builder.py

from typing import Dict, Any

class DigitalTwinBuilder:
    def build_twin(self, candidate_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assemble the digital twin model schema.
        """
        return {
            "candidate_id": candidate_id,
            "behavioral_profile": data.get("behavior", {}),
            "career_profile": data.get("career", {}),
            "leadership_profile": data.get("leadership", {}),
            "team_profile": data.get("team", {}),
            "future_profile": data.get("future", {})
        }
