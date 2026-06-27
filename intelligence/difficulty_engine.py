# intelligence/difficulty_engine.py

from typing import Dict, List, Any

class DifficultyEngine:
    def classify(self, item_name: str) -> str:
        """
        Classifies learning/project tasks into difficulty levels (Easy, Medium, Hard, Very Hard).
        """
        name_lower = item_name.lower()
        if any(w in name_lower for w in ["docker", "fastapi", "python", "git", "sql"]):
            return "Easy"
        elif any(w in name_lower for w in ["kubernetes", "terraform", "aws", "ci/cd", "devops"]):
            return "Medium"
        elif any(w in name_lower for w in ["system design", "microservices", "deployment", "rag", "ai"]):
            return "Hard"
        else:
            return "Very Hard"
