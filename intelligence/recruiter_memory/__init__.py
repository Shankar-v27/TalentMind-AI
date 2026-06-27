# intelligence/recruiter_memory/__init__.py

from typing import Dict, List, Any

from .memory_collector import MemoryCollector
from .recruiter_graph import RecruiterKnowledgeGraph
from .preference_engine import PreferenceEngine
from .behavior_engine import BehaviorEngine
from .feedback_engine import FeedbackEngine
from .embedding_engine import EmbeddingEngine
from .personalization_engine import PersonalizationEngine
from .prediction_engine import HiringPredictionEngine
from .similarity_engine import SimilarityEngine
from .habit_engine import HabitEngine
from .pattern_engine import PatternEngine
from .recommendation_engine import RecruiterRecommendationEngine
from .reinforcement_engine import RecruiterReinforcementEngine
from .explainability_engine import RecruiterExplainabilityEngine
from .visualization_engine import RecruiterVisualizationEngine

class RecruiterMemoryGraphManager:
    def __init__(self):
        self.collector = MemoryCollector()
        self.graph = RecruiterKnowledgeGraph()
        self.preference = PreferenceEngine()
        self.behavior = BehaviorEngine()
        self.feedback = FeedbackEngine()
        self.embedding = EmbeddingEngine()
        self.personalization = PersonalizationEngine()
        self.prediction = HiringPredictionEngine()
        self.similarity = SimilarityEngine()
        self.habit = HabitEngine()
        self.pattern = PatternEngine()
        self.recommendation = RecruiterRecommendationEngine()
        self.reinforcement = RecruiterReinforcementEngine()
        self.explain = RecruiterExplainabilityEngine()
        self.visual = RecruiterVisualizationEngine()

    def process_recruiter_profile(
        self,
        recruiter_id: str,
        candidates: List[Dict[str, Any]],
        actions: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Runs the full Recruiter Memory Graph personalization pipeline.
        """
        candidates_map = {c.get("candidate_id") or c.get("id"): c for c in candidates}
        
        # 1. Collect / Load actions
        if not actions:
            # Seed mock history actions to prevent cold start issues
            actions = [
                {"recruiter_id": recruiter_id, "candidate_id": candidates[0].get("candidate_id"), "action": "hired"},
                {"recruiter_id": recruiter_id, "candidate_id": candidates[-1].get("candidate_id"), "action": "shortlisted"},
                {"recruiter_id": recruiter_id, "candidate_id": candidates[0].get("candidate_id"), "action": "saved"}
            ]
            
        for act in actions:
            self.collector.record_activity(
                recruiter_id=act["recruiter_id"],
                candidate_id=act["candidate_id"],
                action=act["action"]
            )
            
        recruiter_actions = self.collector.get_recruiter_logs(recruiter_id)
        
        # 2. Build networkx knowledge graph relation
        self.graph.build_recruiter_nodes(recruiter_id, recruiter_actions, candidates_map)
        
        # 3. Calculate preferences & behaviors
        prefs = self.preference.calculate_preferences(recruiter_actions, candidates_map)
        behav = self.behavior.calculate_behavior(recruiter_actions, candidates_map)
        adjustments = self.feedback.get_recruiter_adjustments(recruiter_id)
        
        # 4. Compile recruiter DNA & embeddings
        dna = self.habit.compile_recruiter_dna(prefs, behav)
        r_embedding = self.embedding.generate_recruiter_embedding(prefs)
        
        # Calculate hired profiles similarity matrix
        hired_embeddings = []
        for act in recruiter_actions:
            if act["action"] == "hired":
                cand_obj = candidates_map.get(act["candidate_id"])
                if cand_obj:
                    h_embed = self.embedding.generate_candidate_embedding(cand_obj)
                    hired_embeddings.append(h_embed)
                    
        # 5. Personalize rankings
        personalized_candidates = self.personalization.personalize_rankings(
            candidates=candidates,
            preferences=prefs,
            behavior=behav,
            adjustments=adjustments
        )
        
        # Process similarity to past hires & predictions
        for cand in personalized_candidates:
            c_embed = self.embedding.generate_candidate_embedding(cand)
            cand["similarity_to_hires"] = self.similarity.calculate_similarity_to_past_hires(
                cand, hired_embeddings, c_embed
            )
            cand["predictions"] = self.prediction.predict_action(cand, prefs, behav)
            
        # 6. Generate Recommendations & patterns
        recs = self.recommendation.generate_recommendations(personalized_candidates, prefs)
        patterns = self.pattern.discover_patterns(recruiter_actions, candidates_map)
        
        # 7. Reinforcement values
        q_vals = self.reinforcement.get_q_values(recruiter_id)
        
        # 8. Explanations & Visuals
        selected_cand = personalized_candidates[0]
        explanation = self.explain.explain_personalization(
            candidate_name=selected_cand.get("name"),
            preferences=prefs,
            candidate=selected_cand,
            boost=selected_cand.get("personalization_boost", 0.0)
        )
        
        visual_data = self.visual.format_visualization(prefs, behav)
        
        return {
            "recruiter_id": recruiter_id,
            "preferences": prefs,
            "behavior": behav,
            "dna": dna,
            "recruiter_embedding": r_embedding[:10], # truncate to reduce size
            "personalized_candidates": personalized_candidates,
            "recommendations": recs,
            "patterns": patterns,
            "reinforcement_q_values": q_vals,
            "explanation": explanation,
            "visualization": visual_data
        }
