# embeddings/embedder.py

from sentence_transformers import SentenceTransformer
from config.settings import Settings


class EmbeddingModel:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(
            Settings.EMBEDDING_MODEL
        )

        print("Embedding model loaded")


    def encode(self, texts, batch_size=None):
        """
        Convert texts into vectors
        """

        vectors = self.model.encode(
            texts,
            batch_size=batch_size or Settings.BATCH_SIZE,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return vectors