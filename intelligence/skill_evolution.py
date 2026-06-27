# intelligence/skill_evolution.py

from typing import Dict, List, Any

class SkillEvolutionPredictor:
    SKILL_TRANSITION_GRAPH = {
        "python": ["fastapi", "django", "scikit-learn", "numpy", "pandas"],
        "fastapi": ["docker", "postgresql", "redis", "kubernetes", "grpc"],
        "docker": ["kubernetes", "terraform", "devops", "aws", "github actions"],
        "aws": ["terraform", "lambda", "ecs", "kubernetes", "cloudformation"],
        "javascript": ["typescript", "react", "node.js", "next.js", "tailwind"],
        "react": ["next.js", "typescript", "redux", "graphql", "tailwind"],
        "node.js": ["express", "mongodb", "postgresql", "typescript", "docker"],
        "pytorch": ["llms", "rag", "embeddings", "faiss", "transformers", "deep learning"],
        "llms": ["rag", "faiss", "langchain", "prompt engineering", "agentic workflows"],
        "rag": ["faiss", "qdrant", "milvus", "vector databases", "langchain"],
        "faiss": ["qdrant", "pinecone", "milvus", "embeddings", "vector search"],
        "java": ["spring boot", "microservices", "kubernetes", "aws", "docker"],
        "c++": ["cuda", "computer vision", "opencv", "embedded systems", "rust"],
        "sql": ["postgresql", "mongodb", "redis", "data warehousing", "dbt"]
    }

    def predict(self, candidate: Dict[str, Any], learning_velocity: float) -> Dict[str, List[str]]:
        """
        Predicts skills the candidate will acquire in 6, 12, and 24 months.
        Utilizes technology transition maps and learning speed.
        """
        skills = [s.get("name", "").lower() for s in candidate.get("skills", []) if s.get("name")]
        base_skills = set(skills)
        
        # Build logical transition pipeline
        future_skills_pool = []
        for skill in skills:
            for target in self.SKILL_TRANSITION_GRAPH.get(skill, []):
                if target not in base_skills and target not in future_skills_pool:
                    future_skills_pool.append(target)
                    
        # Append default technical concepts
        defaults = ["system design", "microservices", "devops", "kubernetes", "ci/cd", "observability"]
        for d in defaults:
            if d not in base_skills and d not in future_skills_pool:
                future_skills_pool.append(d)
                
        # Learning velocity dictates scaling capacity
        skills_per_year = max(1, int(learning_velocity * 4))
        
        predicted_6m = []
        predicted_12m = []
        predicted_24m = []
        
        idx = 0
        # 6 Months (immediate extensions)
        limit_6m = max(1, skills_per_year // 2)
        while idx < len(future_skills_pool) and len(predicted_6m) < limit_6m:
            item = future_skills_pool[idx]
            predicted_6m.append(item)
            idx += 1
            
        # 12 Months
        limit_12m = max(1, skills_per_year)
        while idx < len(future_skills_pool) and len(predicted_12m) < limit_12m:
            item = future_skills_pool[idx]
            if item not in predicted_6m:
                predicted_12m.append(item)
            idx += 1
            
        # 24 Months
        limit_24m = max(2, skills_per_year * 2)
        while idx < len(future_skills_pool) and len(predicted_24m) < limit_24m:
            item = future_skills_pool[idx]
            if item not in predicted_6m and item not in predicted_12m:
                predicted_24m.append(item)
            idx += 1
            
        # Capitalize for frontend UI display
        return {
            "6_months": [s.title() if len(s) > 3 else s.upper() for s in predicted_6m],
            "12_months": [s.title() if len(s) > 3 else s.upper() for s in predicted_12m],
            "24_months": [s.title() if len(s) > 3 else s.upper() for s in predicted_24m]
        }
