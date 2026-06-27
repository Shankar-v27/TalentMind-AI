# intelligence/team_compatibility/social_graph.py

from typing import Dict, List, Any

class SocialGraphEngine:
    def build_graph(self, candidate: Dict[str, Any], team_dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Model social connections and centrality metrics.
        """
        return {
            "nodes": [
                {"id": "Alice", "role": "Tech Lead", "centrality": 0.85},
                {"id": "Bob", "role": "Senior Developer", "centrality": 0.72},
                {"id": "David", "role": "QA Engineer", "centrality": 0.50},
                {"id": "Emma", "role": "Product Manager", "centrality": 0.90},
                {"id": "Candidate", "role": "Senior Engineer", "centrality": 0.68}
            ],
            "edges": [
                {"source": "Alice", "target": "Bob", "weight": 0.8},
                {"source": "Alice", "target": "Emma", "weight": 0.9},
                {"source": "Bob", "target": "Candidate", "weight": 0.75},
                {"source": "Emma", "target": "Candidate", "weight": 0.82},
                {"source": "David", "target": "Bob", "weight": 0.50}
            ]
        }
