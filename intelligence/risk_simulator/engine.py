# intelligence/risk_simulator/engine.py

from typing import Dict, Any

from intelligence.risk_simulator.offer_acceptance import OfferAcceptancePredictor
from intelligence.risk_simulator.ghosting_predictor import GhostingPredictor
from intelligence.risk_simulator.joining_predictor import JoiningPredictor
from intelligence.risk_simulator.retention_predictor import RetentionPredictor
from intelligence.risk_simulator.resignation_predictor import ResignationPredictor
from intelligence.risk_simulator.switch_predictor import SwitchPredictor
from intelligence.risk_simulator.burnout_predictor import BurnoutPredictor
from intelligence.risk_simulator.promotion_predictor import PromotionPredictor
from intelligence.risk_simulator.leadership_predictor import LeadershipPredictor
from intelligence.risk_simulator.teamlead_predictor import TeamLeadPredictor
from intelligence.risk_simulator.manager_predictor import ManagerPredictor
from intelligence.risk_simulator.director_predictor import DirectorPredictor
from intelligence.risk_simulator.salary_predictor import SalaryPredictor
from intelligence.risk_simulator.conflict_predictor import ConflictPredictor
from intelligence.risk_simulator.survival_predictor import SurvivalPredictor
from intelligence.risk_simulator.future_success_predictor import FutureSuccessPredictor

from simulation.career_simulator import CareerSimulator
from simulation.monte_carlo_hiring import MonteCarloHiringSimulator
from ranking.risk_score import RiskScorer
from explainability.risk_explain import RiskExplainabilityEngine


class HiringRiskSimulatorEngine:
    def __init__(self):
        self.offer_acc = OfferAcceptancePredictor()
        self.ghosting = GhostingPredictor()
        self.joining = JoiningPredictor()
        self.retention = RetentionPredictor()
        self.resignation = ResignationPredictor()
        self.switch = SwitchPredictor()
        self.burnout = BurnoutPredictor()
        self.promotion = PromotionPredictor()
        self.leadership = LeadershipPredictor()
        self.teamlead = TeamLeadPredictor()
        self.manager = ManagerPredictor()
        self.director = DirectorPredictor()
        self.salary = SalaryPredictor()
        self.conflict = ConflictPredictor()
        self.survival = SurvivalPredictor()
        self.success = FutureSuccessPredictor()
        
        self.career_sim = CareerSimulator()
        self.mc_hiring = MonteCarloHiringSimulator()
        self.scorer = RiskScorer()
        self.explainer = RiskExplainabilityEngine()

    def run_simulation(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Orchestrates the entire risk and outcome prediction analysis for a candidate.
        """
        ctx = context or {}
        
        # Predict all probability metrics
        oa_res = self.offer_acc.predict(candidate, ctx)
        gh_res = self.ghosting.predict(candidate, ctx)
        jn_res = self.joining.predict(candidate, ctx)
        rt_res = self.retention.predict(candidate, ctx)
        rs_res = self.resignation.predict(candidate, ctx)
        sw_res = self.switch.predict(candidate, ctx)
        bo_res = self.burnout.predict(candidate, ctx)
        pr_res = self.promotion.predict(candidate, ctx)
        ld_res = self.leadership.predict(candidate, ctx)
        tl_res = self.teamlead.predict(candidate, ctx)
        mn_res = self.manager.predict(candidate, ctx)
        dr_res = self.director.predict(candidate, ctx)
        sl_res = self.salary.predict(candidate, ctx)
        cf_res = self.conflict.predict(candidate, ctx)
        sv_res = self.survival.predict(candidate, ctx)
        sc_res = self.success.predict(candidate, ctx)
        
        # Simulators
        career_res = self.career_sim.simulate(candidate)
        mc_res = self.mc_hiring.simulate(candidate)
        
        # Scoring
        metrics_payload = {
            "accept_probability": oa_res.get("accept_probability", 0.9),
            "joining_probability": jn_res.get("joining_probability", 0.8),
            "retention_12": rt_res.get("12_months", 0.8),
            "promotion_probability": pr_res.get("promotion_probability", 0.8),
            "future_leader": ld_res.get("future_leader", 0.7),
            "success_probability": sc_res.get("success_probability", 0.8),
            "burnout_probability": bo_res.get("burnout_probability", 0.2),
            "resignation_probability": rs_res.get("resignation_probability", 0.2),
            "switch_probability": sw_res.get("switch_probability", 0.2),
            "conflict_probability": cf_res.get("conflict_probability", 0.1),
            "survival_probability": sv_res.get("survival_probability", 0.8)
        }
        risk_score_value = self.scorer.calculate(metrics_payload)
        
        # Explanation
        explain_payload = {
            "expected_month": rs_res.get("expected_month", 36),
            "accept_probability": oa_res.get("accept_probability", 0.91),
            "ghosting_probability": gh_res.get("ghost_probability", 0.04),
            "joining_probability": jn_res.get("joining_probability", 0.87),
            "retention_12": rt_res.get("12_months", 0.92),
            "promotion_probability": pr_res.get("promotion_probability", 0.84),
            "future_leader": ld_res.get("future_leader", 0.81),
            "burnout_probability": bo_res.get("burnout_probability", 0.09),
            "resignation_probability": rs_res.get("resignation_probability", 0.12),
            "teamlead_probability": tl_res.get("teamlead_probability", 0.79),
            "manager_probability": mn_res.get("manager_probability", 0.71),
            "success_probability": sc_res.get("success_probability", 0.90)
        }
        explanation_text = self.explainer.explain(candidate.get("name", "Candidate"), explain_payload)
        
        return {
            "risk_score": risk_score_value,
            "offer_acceptance": oa_res,
            "ghosting": gh_res,
            "joining": jn_res,
            "retention": rt_res,
            "resignation": rs_res,
            "switch": sw_res,
            "burnout": bo_res,
            "promotion": pr_res,
            "leadership": ld_res,
            "teamlead": tl_res,
            "manager": mn_res,
            "director": dr_res,
            "salary": sl_res,
            "conflict": cf_res,
            "survival": sv_res,
            "success": sc_res,
            "career_timeline": career_res,
            "monte_carlo_hiring": mc_res,
            "explanation": explanation_text
        }
