from config.settings import Settings

from preprocessing.parser import load_candidates

from embeddings.embedder import EmbeddingModel
from embeddings.candidate_search import build_candidate_text
from embeddings.faiss_index import CandidateIndex
from embeddings.cache_manager import CacheManager


print("Loading candidates...")

candidates = load_candidates(
    Settings.CANDIDATE_FILE
)


print("Preparing documents...")

documents = [
    build_candidate_text(c)
    for c in candidates
]


print("Generating embeddings...")

model = EmbeddingModel()

vectors = model.encode(
    documents
)


print("Building FAISS...")

index = CandidateIndex(
    Settings.EMBEDDING_DIMENSION
)

index.add(vectors)


candidate_ids = [
    c["candidate_id"]
    for c in candidates
]


cache = CacheManager(Settings)

cache.save(
    vectors,
    index,
    candidate_ids
)

print(
    "All cache files created!"
)