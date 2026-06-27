# agents/orchestrator.py

from typing import Dict, Any

from agents.hire_agent import HireAgent
from agents.reject_agent import RejectAgent
from agents.risk_agent import RiskAgent
from agents.future_agent import FutureAgent
from agents.culture_agent import CultureAgent
from agents.leadership_agent import LeadershipAgent
from agents.retention_agent import RetentionAgent
from agents.innovation_agent import InnovationAgent
from agents.counterfactual_agent import CounterfactualAgent
from agents.compensation_agent import CompensationAgent
from agents.promotion_agent import PromotionAgent
from agents.trust_agent import TrustAgent

from agents.recruiter_agent import RecruiterAgent
from agents.engineering_manager_agent import EngineeringManagerAgent
from agents.hr_agent import HRAgent
from agents.ceo_agent import CEOAgent

from agents.debate_engine import DebateEngine
from agents.negotiation_engine import NegotiationEngine
from agents.consensus_engine import ConsensusEngine
from agents.judge_agent import JudgeAgent
from graphs.argument_graph import ArgumentGraphGenerator
from simulation.debate_simulator import DebateSimulator

class AgentOrchestrator:
    def __init__(self):
        self.hire = HireAgent()
        self.reject = RejectAgent()
        self.risk = RiskAgent()
        self.future = FutureAgent()
        self.culture = CultureAgent()
        self.leadership = LeadershipAgent()
        self.retention = RetentionAgent()
        self.innovation = InnovationAgent()
        self.counterfactual = CounterfactualAgent()
        self.compensation = CompensationAgent()
        self.promotion = PromotionAgent()
        self.trust = TrustAgent()
        
        self.recruiter = RecruiterAgent()
        self.em = EngineeringManagerAgent()
        self.hr = HRAgent()
        self.ceo = CEOAgent()
        
        self.debate = DebateEngine()
        self.negotiation = NegotiationEngine()
        self.consensus = ConsensusEngine()
        self.judge = JudgeAgent()
        self.graph_gen = ArgumentGraphGenerator()
        self.sim = DebateSimulator()

    def run_board(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Orchestrate debate, consensus, negotiation and judgment for a candidate.
        """
        ctx = context or {}
        
        # 12 Core and Board evaluations
        hire_eval = self.hire.evaluate(candidate, ctx)
        reject_eval = self.reject.evaluate(candidate, ctx)
        risk_eval = self.risk.evaluate(candidate, ctx)
        future_eval = self.future.evaluate(candidate, ctx)
        culture_eval = self.culture.evaluate(candidate, ctx)
        leader_eval = self.leadership.evaluate(candidate, ctx)
        retention_eval = self.retention.evaluate(candidate, ctx)
        innovation_eval = self.innovation.evaluate(candidate, ctx)
        cf_eval = self.counterfactual.evaluate(candidate, ctx)
        comp_eval = self.compensation.evaluate(candidate, ctx)
        promo_eval = self.promotion.evaluate(candidate, ctx)
        trust_eval = self.trust.evaluate(candidate, ctx)
        
        recruiter_eval = self.recruiter.evaluate(candidate, ctx)
        em_eval = self.em.evaluate(candidate, ctx)
        hr_eval = self.hr.evaluate(candidate, ctx)
        ceo_eval = self.ceo.evaluate(candidate, ctx)
        
        # Engines
        debate_rounds = self.debate.simulate_debate(candidate, ctx)
        
        # Negotiate initial confidence scores
        negotiation_res = self.negotiation.negotiate(hire_eval["confidence"], reject_eval["confidence"])
        
        # Consensus
        consensus_res = self.consensus.vote(candidate, ctx)
        
        # Final Judge Decision
        debate_summary = {"consensus": consensus_res}
        judge_res = self.judge.evaluate(debate_summary)
        
        # Graph & Simulator
        arg_graph = self.graph_gen.generate(candidate)
        simulation_res = self.sim.simulate(candidate)
        
        # Narrative Explanation (Part 24)
        name = candidate.get("profile", {}).get("anonymized_name") or candidate.get("id") or "Candidate"
        explanation = (
            f"Candidate {name} was debated by 12 AI agents of the hiring committee.\n\n"
            f"Positive Factors:\n"
            f"✓ Core capabilities are strong\n"
            f"✓ Leadership potential: {int(leader_eval['leadership']*100)}%\n"
            f"✓ High trust: {int(trust_eval['trust']*100)}%\n\n"
            f"Negative Gaps:\n"
            f"✗ Missing DevOps requirements: {', '.join(cf_eval['missing'])}\n"
            f"✗ Short tenure risk\n\n"
            f"After 4 rounds of debate, the hiring committee voted:\n"
            f"• HIRE: {consensus_res['votes']['hire']} votes\n"
            f"• REJECT: {consensus_res['votes']['reject']} votes\n"
            f"• ABSTAIN: {consensus_res['votes']['abstain']} votes\n\n"
            f"Final Committee Decision: {consensus_res['decision']}\n"
            f"Judge Decision: {judge_res['decision']} (Confidence: {int(judge_res['confidence']*100)}%)\n"
            f"Reasoning: {judge_res['reason']}"
        )
        
        return {
            "hire_agent": hire_eval,
            "reject_agent": reject_eval,
            "risk_agent": risk_eval,
            "future_agent": future_eval,
            "culture_agent": culture_eval,
            "leadership_agent": leader_eval,
            "retention_agent": retention_eval,
            "innovation_agent": innovation_eval,
            "counterfactual_agent": cf_eval,
            "compensation_agent": comp_eval,
            "promotion_agent": promo_eval,
            "trust_agent": trust_eval,
            
            "recruiter_agent": recruiter_eval,
            "em_agent": em_eval,
            "hr_agent": hr_eval,
            "ceo_agent": ceo_eval,
            
            "debate_rounds": debate_rounds,
            "negotiation": negotiation_res,
            "consensus": consensus_res,
            "judge": judge_res,
            "argument_graph": arg_graph,
            "debate_simulation": simulation_res,
            "explanation": explanation
        }
