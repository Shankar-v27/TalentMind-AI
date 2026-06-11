class EducationScorer:


    TIER_SCORE = {

        "tier_1": 1.0,
        "tier_2": 0.8,
        "tier_3": 0.6,
        "tier_4": 0.45,
        "unknown": 0.5
    }


    def calculate_score(self, candidate):

        education = candidate.get(
            "education",
            []
        )


        if not education:
            return 0.3


        scores = []


        for edu in education:

            tier = edu.get(
                "tier",
                "unknown"
            )


            scores.append(
                self.TIER_SCORE.get(
                    tier,
                    0.5
                )
            )


        return max(scores)
