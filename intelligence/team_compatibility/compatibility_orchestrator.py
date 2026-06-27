# intelligence/team_compatibility/compatibility_orchestrator.py

from typing import Dict, Any

from intelligence.team_compatibility.candidate_dna import CandidateDNABuilder
from intelligence.team_compatibility.team_dna import TeamDNABuilder
from intelligence.team_compatibility.organization_dna import OrganizationDNABuilder
from intelligence.team_compatibility.compatibility_engine import CompatibilityEngine
from intelligence.team_compatibility.communication_engine import CommunicationEngine
from intelligence.team_compatibility.collaboration_engine import CollaborationEngine
from intelligence.team_compatibility.leadership_engine import LeadershipEngine
from intelligence.team_compatibility.conflict_engine import ConflictEngine
from intelligence.team_compatibility.diversity_engine import KnowledgeDiversityEngine
from intelligence.team_compatibility.mentorship_engine import MentorshipEngine
from intelligence.team_compatibility.productivity_engine import ProductivityEngine
from intelligence.team_compatibility.innovation_engine import InnovationEngine
from intelligence.team_compatibility.burnout_engine import BurnoutEngine
from intelligence.team_compatibility.social_graph import SocialGraphEngine
from intelligence.team_compatibility.role_predictor import TeamRolePredictor
from intelligence.team_compatibility.team_simulator import TeamSimulator
from intelligence.team_compatibility.monte_carlo import TeamMonteCarloSimulator
from intelligence.team_compatibility.explainability import TeamExplainabilityLayer

class TeamCompatibilityOrchestrator:
    def __init__(self):
        self.cand_builder = CandidateDNABuilder()
        self.team_builder = TeamDNABuilder()
        self.org_builder = OrganizationDNABuilder()
        self.compat = CompatibilityEngine()
        self.comm = CommunicationEngine()
        self.collab = CollaborationEngine()
        self.lead = LeadershipEngine()
        self.conflict = ConflictEngine()
        self.diversity = KnowledgeDiversityEngine()
        self.mentor = MentorshipEngine()
        self.prod = ProductivityEngine()
        self.innov = InnovationEngine()
        self.burn = BurnoutEngine()
        self.graph = SocialGraphEngine()
        self.role = TeamRolePredictor()
        self.sim = TeamSimulator()
        self.mc = TeamMonteCarloSimulator()
        self.explainability = TeamExplainabilityLayer()

    def run_simulation(self, candidate: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Orchestrate complete candidate-team digital twin compatibility simulation.
        """
        ctx = context or {}
        
        cand_dna_res = self.cand_builder.build(candidate)
        team_dna_res = self.team_builder.build(ctx.get("team_profile"))
        org_dna_res = self.org_builder.build(ctx.get("org_profile"))
        
        compat_res = self.compat.calculate(cand_dna_res, team_dna_res, org_dna_res)
        comm_res = self.comm.evaluate(cand_dna_res, team_dna_res)
        collab_res = self.collab.evaluate(cand_dna_res, team_dna_res)
        lead_res = self.lead.evaluate(cand_dna_res, team_dna_res)
        conflict_res = self.conflict.evaluate(cand_dna_res, team_dna_res)
        diversity_res = self.diversity.evaluate(candidate, team_dna_res)
        mentor_res = self.mentor.evaluate(cand_dna_res, team_dna_res)
        prod_res = self.prod.evaluate(cand_dna_res, team_dna_res)
        innov_res = self.innov.evaluate(cand_dna_res, team_dna_res)
        burn_res = self.burn.evaluate(cand_dna_res, team_dna_res)
        graph_res = self.graph.build_graph(candidate, team_dna_res)
        role_res = self.role.predict(cand_dna_res)
        sim_res = self.sim.simulate(cand_dna_res, team_dna_res)
        
        comp_score = float(compat_res["compatibility"])
        conflict_prob = float(conflict_res["conflict_probability"])
        mc_res = self.mc.simulate(comp_score, conflict_prob)
        
        # Part 20: Organizational Impact Engine calculation yielding organization_value
        org_value = round((comp_score * 0.5 + float(prod_res["productivity_gain"]) * 2.0 + float(innov_res["innovation_boost"]) * 1.5), 2)
        
        aggregated = {
            "candidate_dna": cand_dna_res,
            "team_dna": team_dna_res,
            "org_dna": org_dna_res,
            "compatibility": compat_res,
            "communication": comm_res,
            "collaboration": collab_res,
            "leadership": lead_res,
            "conflict": conflict_res,
            "diversity": diversity_res,
            "mentorship": mentor_res,
            "productivity": prod_res,
            "innovation": innov_res,
            "burnout": burn_res,
            "social_graph": graph_res,
            "role": role_res,
            "simulation": sim_res,
            "monte_carlo": mc_res,
            "org_impact": {
                "organization_value": min(0.99, org_value)
            }
        }
        
        explanation = self.explainability.generate(aggregated, candidate)
        aggregated["explanation"] = explanation
        
        return aggregated
