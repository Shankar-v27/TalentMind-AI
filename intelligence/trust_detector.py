class TrustDetector:

    def calculate_score(self, candidate):

        skills = candidate.get(
            "skills",
            []
        )

        if not skills:
            return 0.5


        trusted = 0


        for skill in skills:

            duration = skill.get(
                "duration_months",
                0
            )

            endorsements = skill.get(
                "endorsements",
                0
            )


            if (
                duration >= 6
                and endorsements >= 3
            ):
                trusted += 1


        trust = trusted / len(skills)


        return max(
            trust,
            0.2
        )