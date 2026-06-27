# intelligence/optimizer/__init__.py

from typing import Dict, List, Any

from .objective_engine import ObjectiveEngine
from .constraint_engine import ConstraintEngine
from .pareto_engine import ParetoEngine
from .nsga2_optimizer import NSGA2Optimizer
from .genetic_optimizer import GeneticOptimizer
from .monte_carlo_engine import MonteCarloOptimizerEngine
from .scenario_optimizer import ScenarioOptimizer
from .salary_optimizer import SalaryOptimizer
from .retention_optimizer import RetentionOptimizer
from .joining_optimizer import JoiningOptimizer
from .diversity_optimizer import DiversityOptimizer
from .learning_optimizer import LearningOptimizer
from .future_value_optimizer import FutureValueOptimizer
from .team_optimizer import TeamOptimizer
from .organization_optimizer import OrganizationOptimizer
from .risk_optimizer import RiskOptimizer
from .tradeoff_analyzer import TradeoffAnalyzer
from .sensitivity_analyzer import SensitivityAnalyzer
from .decision_engine import DecisionEngine
from .explainability_engine import ExplainabilityEngine
from .visualization_engine import VisualizationEngine

class MultiObjectiveHiringOptimizer:
    def __init__(self):
        self.objective = ObjectiveEngine()
        self.constraint = ConstraintEngine()
        self.pareto = ParetoEngine()
        self.nsga2 = NSGA2Optimizer()
        self.genetic = GeneticOptimizer()
        self.mc = MonteCarloOptimizerEngine()
        self.scenario = ScenarioOptimizer()
        self.salary = SalaryOptimizer()
        self.retention = RetentionOptimizer()
        self.joining = JoiningOptimizer()
        self.diversity = DiversityOptimizer()
        self.learning = LearningOptimizer()
        self.future_value = FutureValueOptimizer()
        self.team = TeamOptimizer()
        self.organization = OrganizationOptimizer()
        self.risk = RiskOptimizer()
        self.tradeoff = TradeoffAnalyzer()
        self.sensitivity = SensitivityAnalyzer()
        self.decision = DecisionEngine()
        self.explain = ExplainabilityEngine()
        self.visual = VisualizationEngine()

    def run_optimization(
        self,
        candidates: List[Dict[str, Any]],
        constraints: Dict[str, Any] = None,
        strategy: str = "future_growth",
        scenario_id: str = "startup"
    ) -> Dict[str, Any]:
        """
        Executes the full MOHO optimization pipeline over a candidate pool.
        """
        if not candidates:
            return {}
            
        if constraints is None:
            constraints = {
                "salary_max": 45.0,
                "joining_max": 90.0,
                "experience_min": 2.0,
                "required_skills": []
            }
            
        # 1. Feature Extraction & Objectives Calculation
        processed_candidates = []
        for cand in candidates:
            objs = self.objective.calculate_objectives(cand)
            checks = self.constraint.evaluate_constraints(cand, constraints)
            
            # Merge into candidate copy
            c_copy = cand.copy()
            c_copy["objectives"] = objs
            c_copy["constraints_eval"] = checks
            processed_candidates.append(c_copy)
            
        # Filter eligible candidates
        eligible_candidates = [c for c in processed_candidates if c["constraints_eval"]["eligible"]]
        if not eligible_candidates:
            # Fallback to all if constraint matches are empty
            eligible_candidates = processed_candidates
            
        # 2. Pareto Frontier & NSGA-II
        objectives_list = ["quality", "salary", "joining", "retention", "future"]
        maximize_flags = [True, False, False, True, True]
        
        frontier = self.pareto.find_pareto_frontier(eligible_candidates, objectives_list, maximize_flags)
        frontier_with_crowding = self.pareto.calculate_crowding_distance(frontier, objectives_list)
        
        nsga2_optimal = self.nsga2.optimize(eligible_candidates, objectives_list, maximize_flags)
        
        # 3. Specific Sub-Optimizations
        salary_roi = self.salary.optimize_salary(eligible_candidates)
        joining_ranks = self.joining.optimize_joining(eligible_candidates)
        future_forecast = self.future_value.optimize_future_value(eligible_candidates)
        
        # 4. Decision & Recommendation
        rec = self.decision.recommend_decision(eligible_candidates, strategy)
        
        # Selected candidate sub-runs
        selected_cand = next((c for c in eligible_candidates if c.get("candidate_id") == rec.get("candidate_id")), eligible_candidates[0])
        
        ret_forecast = self.retention.optimize_retention(selected_cand)
        learn_forecast = self.learning.optimize_learning(selected_cand)
        team_forecast = self.team.optimize_team(selected_cand)
        org_forecast = self.organization.optimize_organization(selected_cand)
        risk_forecast = self.risk.optimize_risk(selected_cand)
        diversity_forecast = self.diversity.optimize_diversity(selected_cand, candidates[:5])
        
        # 5. Tradeoff & Sensitivity Analysers
        tradeoffs = self.tradeoff.analyze_tradeoffs(eligible_candidates)
        sensitivities = self.sensitivity.analyze_sensitivity(eligible_candidates, objectives_list)
        
        # 6. Scenario Mode Recommended Pick
        scenario_res = self.scenario.run_scenario(eligible_candidates, scenario_id)
        
        # 7. Monte Carlo strategy run
        mc_res = self.mc.simulate_workforce(eligible_candidates)
        
        # 8. Explainability & Visualization formatter
        explanation = self.explain.explain_selection(selected_cand.get("name"), selected_cand["objectives"], tradeoffs)
        visual_data = self.visual.format_visualization_data(frontier_with_crowding, eligible_candidates)
        
        return {
            "optimal_strategy": strategy,
            "recommended_candidate": rec,
            "pareto_frontier": frontier_with_crowding[:10],
            "nsga2_frontier": nsga2_optimal[:10],
            "salary_roi": salary_roi,
            "joining": joining_ranks,
            "future_forecast": future_forecast,
            "retention": ret_forecast,
            "learning": learn_forecast,
            "team": team_forecast,
            "organization": org_forecast,
            "risk": risk_forecast,
            "diversity": diversity_forecast,
            "tradeoffs": tradeoffs,
            "sensitivity": sensitivities,
            "scenario_results": scenario_res,
            "monte_carlo": mc_res,
            "explanation": explanation,
            "visualization": visual_data
        }
