# ranking/scorer.py

from config.settings import Settings


class FinalScorer:

    def _score_value(self, features, name):

        try:
            value = float(features.get(name, 0))
        except (TypeError, ValueError):
            return 0

        return max(
            0,
            min(value, 1)
        )


    def calculate(self, features):

        weights = Settings.SCORE_WEIGHTS

        skill_score = self._score_value(features, "skills")
        career_score = self._score_value(features, "career")
        experience_score = self._score_value(features, "experience")
        education_score = self._score_value(features, "education")
        intent_score = self._score_value(features, "intent")
        reliability_score = self._score_value(features, "reliability")
        activity_score = self._score_value(features, "activity")
        trust_score = self._score_value(features, "trust")

        # Base weighted score
        score = (
            skill_score * weights["skills"] +
            career_score * weights["career"] +
            experience_score * weights["experience"] +
            education_score * weights["education"] +
            intent_score * weights["intent"] +
            reliability_score * weights["reliability"] +
            activity_score * weights["activity"]
        )


        # Reliability multiplier
        behavior_multiplier = (
            0.5 +
            reliability_score * 0.5
        )


        # Trust multiplier
        trust_multiplier = max(
            trust_score,
            0.2
        )


        final_score = (
            score *
            behavior_multiplier *
            trust_multiplier
        )


        return round(
            max(0, min(final_score, 1)),
            4
        )
