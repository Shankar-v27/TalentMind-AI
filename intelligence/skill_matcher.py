# intelligence/skill_matcher.py


from intelligence.knowledge_graph import (
    get_related_skills
)


class SkillMatcher:


    PROFICIENCY_SCORE = {

        "beginner": 0.5,
        "intermediate": 0.8,
        "advanced": 1.0,
        "expert": 1.0
    }


    def duration_score(self, months):

        if months >= 24:
            return 1.0

        elif months >= 12:
            return 0.85

        elif months >= 6:
            return 0.7

        return 0.4


    def endorsement_score(self, count):

        if count >= 25:
            return 1.0

        elif count >= 10:
            return 0.9

        elif count >= 3:
            return 0.7

        return 0.5


    def calculate_score(
        self,
        candidate,
        jd_data
    ):

        candidate_skills = candidate.get(
            "skills",
            []
        )


        required = [
            skill.lower()
            for skill in jd_data.get(
                "required_skills",
                []
            )
        ]


        if not required:
            return 0


        total_score = 0


        for req_skill in required:

            best_match = 0


            for skill in candidate_skills:

                name = skill.get(
                    "name",
                    ""
                ).lower()


                # -------------------------
                # Exact Match
                # -------------------------

                if name == req_skill:

                    match_score = 1.0


                # -------------------------
                # Related Skill Match
                # -------------------------

                elif (
                    name in get_related_skills(
                        req_skill
                    )
                ):

                    match_score = 0.7


                else:
                    continue


                # -------------------------
                # Skill Depth
                # -------------------------

                proficiency = (
                    self.PROFICIENCY_SCORE.get(
                        skill.get(
                            "proficiency",
                            "beginner"
                        ).lower(),
                        0.5
                    )
                )


                duration = self.duration_score(
                    skill.get(
                        "duration_months",
                        0
                    )
                )


                endorsements = (
                    self.endorsement_score(
                        skill.get(
                            "endorsements",
                            0
                        )
                    )
                )


                skill_score = (
                    match_score *
                    proficiency *
                    duration *
                    endorsements
                )


                if skill_score > best_match:
                    best_match = skill_score


            total_score += best_match


        final_score = (
            total_score /
            len(required)
        )


        return round(
            final_score,
            3
        )
