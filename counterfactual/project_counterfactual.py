# counterfactual/project_counterfactual.py

from typing import Dict, List, Any

class ProjectCounterfactual:
    def evaluate(self, gaps: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines what type of projects are missing (production, microservices, open source, etc).
        """
        missing = gaps.get("missing_projects", [])
        required_projects = missing if missing else ["production deployment", "microservice architecture"]
        
        # Format names nicely
        formatted = [p.replace("_", " ").title() for p in required_projects]
        
        return {
            "required_projects": formatted
        }
