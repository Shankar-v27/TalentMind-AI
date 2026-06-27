# intelligence/optimizer/scenario_optimizer.py

from typing import Dict, List, Any

class ScenarioOptimizer:
    SCENARIO_CONFIGS = {
        "startup": {
            "label": "Startup Mode",
            "weights": {"innovation": 0.4, "learning": 0.3, "leadership": 0.2, "risk": -0.1},
            "description": "High growth focus prioritizing agility, learning speed, and innovation capability."
        },
        "corporate": {
            "label": "Corporate Mode",
            "weights": {"leadership": 0.4, "retention": 0.3, "culture": 0.3},
            "description": "Enterprise alignment focusing on team stability, structure fit, and retention."
        },
        "government": {
            "label": "Government Mode",
            "weights": {"retention": 0.4, "culture": 0.4, "risk": -0.2},
            "description": "Highly risk-averse structure optimizing compliance, stability, and minimum churn."
        },
        "research": {
            "label": "Research Mode",
            "weights": {"innovation": 0.5, "learning": 0.3, "knowledge_diversity": 0.2},
            "description": "R&D operations targeting extreme expertise, new learning adoption, and knowledge diversity."
        }
    }

    def run_scenario(
        self,
        candidates: List[Dict[str, Any]],
        scenario_id: str = "startup"
    ) -> Dict[str, Any]:
        """
        Applies a scenario weighting and identifies the highest scoring candidate.
        """
        config = self.SCENARIO_CONFIGS.get(scenario_id, self.SCENARIO_CONFIGS["startup"])
        weights = config["weights"]
        
        best_cand = None
        best_score = -99999.0
        
        scored_candidates = []
        for cand in candidates:
            objs = cand.get("objectives", {})
            score = 0.0
            
            for key, weight in weights.items():
                val = objs.get(key, 50.0)
                # handle inverse weights (e.g. minimizing risk)
                if weight < 0:
                    score += abs(weight) * (100.0 - val)
                else:
                    score += weight * val
                    
            scored_candidates.append({
                "candidate_id": cand.get("candidate_id"),
                "name": cand.get("name"),
                "score": round(score, 1)
            })
            
            if score > best_score:
                best_score = score
                best_cand = cand
                
        return {
            "scenario": scenario_id,
            "label": config["label"],
            "description": config["description"],
            "recommended_candidate": best_cand.get("candidate_id") if best_cand else None,
            "recommended_candidate_name": best_cand.get("name") if best_cand else "N/A",
            "scores": sorted(scored_candidates, key=lambda x: x["score"], reverse=True)
        }
