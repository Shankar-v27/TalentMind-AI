def build_candidate_text(candidate):

    parts = []

    profile = candidate.get(
        "profile",
        {}
    )


    parts.append(
        profile.get(
            "headline",
            ""
        )
    )


    parts.append(
        profile.get(
            "summary",
            ""
        )
    )


    for skill in candidate.get(
        "skills",
        []
    ):
        parts.append(
            skill.get(
                "name",
                ""
            )
        )


    for job in candidate.get(
        "career_history",
        []
    ):

        parts.append(
            job.get(
                "title",
                ""
            )
        )


        parts.append(
            job.get(
                "description",
                ""
            )
        )


    return " ".join(parts)