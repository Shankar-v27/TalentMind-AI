class CareerAnalyzer:


    LEVELS = {

        "intern": 0,
        "junior": 1,
        "engineer": 2,
        "senior": 3,
        "lead": 4,
        "manager": 5,
        "director": 6
    }


    def get_level(self, title):

        title = title.lower()


        for key, value in self.LEVELS.items():

            if key in title:
                return value


        return 2


    def calculate_score(self, candidate):

        history = candidate.get(
            "career_history",
            []
        )


        if not history:
            return 0.5


        levels = []


        for job in history:

            levels.append(
                self.get_level(
                    job.get(
                        "title",
                        ""
                    )
                )
            )


        growth = (
            max(levels)
            -
            min(levels)
        )


        if growth >= 3:
            return 1.0

        if growth >= 1:
            return 0.8


        return 0.6