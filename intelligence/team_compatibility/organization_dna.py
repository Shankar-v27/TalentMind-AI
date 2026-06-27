# intelligence/team_compatibility/organization_dna.py

from typing import Dict, Any

class OrganizationDNABuilder:
    def build(self, org_profile: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Build general organization profile characteristics.
        """
        profile = org_profile or {}
        
        return {
            "organization": profile.get("organization", "startup"),
            "risk": float(profile.get("risk", 0.91)),
            "innovation": float(profile.get("innovation", 0.93)),
            "ownership": float(profile.get("ownership", 0.88)),
            "speed": float(profile.get("speed", 0.95))
        }
