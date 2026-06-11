# embeddings/faiss_index.py

import faiss
import numpy as np


class CandidateIndex:


    def __init__(
        self,
        dimension=None,
        existing_index=None
    ):

        """
        If existing_index is provided,
        use the cached FAISS index.

        Otherwise create a new one.
        """

        if existing_index is not None:

            self.index = existing_index

        else:

            self.index = faiss.IndexFlatIP(
                dimension
            )


    def add(self, vectors):

        """
        Add candidate vectors
        to the FAISS database.
        """

        self.index.add(
            vectors.astype(
                np.float32
            )
        )


    def search(
        self,
        query_vector,
        k=1000
    ):

        """
        Search the nearest
        candidate embeddings.
        """

        scores, ids = self.index.search(
            query_vector.astype(
                np.float32
            ),
            k
        )


        return (
            scores[0],
            ids[0]
        )


    def count(self):

        """
        Number of candidates
        in the FAISS index.
        """

        return self.index.ntotal