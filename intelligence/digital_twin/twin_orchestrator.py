# intelligence/digital_twin/twin_orchestrator.py

from typing import Dict, Any

from intelligence.digital_twin.candidate_dna import CandidateDnaEngine
from intelligence.digital_twin.behavioral_engine import BehavioralProfileEngine
from intelligence.digital_twin.personality_engine import PersonalityEngine
from intelligence.digital_twin.learning_engine import LearningEngine
from intelligence.digital_twin.skill_evolution import SkillEvolution
from intelligence.digital_twin.career_forecast import CareerForecastEngine
from intelligence.digital_twin.leadership_forecast import LeadershipForecastEngine
from intelligence.digital_twin.retention_engine import RetentionEngine
from intelligence.digital_twin.resignation_engine import ResignationEngine
from intelligence.digital_twin.burnout_engine import BurnoutEngine
from intelligence.digital_twin.promotion_engine import PromotionEngine
from intelligence.digital_twin.innovation_engine import InnovationEngine
from intelligence.digital_twin.productivity_engine import ProductivityEngine
from intelligence.digital_twin.mentorship_engine import MentorshipEngine
from intelligence.digital_twin.team_impact import TeamImpactEngine
from intelligence.digital_twin.organization_impact import OrganizationImpactEngine
from intelligence.digital_twin.digital_twin_builder import DigitalTwinBuilder
from intelligence.digital_twin.simulation_engine import FutureSimulationEngine
from intelligence.digital_twin.monte_carlo import MonteCarloSimulator
from intelligence.digital_twin.explainability import ExplainabilityEngine

class TalentTwinOrchestrator:
    def __init__(self):
        self.dna = CandidateDnaEngine()
        self.behavior = BehavioralProfileEngine()
        self.personality = PersonalityEngine()
        self.learning = LearningEngine()
        self.skills = SkillEvolution()
        self.career = CareerForecastEngine()
        self.leadership = LeadershipForecastEngine()
        self.retention = RetentionEngine()
        self.resignation = ResignationEngine()
        self.burnout = BurnoutEngine()
        self.promotion = PromotionEngine()
        self.innovation = InnovationEngine()
        self.productivity = ProductivityEngine()
        self.mentorship = MentorshipEngine()
        self.team_impact = TeamImpactEngine()
        self.org_impact = OrganizationImpactEngine()
        self.builder = DigitalTwinBuilder()
        self.simulation = FutureSimulationEngine()
        self.mc = MonteCarloSimulator()
        self.explainability = ExplainabilityEngine()

    def run_twin(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run the complete Digital Twin Simulation pipeline.
        """
        cand_dna = self.dna.extract_dna(candidate)
        behavior_res = self.behavior.predict_profile(candidate)
        personality_res = self.personality.estimate_traits(candidate)
        learning_res = self.learning.predict(candidate)
        skills_res = self.skills.calculate(candidate)
        career_res = self.career.predict_career(candidate)
        leadership_res = self.leadership.predict_leadership(candidate)
        retention_res = self.retention.predict_retention(candidate)
        resignation_res = self.resignation.predict_resignation(candidate)
        burnout_res = self.burnout.predict_burnout(candidate)
        promotion_res = self.promotion.predict_promotion(candidate)
        innovation_res = self.innovation.predict_innovation(candidate)
        productivity_res = self.productivity.predict_productivity(candidate)
        mentorship_res = self.mentorship.predict_mentorship(candidate)
        team_res = self.team_impact.predict_impact(candidate)
        org_res = self.org_impact.predict_value(candidate)
        
        score_val = float(candidate.get("score", 85))
        mc_res = self.mc.simulate(score_val)
        sim_res = self.simulation.simulate(candidate)
        
        aggregated = {
            "dna": cand_dna,
            "behavior": behavior_res,
            "personality": personality_res,
            "learning": learning_res,
            "skills": skills_res,
            "career": career_res,
            "leadership": leadership_res,
            "retention": retention_res,
            "resignation": resignation_res,
            "burnout": burnout_res,
            "promotion": promotion_res,
            "innovation": innovation_res,
            "productivity": productivity_res,
            "mentorship": mentorship_res,
            "team_impact": team_res,
            "organization_impact": org_res,
            "simulation": sim_res,
            "monte_carlo": mc_res
        }
        
        twin_profile = self.builder.build_twin(candidate.get("candidate_id", "1"), aggregated)
        aggregated["twin_profile"] = twin_profile
        
        explanation = self.explainability.generate(aggregated, candidate)
        aggregated["explanation"] = explanation
        
        return aggregated
