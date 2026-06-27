# intelligence/counterfactual_engine.py

from typing import Dict, List, Any
import random

from intelligence.gap_analyzer import GapAnalyzer
from intelligence.perturbation_engine import PerturbationEngine
from simulation.monte_carlo import MonteCarloSimulator
from optimization.path_optimizer import PathOptimizer
from counterfactual.skill_counterfactual import SkillCounterfactual
from counterfactual.experience_counterfactual import ExperienceCounterfactual
from counterfactual.project_counterfactual import ProjectCounterfactual
from counterfactual.leadership_counterfactual import LeadershipCounterfactual
from counterfactual.career_counterfactual import CareerCounterfactual
from counterfactual.salary_counterfactual import SalaryCounterfactual
from counterfactual.retention_counterfactual import RetentionCounterfactual
from counterfactual.culture_counterfactual import CultureCounterfactual
from counterfactual.future_counterfactual import FutureCounterfactual
from intelligence.difficulty_engine import DifficultyEngine
from intelligence.cost_engine import CostEngine
from intelligence.probability_engine import ProbabilityEngine
from agents.debate_engine import DebateEngine
from ranking.counterfactual_score import CounterfactualScorer
from explainability.counterfactual_explain import CounterfactualExplainabilityEngine


class CounterfactualEngine:
    def __init__(self):
        self.gap_analyzer = GapAnalyzer()
        self.perturbation = PerturbationEngine()
        self.monte_carlo = MonteCarloSimulator()
        self.optimizer = PathOptimizer()
        self.skill_cf = SkillCounterfactual()
        self.exp_cf = ExperienceCounterfactual()
        self.proj_cf = ProjectCounterfactual()
        self.lead_cf = LeadershipCounterfactual()
        self.career_cf = CareerCounterfactual()
        self.salary_cf = SalaryCounterfactual()
        self.retention_cf = RetentionCounterfactual()
        self.culture_cf = CultureCounterfactual()
        self.future_cf = FutureCounterfactual()
        self.difficulty_eng = DifficultyEngine()
        self.cost_eng = CostEngine()
        self.prob_eng = ProbabilityEngine()
        self.debate_eng = DebateEngine()
        self.scorer = CounterfactualScorer()
        self.explainer = CounterfactualExplainabilityEngine()

    def run_all(self, candidate: Dict[str, Any], job: Dict[str, Any], current_score: float = 85.0, target_rank: int = 1) -> Dict[str, Any]:
        """
        Run the complete counterfactual assessment pipeline for a candidate.
        """
        # 1. Gap Analysis
        gaps = self.gap_analyzer.analyze(candidate, job)
        
        # 2. Perturbation Scenarios
        scenarios = self.perturbation.generate_scenarios(gaps)
        
        # 3. Monte Carlo Simulation
        mc_results = self.monte_carlo.simulate(current_score, scenarios)
        
        # 4. Optimal Path Search
        paths = self.optimizer.optimize(scenarios)
        optimal_scenario = paths.get("highest_roi") or paths.get("maximum_score")
        
        # 5. Core Counterfactual Engines
        skill_res = self.skill_cf.evaluate(gaps)
        exp_res = self.exp_cf.evaluate(gaps, current_score)
        proj_res = self.proj_cf.evaluate(gaps)
        lead_res = self.lead_cf.evaluate(candidate)
        career_res = self.career_cf.evaluate(candidate)
        
        # Extract skills to learn
        skills_to_learn = skill_res.get("required_skills", ["Kubernetes", "Terraform"])
        salary_res = self.salary_cf.evaluate(skills_to_learn)
        retention_res = self.retention_cf.evaluate(candidate)
        culture_res = self.culture_cf.evaluate(candidate)
        
        # 6. Timeline Projection
        future_res = self.future_cf.evaluate(current_score, optimal_scenario.get("score_gain", 10))
        
        # 7. Difficulty, Cost & Success Probability
        base_improvements = []
        for s in skills_to_learn:
            base_improvements.append({"type": "skill", "name": s})
        for p in proj_res.get("required_projects", []):
            base_improvements.append({"type": "project", "name": p})
            
        cost_res = self.cost_eng.estimate(base_improvements)
        prob_res = self.prob_eng.calculate(candidate, base_improvements)
        
        difficulty_mapping = {s: self.difficulty_eng.classify(s) for s in skills_to_learn}
        
        # 8. Debate Engine Simulation
        debate_res = self.debate_eng.simulate_debate(candidate, gaps, mc_results.get("best_score", 98))
        
        # 9. Scorer calculation
        composite_score = self.scorer.calculate({
            "current_score": current_score,
            "future_score": mc_results.get("best_score", 98),
            "cost_numeric": cost_res.get("cost_numeric", 15000),
            "months_numeric": cost_res.get("months_numeric", 6),
            "success_probability": prob_res.get("success_probability", 0.85),
            "leadership_growth": lead_res.get("future_leadership", 0.8)
        })
        
        # 10. Generate Explanations
        explain_payload = {
            "name": candidate.get("name", "Candidate"),
            "current_rank": candidate.get("rank", 2),
            "current_score": current_score,
            "potential_score": mc_results.get("best_score", 98),
            "missing_skills": skills_to_learn,
            "cost": cost_res.get("cost", "₹15,000"),
            "months": cost_res.get("months", 6),
            "success_probability": prob_res.get("success_probability", 0.87),
            "future_role": career_res.get("best_path", "Senior DevOps Architect")
        }
        explanation_text = self.explainer.explain(explain_payload)
        
        # Format the master required changes response
        required_changes = []
        for s in skills_to_learn:
            required_changes.append({
                "type": "skill",
                "name": s,
                "difficulty": difficulty_mapping.get(s, "Medium"),
                "score_gain": 5 if s.lower() in ["kubernetes", "docker", "fastapi"] else 3
            })
        for p in proj_res.get("required_projects", []):
            required_changes.append({
                "type": "project",
                "name": p,
                "difficulty": "Hard",
                "score_gain": 6
            })
            
        return {
            "current_rank": candidate.get("rank", 2),
            "future_rank": target_rank,
            "required_changes": required_changes,
            "probability": prob_res.get("success_probability", 0.87),
            "composite_score": composite_score,
            "gap_analysis": gaps,
            "monte_carlo": mc_results,
            "optimal_paths": paths,
            "skills_counterfactual": skill_res,
            "experience_counterfactual": exp_res,
            "project_counterfactual": proj_res,
            "leadership_counterfactual": lead_res,
            "career_counterfactual": career_res,
            "salary_counterfactual": salary_res,
            "retention_counterfactual": retention_res,
            "culture_counterfactual": culture_res,
            "future_counterfactual": future_res,
            "cost_estimation": cost_res,
            "debate": debate_res,
            "explanation": explanation_text
        }

    def explain(self, candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy compatibility wrapper for test suites."""
        res = self.run_all(candidate, job)
        return {
            "missing_skills": res.get("gap_analysis", {}).get("missing_skills", []),
            "missing_experience": res.get("gap_analysis", {}).get("missing_experience", 0.0),
            "predicted_rank_after_changes": res.get("future_rank", 1)
        }

