# intelligence/recruiter_memory/embedding_engine.py

import numpy as np
from typing import Dict, List, Any

class EmbeddingEngine:
    def generate_candidate_embedding(self, candidate: Dict[str, Any]) -> List[float]:
        """
        Generates a deterministic 768-dimensional embedding for a candidate profile.
        Uses key metrics and properties to populate the vector space.
        """
        score = float(candidate.get("score", 75.0))
        quality = float(candidate.get("quality_score", 75.0))
        future = float(candidate.get("future_score", 75.0))
        leadership = float(candidate.get("leadership_score", 75.0))
        
        # Build raw components
        vector = np.zeros(768)
        vector[0] = score / 100.0
        vector[1] = quality / 100.0
        vector[2] = future / 100.0
        vector[3] = leadership / 100.0
        
        # Populate with deterministic pseudo-noise based on candidate_id to ensure uniqueness
        cand_id = candidate.get("candidate_id", "default")
        seed = sum(ord(char) for char in cand_id)
        rng = np.random.default_rng(seed)
        noise = rng.normal(0.0, 0.1, 768)
        
        final_vector = vector + noise
        # Normalize
        norm = np.linalg.norm(final_vector) or 1.0
        normalized_vector = final_vector / norm
        
        return normalized_vector.tolist()

    def generate_recruiter_embedding(self, preferences: Dict[str, float]) -> List[float]:
        """
        Generates a 768-dimensional embedding for a recruiter based on their preference profile.
        """
        vector = np.zeros(768)
        vector[0] = preferences.get("communication", 0.5)
        vector[1] = preferences.get("leadership", 0.5)
        vector[2] = preferences.get("github", 0.5)
        vector[3] = preferences.get("opensource", 0.5)
        vector[4] = preferences.get("learning", 0.5)
        vector[5] = preferences.get("stability", 0.5)
        
        # Set dummy projection values
        seed = int(sum(preferences.values()) * 100) or 42
        rng = np.random.default_rng(seed)
        noise = rng.normal(0.0, 0.05, 768)
        
        final_vector = vector + noise
        norm = np.linalg.norm(final_vector) or 1.0
        return (final_vector / norm).tolist()
