# intelligence/digital_twin/twin_generator.py

from typing import Dict, Any
from intelligence.learning_velocity import LearningVelocityEngine
from intelligence.career_simulator import CareerSimulator
from intelligence.skill_evolution import SkillEvolutionPredictor
from intelligence.promotion_engine import PromotionEngine
from intelligence.retention_engine import RetentionEngine
from intelligence.burnout_engine import BurnoutEngine
from intelligence.organization_dna import OrganizationDNA
from intelligence.leadership_engine import LeadershipEngine
from intelligence.counterfactual_engine import CounterfactualEngine
from intelligence.future_simulator import FutureSimulator

class DigitalTwinGenerator:
    def __init__(self):
        self.learning_engine = LearningVelocityEngine()
        self.career_sim = CareerSimulator()
        self.skill_evo = SkillEvolutionPredictor()
        self.promotion_engine = PromotionEngine()
        self.retention_engine = RetentionEngine()
        self.burnout_engine = BurnoutEngine()
        self.org_dna = OrganizationDNA()
        self.leadership_engine = LeadershipEngine()
        self.counterfactual_engine = CounterfactualEngine()
        self.future_sim = FutureSimulator()

    def generate(self, candidate: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinates the execution of all ten intelligence engines to assemble
        a comprehensive Digital Twin simulation.
        """
        learn_results = self.learning_engine.calculate(candidate)
        learn_vel = learn_results["learning_velocity"]
        
        career_results = self.career_sim.simulate(candidate)
        skill_results = self.skill_evo.predict(candidate, learn_vel)
        
        promo_results = self.promotion_engine.calculate(candidate, career_results, learn_vel)
        retention_results = self.retention_engine.calculate(candidate, career_results)
        
        burnout_results = self.burnout_engine.calculate(candidate, learn_vel, career_results, retention_results)
        dna_results = self.org_dna.match(candidate, learn_vel, career_results, "corporate")
        
        lead_results = self.leadership_engine.predict(candidate, career_results, learn_vel)
        counter_results = self.counterfactual_engine.explain(candidate, jd_data)
        timeline_results = self.future_sim.simulate(career_results, promo_results)
        
        return {
            "learning_velocity": learn_results["learning_velocity"],
            "learning_type": learn_results["learning_type"],
            "future_learning_capacity": learn_results["future_learning_capacity"],
            "learning_consistency": learn_results["learning_consistency"],
            "learning_diversity": learn_results["learning_diversity"],
            "learning_acceleration": learn_results["learning_acceleration"],
            
            "career_acceleration": career_results["career_acceleration"],
            "career_momentum": career_results["career_momentum"],
            "growth_speed": career_results["growth_speed"],
            "predicted_role": career_results["predicted_role"],
            "current_level": career_results["current_level"],
            
            "skill_evolution": skill_results,
            
            "promotion_probability": promo_results["promotion_probability"],
            "next_role": promo_results["next_role"],
            "promotion_time": promo_results["promotion_time"],
            
            "retention_probability": retention_results["retention_probability"],
            "attrition_risk": retention_results["attrition_risk"],
            "avg_tenure_years": retention_results["avg_tenure_years"],
            "job_hopper_flag": retention_results["job_hopper_flag"],
            
            "burnout_probability": burnout_results["burnout_probability"],
            "burnout_risk": burnout_results["risk"],
            "career_stress": burnout_results["career_stress"],
            
            "culture_fit": dna_results["culture_fit"],
            "work_style": dna_results["work_style"],
            "candidate_dna": dna_results["candidate_dna"],
            
            "leadership_potential": lead_results["current"],
            "leadership_evolution": lead_results,
            
            "counterfactual": counter_results,
            "timeline": timeline_results
        }
