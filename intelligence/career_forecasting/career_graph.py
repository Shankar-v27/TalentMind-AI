# intelligence/career_forecasting/career_graph.py

import json
import os
from typing import Dict, List, Any

CAREER_LEVELS = {
    "intern": 0,
    "junior_engineer": 1,
    "engineer": 2,
    "senior_engineer": 3,
    "staff_engineer": 4,
    "tech_lead": 5,
    "architect": 6,
    "manager": 7,
    "director": 8,
    "vp": 9,
    "cto": 10
}

class CareerGraph:
    def __init__(self):
        self.levels = CAREER_LEVELS
        self.graph_data = {}
        self._load_graph()

    def _load_graph(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge", "career_graph.json")
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    for item in data.get("roles", []):
                        self.graph_data[item["node"]] = item["next_roles"]
            except Exception:
                pass

    def get_next_roles(self, current_role: str) -> List[Dict[str, Any]]:
        normalized = current_role.lower().replace(" ", "_")
        return self.graph_data.get(normalized, [{"role": "senior_engineer", "probability": 0.50}])
