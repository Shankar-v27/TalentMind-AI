import os
import pickle
import numpy as np
import faiss


class CacheManager:


    def __init__(self, settings):

        self.settings = settings

        os.makedirs(
            settings.CACHE_DIR,
            exist_ok=True
        )


    def cache_exists(self):

        return (
            os.path.exists(
                self.settings.EMBEDDING_CACHE_FILE
            )
            and
            os.path.exists(
                self.settings.FAISS_INDEX_FILE
            )
            and
            os.path.exists(
                self.settings.CANDIDATE_MAPPING_FILE
            )
        )


    def save(
        self,
        embeddings,
        index,
        candidate_ids
    ):

        np.save(
            self.settings.EMBEDDING_CACHE_FILE,
            embeddings
        )


        faiss.write_index(
            index.index,
            self.settings.FAISS_INDEX_FILE
        )


        with open(
            self.settings.CANDIDATE_MAPPING_FILE,
            "wb"
        ) as file:

            pickle.dump(
                candidate_ids,
                file
            )


        print(
            "Cache saved successfully"
        )


    def load(self):

        embeddings = np.load(
            self.settings.EMBEDDING_CACHE_FILE
        )


        index = faiss.read_index(
            self.settings.FAISS_INDEX_FILE
        )


        with open(
            self.settings.CANDIDATE_MAPPING_FILE,
            "rb"
        ) as file:

            candidate_ids = pickle.load(file)


        print(
            "Cache loaded successfully"
        )


        return (
            embeddings,
            index,
            candidate_ids
        )