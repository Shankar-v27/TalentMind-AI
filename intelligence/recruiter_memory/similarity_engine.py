# intelligence/recruiter_memory/similarity_engine.py

from typing import Dict, List, Any
import numpy as np

class SimilarityEngine:
    def calculate_similarity_to_past_hires(
        self,
        candidate: Dict[str, Any],
        hired_embeddings: List[List[float]],
        candidate_embedding: List[float]
    ) -> float:
        """
        Calculates similarity index between target candidate and past hire vectors.
        """
        if not hired_embeddings or not candidate_embedding:
            return 0.0
            
        c_vector = np.array(candidate_embedding)
        similarities = []
        
        for h_vec in hired_embeddings:
            h_vector = np.array(h_vec)
            # Cosine similarity
            dot = np.dot(c_vector, h_vector)
            norm_c = np.linalg.norm(c_vector)
            norm_h = np.linalg.norm(h_vector)
            if norm_c > 0 and norm_h > 0:
                sim = dot / (norm_c * norm_h)
                similarities.append(sim)
                
        if not similarities:
            return 0.0
            
        # Return average similarity index
        return round(float(np.mean(similarities)), 3)
