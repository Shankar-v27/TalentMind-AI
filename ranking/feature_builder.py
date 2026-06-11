# ranking/feature_builder.py

from intelligence.skill_matcher import SkillMatcher
from intelligence.experience_engine import ExperienceEngine
from intelligence.career_analyzer import CareerAnalyzer
from intelligence.education_scorer import EducationScorer
from intelligence.behavioral_engine import BehavioralEngine
from intelligence.trust_detector import TrustDetector


class FeatureBuilder:

    def __init__(self):

        self.skill_engine = SkillMatcher()
        self.exp_engine = ExperienceEngine()
        self.career_engine = CareerAnalyzer()
        self.edu_engine = EducationScorer()
        self.behavior_engine = BehavioralEngine()
        self.trust_engine = TrustDetector()


    def build(self, candidate, jd_data):

        features = {}

        # ----------------------
        # Core recruiter signals
        # ----------------------

        features["skills"] = (
            self.skill_engine.calculate_score(
                candidate,
                jd_data
            )
        )

        features["experience"] = (
            self.exp_engine.calculate_score(
                candidate,
                jd_data
            )
        )

        features["career"] = (
            self.career_engine.calculate_score(
                candidate
            )
        )

        features["education"] = (
            self.edu_engine.calculate_score(
                candidate
            )
        )


        # ----------------------
        # Behavioral signals
        # ----------------------

        behavior = (
            self.behavior_engine.calculate_scores(
                candidate
            )
        )


        features["reliability"] = (
            behavior["reliability"]
        )

        features["intent"] = (
            behavior["intent"]
        )

        features["activity"] = (
            behavior["activity"]
        )


        # ----------------------
        # Anti-honeypot score
        # ----------------------

        features["trust"] = (
            self.trust_engine.calculate_score(
                candidate
            )
        )


        return features