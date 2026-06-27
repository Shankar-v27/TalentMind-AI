# intelligence/skill_evolution/knowledge_graph.py

from typing import Dict, List, Any

class SkillKnowledgeGraph:
    def get_relations(self) -> Dict[str, List[str]]:
        """
        Return the dictionary representing transition pathways.
        """
        return {
            "python": ["machine_learning", "backend"],
            "machine_learning": ["deep_learning"],
            "deep_learning": ["llm_engineering"],
            "backend": ["cloud"],
            "cloud": ["kubernetes"],
            "kubernetes": ["platform_architecture"]
        }
