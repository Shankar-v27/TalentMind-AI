# graphs/argument_graph.py

from typing import Dict, List, Any

class ArgumentGraphGenerator:
    def generate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build supporting and opposing edges between candidate characteristics.
        """
        # Node structures
        nodes = [
            {"id": "skills", "label": "Technical Competence", "value": 0.88},
            {"id": "learning", "label": "Learning Velocity", "value": 0.90},
            {"id": "leadership", "label": "Leadership DNA", "value": 0.86},
            {"id": "gaps", "label": "Infrastructure Gaps", "value": 0.65},
            {"id": "tenure", "label": "Short Tenures", "value": 0.70}
        ]
        
        # Edges
        edges = [
            {"source": "learning", "target": "skills", "type": "supports", "weight": 0.80},
            {"source": "learning", "target": "leadership", "type": "supports", "weight": 0.60},
            {"source": "tenure", "target": "leadership", "type": "opposes", "weight": -0.40},
            {"source": "gaps", "target": "skills", "type": "opposes", "weight": -0.50}
        ]
        
        return {
            "nodes": nodes,
            "edges": edges
        }
