# intelligence/optimizer/organization_optimizer.py

from typing import Dict, List, Any

class OrganizationOptimizer:
    def optimize_organization(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates organizational outcomes: business value, innovation, retention, leadership.
        """
        objs = candidate.get("objectives", {})
        biz_val = objs.get("business_value", 75.0) / 100.0
        innov = objs.get("innovation", 75.0) / 100.0
        ret = objs.get("retention", 85.0) / 100.0
        lead = objs.get("leadership", 70.0) / 100.0
        
        org_val = round((biz_val * 0.4 + innov * 0.2 + ret * 0.2 + lead * 0.2), 2)
        
        return {
            "candidate_id": candidate.get("candidate_id"),
            "name": candidate.get("name"),
            "organization_value": org_val,
            "breakdown": {
                "business_value": biz_val,
                "innovation_contribution": innov,
                "retention_stability": ret,
                "leadership_capital": lead
            }
        }
