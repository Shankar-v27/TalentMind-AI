# intelligence/candidate_dna.py

from typing import Dict, Any
from intelligence.speed_engine import SpeedEngine
from intelligence.ownership_engine import OwnershipEngine
from intelligence.innovation_engine import InnovationEngine
from intelligence.risk_engine import RiskEngine
from intelligence.leadership_engine import LeadershipEngine
from intelligence.communication_engine import CommunicationEngine
from intelligence.learning_engine import LearningEngine

class CandidateDNA:
    def __init__(self):
        self.speed_eng = SpeedEngine()
        self.own_eng = OwnershipEngine()
        self.inno_eng = InnovationEngine()
        self.risk_eng = RiskEngine()
        self.lead_eng = LeadershipEngine()
        self.comm_eng = CommunicationEngine()
        self.learn_eng = LearningEngine()
        
    def generate(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        speed = self.speed_eng.calculate(candidate)["speed_score"]
        ownership = self.own_eng.calculate(candidate)["ownership"]
        innovation = self.inno_eng.calculate(candidate)["innovation_score"]
        risk = self.risk_eng.calculate(candidate)["risk_score"]
        leadership = self.lead_eng.calculate(candidate)["leadership"]
        comm = self.comm_eng.calculate(candidate)["communication"]
        learning = self.learn_eng.calculate(candidate)["learning"]
        
        # Derived DNA vectors
        adaptability = round((learning + speed) / 2.0, 2)
        stability = round(max(0.1, min(0.99, 1.0 - risk)), 2)
        creativity = round((innovation + learning) / 2.0, 2)
        collaboration = round((comm + ownership) / 2.0, 2)
        execution = round((speed + ownership) / 2.0, 2)
        research = round(max(0.1, min(0.99, innovation * 0.9 + learning * 0.1)), 2)
        management = leadership
        experimentation = innovation
        autonomy = ownership
        ambiguity = risk
        customer = round(max(0.1, min(0.99, comm * 0.8 + ownership * 0.2)), 2)
        team = round(max(0.1, min(0.99, comm * 0.7 + learning * 0.3)), 2)
        growth = learning
        
        return {
            "speed": speed,
            "ownership": ownership,
            "leadership": leadership,
            "innovation": innovation,
            "learning": learning,
            "communication": comm,
            "risk": risk,
            "adaptability": adaptability,
            "stability": stability,
            "creativity": creativity,
            "collaboration": collaboration,
            "execution": execution,
            "research": research,
            "management": management,
            "experimentation": experimentation,
            "autonomy": autonomy,
            "ambiguity": ambiguity,
            "customer": customer,
            "team": team,
            "growth": growth
        }
