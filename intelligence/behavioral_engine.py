class BehavioralEngine:

    def _clamp(self, value, minimum=0, maximum=1):

        try:
            value = float(value)
        except (TypeError, ValueError):
            return minimum

        return max(
            minimum,
            min(value, maximum)
        )


    def calculate_scores(self, candidate):

        signals = candidate.get(
            "redrob_signals",
            {}
        )


        # Reliability
        reliability = (
            self._clamp(signals.get(
                "recruiter_response_rate",
                0
            )) * 0.4
            +
            self._clamp(signals.get(
                "interview_completion_rate",
                0
            )) * 0.3
            +
            self._clamp(signals.get(
                "offer_acceptance_rate",
                0
            )) * 0.3
        )


        # Intent
        intent = 0

        if signals.get(
            "open_to_work_flag",
            False
        ):
            intent += 0.6


        if signals.get(
            "applications_submitted_30d",
            0
        ) > 0:
            intent += 0.2


        if signals.get(
            "willing_to_relocate",
            False
        ):
            intent += 0.2


        intent = min(intent, 1)


        # Activity

        github = (
            self._clamp(
                signals.get(
                    "github_activity_score",
                    0
                ),
                0,
                100
            ) / 100
        )


        completeness = (
            self._clamp(
                signals.get(
                    "profile_completeness_score",
                    0
                ),
                0,
                100
            ) / 100
        )


        visibility = self._clamp(
            signals.get(
                "search_appearance_30d",
                0
            ) / 300
        )


        activity = (
            github * 0.4
            +
            completeness * 0.4
            +
            visibility * 0.2
        )


        return {

            "reliability": round(
                self._clamp(reliability),
                3
            ),

            "intent": round(
                self._clamp(intent),
                3
            ),

            "activity": round(
                self._clamp(activity),
                3
            )
        }
