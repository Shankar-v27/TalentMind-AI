# intelligence/personality_engine.py

from typing import Dict, Any
from intelligence.speed_engine import SpeedEngine
from intelligence.ownership_engine import OwnershipEngine
from intelligence.innovation_engine import InnovationEngine
from intelligence.risk_engine import RiskEngine
from intelligence.leadership_engine import LeadershipEngine
from intelligence.communication_engine import CommunicationEngine
from intelligence.learning_engine import LearningEngine

class PersonalityEngine:
    def __init__(self):
        self.speed_eng = SpeedEngine()
        self.own_eng = OwnershipEngine()
        self.inno_eng = InnovationEngine()
        self.risk_eng = RiskEngine()
        self.lead_eng = LeadershipEngine()
        self.comm_eng = CommunicationEngine()
        self.learn_eng = LearningEngine()
        
    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        speed = self.speed_eng.calculate(candidate)["speed_score"]
        ownership = self.own_eng.calculate(candidate)["ownership"]
        innovation = self.inno_eng.calculate(candidate)["innovation_score"]
        risk = self.risk_eng.calculate(candidate)["risk_score"]
        leadership = self.lead_eng.calculate(candidate)["leadership"]
        comm = self.comm_eng.calculate(candidate)["communication"]
        learning = self.learn_eng.calculate(candidate)["learning"]
        
        # Calculate personality archetype mapping scores
        scores = {
            "Builder": 0.4 * speed + 0.4 * ownership + 0.2 * innovation,
            "Leader": 0.5 * leadership + 0.3 * comm + 0.2 * ownership,
            "Innovator": 0.5 * innovation + 0.3 * speed + 0.2 * risk,
            "Researcher": 0.4 * learning + 0.4 * innovation + 0.2 * comm,
            "Architect": 0.4 * ownership + 0.3 * learning + 0.3 * speed,
            "Strategist": 0.4 * leadership + 0.3 * risk + 0.3 * comm,
            "Mentor": 0.5 * comm + 0.3 * leadership + 0.2 * learning,
            "Executor": 0.4 * speed + 0.4 * comm + 0.2 * ownership,
            "Explorer": 0.5 * risk + 0.3 * innovation + 0.2 * speed,
            "Operator": 0.4 * comm + 0.4 * speed + 0.2 * leadership,
            "Visionary": 0.5 * innovation + 0.3 * risk + 0.2 * leadership,
            "Creator": 0.4 * innovation + 0.4 * ownership + 0.2 * speed
        }
        
        sorted_personalities = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "primary": sorted_personalities[0][0],
            "secondary": sorted_personalities[1][0],
            "tertiary": sorted_personalities[2][0]
        }
