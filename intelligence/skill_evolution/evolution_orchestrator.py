# intelligence/skill_evolution/evolution_orchestrator.py

from typing import Dict, Any

from intelligence.skill_evolution.skill_extractor import SkillExtractor
from intelligence.skill_evolution.timeline_builder import SkillTimelineBuilder
from intelligence.skill_evolution.learning_velocity import LearningVelocityEngine
from intelligence.skill_evolution.project_velocity import ProjectVelocityEngine
from intelligence.skill_evolution.github_engine import GitHubIntelligenceEngine
from intelligence.skill_evolution.certification_engine import CertificationEngine
from intelligence.skill_evolution.knowledge_graph import SkillKnowledgeGraph
from intelligence.skill_evolution.dependency_graph import SkillDependencyEngine
from intelligence.skill_evolution.skill_growth import SkillGrowthEngine
from intelligence.skill_evolution.future_skill_predictor import FutureSkillPredictor
from intelligence.skill_evolution.obsolescence_engine import SkillObsolescenceEngine
from intelligence.skill_evolution.specialization_engine import SpecializationEngine
from intelligence.skill_evolution.leadership_growth import LeadershipGrowthEngine
from intelligence.skill_evolution.career_evolution import CareerEvolutionEngine
from intelligence.skill_evolution.digital_twin import SkillDigitalTwin
from intelligence.skill_evolution.monte_carlo import SkillMonteCarloSimulator
from intelligence.skill_evolution.human_potential import HumanPotentialEngine
from intelligence.skill_evolution.explainability import SkillExplainabilityLayer

class SkillEvolutionOrchestrator:
    def __init__(self):
        self.extractor = SkillExtractor()
        self.timeline = SkillTimelineBuilder()
        self.velocity = LearningVelocityEngine()
        self.proj_velocity = ProjectVelocityEngine()
        self.github = GitHubIntelligenceEngine()
        self.cert = CertificationEngine()
        self.kg = SkillKnowledgeGraph()
        self.dep = SkillDependencyEngine()
        self.growth = SkillGrowthEngine()
        self.future = FutureSkillPredictor()
        self.obsolescence = SkillObsolescenceEngine()
        self.specialization = SpecializationEngine()
        self.leadership = LeadershipGrowthEngine()
        self.career = CareerEvolutionEngine()
        self.twin = SkillDigitalTwin()
        self.mc = SkillMonteCarloSimulator()
        self.potential = HumanPotentialEngine()
        self.explainability = SkillExplainabilityLayer()

    def run_forecasting(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Orchestrate complete skill growth & human potential prediction pipeline.
        """
        extracted_skills = self.extractor.extract_skills(candidate)
        timeline_data = self.timeline.build_timeline(candidate)
        vel_res = self.velocity.calculate(timeline_data)
        proj_vel_res = self.proj_velocity.calculate(candidate)
        git_res = self.github.analyze(candidate)
        cert_res = self.cert.predict_path(candidate)
        dep_res = self.dep.predict_next_skill(candidate)
        
        velocity_val = float(vel_res["learning_velocity"])
        growth_res = self.growth.calculate_growth(extracted_skills, velocity_val)
        
        future_skills = self.future.predict_future_skills(candidate)
        strengths_res = self.future.forecast_strengths(extracted_skills)
        
        obs_res = self.obsolescence.predict_obsolescence(candidate)
        spec_res = self.specialization.predict_specialization(candidate)
        lead_res = self.leadership.predict_growth(candidate)
        career_res = self.career.predict_evolution(candidate)
        twin_res = self.twin.simulate_scenarios(candidate)
        
        score_val = float(candidate.get("score", 85))
        mc_res = self.mc.simulate(score_val)
        
        potential_res = self.potential.calculate(candidate, velocity_val)
        
        aggregated = {
            "skills": extracted_skills,
            "timeline": timeline_data,
            "velocity": vel_res,
            "project_velocity": proj_vel_res,
            "github": git_res,
            "certification": cert_res,
            "dependency": dep_res,
            "growth": growth_res,
            "future_skills": future_skills,
            "strengths": strengths_res,
            "obsolescence": obs_res,
            "specialization": spec_res,
            "leadership": lead_res,
            "career": career_res,
            "twin": twin_res,
            "monte_carlo": mc_res,
            "potential": potential_res,
            "confidence": 88
        }
        
        explanation = self.explainability.generate(aggregated, candidate)
        aggregated["explanation"] = explanation
        
        return aggregated
