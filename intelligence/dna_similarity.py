# intelligence/dna_similarity.py

import math
from typing import Dict, Any

class DNASimilarity:
    def calculate(self, candidate_dna: Dict[str, float], organization_dna: Dict[str, float]) -> Dict[str, float]:
        # Extract common keys
        common_keys = sorted(list(set(candidate_dna.keys()).intersection(set(organization_dna.keys()))))
        if not common_keys:
            return {
                "organization_match": 0.5,
                "work_style_match": 0.5,
                "leadership_match": 0.5,
                "innovation_match": 0.5
            }
            
        # Cosine Similarity
        dot_product = sum(candidate_dna[k] * organization_dna[k] for k in common_keys)
        mag_c = math.sqrt(sum(candidate_dna[k]**2 for k in common_keys))
        mag_o = math.sqrt(sum(organization_dna[k]**2 for k in common_keys))
        cosine_sim = dot_product / (mag_c * mag_o) if mag_c > 0 and mag_o > 0 else 0.0
        
        # Euclidean Similarity (1 / (1 + distance))
        euclidean_dist = math.sqrt(sum((candidate_dna[k] - organization_dna[k])**2 for k in common_keys))
        euclidean_sim = 1.0 / (1.0 + euclidean_dist)
        
        # Manhattan Similarity
        manhattan_dist = sum(abs(candidate_dna[k] - organization_dna[k]) for k in common_keys)
        manhattan_sim = 1.0 / (1.0 + manhattan_dist)
        
        # Category matches
        c_work = (candidate_dna.get("speed", 0.5) + candidate_dna.get("adaptability", 0.5) + candidate_dna.get("execution", 0.5)) / 3.0
        o_work = (organization_dna.get("speed", 0.5) + organization_dna.get("adaptability", 0.5) + organization_dna.get("execution", 0.5)) / 3.0
        work_style_match = 1.0 - abs(c_work - o_work)
        
        c_inno = (candidate_dna.get("innovation", 0.5) + candidate_dna.get("experimentation", 0.5) + candidate_dna.get("creativity", 0.5)) / 3.0
        o_inno = (organization_dna.get("innovation", 0.5) + organization_dna.get("experimentation", 0.5) + organization_dna.get("creativity", 0.5)) / 3.0
        innovation_match = 1.0 - abs(c_inno - o_inno)
        
        c_lead = (candidate_dna.get("leadership", 0.5) + candidate_dna.get("management", 0.5) + candidate_dna.get("autonomy", 0.5)) / 3.0
        o_lead = (organization_dna.get("leadership", 0.5) + organization_dna.get("autonomy", 0.5)) / 2.0
        leadership_match = 1.0 - abs(c_lead - o_lead)
        
        learning_match = 1.0 - abs(candidate_dna.get("learning", 0.5) - organization_dna.get("learning", 0.5))
        risk_match = 1.0 - abs(candidate_dna.get("risk", 0.5) - organization_dna.get("risk", 0.5))
        comm_match = 1.0 - abs(candidate_dna.get("communication", 0.5) - organization_dna.get("communication", 0.5))
        stability_match = 1.0 - abs(candidate_dna.get("stability", 0.5) - organization_dna.get("stability", 0.5))
        
        # Weighted formula
        final_dna_score = (
            0.25 * work_style_match +
            0.20 * innovation_match +
            0.15 * leadership_match +
            0.15 * comm_match +
            0.10 * learning_match +
            0.10 * risk_match +
            0.05 * stability_match
        )
        
        return {
            "organization_match": round(final_dna_score, 2),
            "work_style_match": round(work_style_match, 2),
            "leadership_match": round(leadership_match, 2),
            "innovation_match": round(innovation_match, 2),
            "cosine_similarity": round(cosine_sim, 2),
            "euclidean_similarity": round(euclidean_sim, 2),
            "manhattan_similarity": round(manhattan_sim, 2)
        }
