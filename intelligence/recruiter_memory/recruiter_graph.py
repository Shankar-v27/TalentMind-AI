# intelligence/recruiter_memory/recruiter_graph.py

import networkx as nx
from typing import Dict, List, Any

class RecruiterKnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_recruiter_nodes(
        self,
        recruiter_id: str,
        actions: List[Dict[str, Any]],
        candidates_map: Dict[str, Dict[str, Any]]
    ):
        """
        Populates nodes and edges for the recruiter based on candidate interaction history.
        """
        # Ensure recruiter node exists
        self.graph.add_node(recruiter_id, type="recruiter")
        
        for act in actions:
            cand_id = act["candidate_id"]
            action_type = act["action"]
            
            # Add candidate node
            cand_info = candidates_map.get(cand_id, {})
            cand_name = cand_info.get("name", cand_id)
            self.graph.add_node(cand_id, type="candidate", name=cand_name)
            
            # Add interaction edge
            self.graph.add_edge(recruiter_id, cand_id, relation=action_type, weight=1.0)
            
            # Connect skills, domains, and companies from candidate profile
            skills = cand_info.get("skills", [])
            for sk in skills:
                sk_name = sk.get("name", "") if isinstance(sk, dict) else sk
                if sk_name:
                    self.graph.add_node(sk_name.lower(), type="skill")
                    self.graph.add_edge(cand_id, sk_name.lower(), relation="has_skill")
                    # Direct virtual preference connection
                    weight_mod = 1.5 if action_type in ["hired", "shortlisted"] else 0.5
                    if self.graph.has_edge(recruiter_id, sk_name.lower()):
                        self.graph[recruiter_id][sk_name.lower()]["weight"] += weight_mod
                    else:
                        self.graph.add_edge(recruiter_id, sk_name.lower(), relation="prefers_skill", weight=weight_mod)

    def get_related_skills(self, recruiter_id: str) -> Dict[str, float]:
        """
        Calculates recruiter's skill preference strengths.
        """
        if not self.graph.has_node(recruiter_id):
            return {}
            
        skills_weight = {}
        for neighbor in self.graph.neighbors(recruiter_id):
            edge_data = self.graph.get_edge_data(recruiter_id, neighbor)
            if edge_data.get("relation") == "prefers_skill":
                skills_weight[neighbor] = edge_data.get("weight", 1.0)
                
        return skills_weight
