# ranking/ranker.py


class CandidateRanker:


    def rank(self, candidates):

        return sorted(
            candidates,
            key=lambda x: x["score"],
            reverse=True
        )