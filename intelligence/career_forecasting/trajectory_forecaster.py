# intelligence/career_forecasting/trajectory_forecaster.py

import random
from typing import Dict, Any

from intelligence.career_forecasting.career_graph import CareerGraph
from intelligence.career_forecasting.career_velocity import CareerVelocityEngine
from intelligence.career_forecasting.future_role_predictor import FutureRolePredictor
from intelligence.career_forecasting.promotion_predictor import PromotionPredictor
from intelligence.career_forecasting.leadership_predictor import LeadershipPredictor
from intelligence.career_forecasting.skill_predictor import SkillPredictor
from intelligence.career_forecasting.role_predictor import RoleBranchPredictor
from intelligence.career_forecasting.salary_predictor import SalaryProgressionPredictor
from intelligence.career_forecasting.ceiling_predictor import CareerCeilingPredictor
from intelligence.career_forecasting.executive_predictor import ExecutivePotentialPredictor
from intelligence.career_forecasting.founder_predictor import FounderPredictor
from intelligence.career_forecasting.plateau_detector import CareerPlateauDetector
from intelligence.career_forecasting.risk_predictor import CareerRiskPredictor
from intelligence.career_forecasting.timeline_generator import CareerTimelineGenerator
from intelligence.career_forecasting.career_simulator import CareerSimulator
from intelligence.career_forecasting.human_capital_value import HumanCapitalValuator
from intelligence.career_forecasting.explainability import CareerExplainabilityLayer

class CareerTrajectoryForecastingEngine:
    def __init__(self):
        self.graph = CareerGraph()
        self.velocity = CareerVelocityEngine()
        self.future_role = FutureRolePredictor()
        self.promotion = PromotionPredictor()
        self.leadership = LeadershipPredictor()
        self.skills = SkillPredictor()
        self.branches = RoleBranchPredictor()
        self.salary = SalaryProgressionPredictor()
        self.ceiling = CareerCeilingPredictor()
        self.executive = ExecutivePotentialPredictor()
        self.founder = FounderPredictor()
        self.plateau = CareerPlateauDetector()
        self.risk = CareerRiskPredictor()
        self.timeline = CareerTimelineGenerator()
        self.simulator = CareerSimulator()
        self.value = HumanCapitalValuator()
        self.explainability = CareerExplainabilityLayer()

    def run_forecasts(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run all career intelligence predictions for a candidate.
        """
        ctx = context or {}
        
        velocity_res = self.velocity.calculate(candidate, ctx)
        future_role_res = self.future_role.predict(candidate, ctx)
        promotion_res = self.promotion.predict(candidate, ctx)
        leadership_res = self.leadership.predict(candidate, ctx)
        skills_res = self.skills.predict(candidate, ctx)
        branches_res = self.branches.predict(candidate, ctx)
        salary_res = self.salary.predict(candidate, ctx)
        ceiling_res = self.ceiling.predict(candidate, ctx)
        executive_res = self.executive.predict(candidate, ctx)
        founder_res = self.founder.predict(candidate, ctx)
        plateau_res = self.plateau.predict(candidate, ctx)
        risk_res = self.risk.predict(candidate, ctx)
        timeline_res = self.timeline.generate(candidate, ctx)
        simulator_res = self.simulator.simulate(candidate, ctx)
        value_res = self.value.calculate(candidate, ctx)
        
        # Monte Carlo Simulation (Part 18): 10,000 iterations to predict final ceiling roles
        score = float(candidate.get("score") or 85.0)
        base_exec = float(executive_res["executive_probability"])
        base_founder = float(founder_res["founder_probability"])
        
        manager_sims = 0
        director_sims = 0
        cto_sims = 0
        founder_sims = 0
        
        for _ in range(10000):
            val = random.random()
            if val < base_founder * 0.15:
                founder_sims += 1
            elif val < base_exec * 0.25:
                cto_sims += 1
            elif val < base_exec * 0.60:
                director_sims += 1
            else:
                manager_sims += 1
                
        monte_carlo_res = {
            "manager": int(round((manager_sims / 10000) * 100)),
            "director": int(round((director_sims / 10000) * 100)),
            "cto": int(round((cto_sims / 10000) * 100)),
            "founder": int(round((founder_sims / 10000) * 100))
        }
        
        aggregated = {
            "velocity": velocity_res,
            "future_role": future_role_res,
            "promotion": promotion_res,
            "leadership": leadership_res,
            "skills": skills_res,
            "branches": branches_res,
            "salary": salary_res,
            "ceiling": ceiling_res,
            "executive": executive_res,
            "founder": founder_res,
            "plateau": plateau_res,
            "risk": risk_res,
            "timeline": timeline_res,
            "simulator": simulator_res,
            "value": value_res,
            "monte_carlo": monte_carlo_res
        }
        
        explanation = self.explainability.generate(aggregated, candidate)
        aggregated["explanation"] = explanation
        
        return aggregated
