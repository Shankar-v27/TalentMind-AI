# explainability/submission_generator.py


import pandas as pd


class SubmissionGenerator:


    def create(
        self,
        ranked_candidates,
        output_path
    ):

        rows = []


        for rank, candidate in enumerate(
            ranked_candidates,
            start=1
        ):

            rows.append(
                {
                    "candidate_id":
                        candidate["candidate_id"],

                    "rank":
                        rank,

                    "score":
                        candidate["score"],

                    "reasoning":
                        candidate["reasoning"]
                }
            )


        df = pd.DataFrame(rows)


        df.to_csv(
            output_path,
            index=False
        )


        print(
            f"Submission saved at {output_path}"
        )