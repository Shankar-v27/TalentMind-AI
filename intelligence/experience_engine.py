class ExperienceEngine:

    def calculate_score(self, candidate, jd_data):

        profile = candidate.get("profile", {})

        experience = profile.get(
            "years_of_experience",
            0
        )

        required = jd_data.get(
            "min_experience",
            0
        )

        if required == 0:
            return 1.0

        if experience >= required:
            return 1.0

        return round(experience / required, 3)