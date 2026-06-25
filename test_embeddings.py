from config.settings import Settings

from preprocessing.parser import load_candidates
from preprocessing.jd_extractor import extract_job_description
from preprocessing.cleaner import clean_text

from embeddings.embedder import EmbeddingModel
from embeddings.faiss_index import CandidateIndex
from embeddings.candidate_search import (
    build_candidate_text
)


# Load data
candidates = load_candidates(
    Settings.CANDIDATE_FILE
)


# Prepare candidate documents
documents = []

for c in candidates:
    documents.append(
        build_candidate_text(c)
    )


print("Preparing embeddings...")

# Load AI model
model = EmbeddingModel()


# Candidate embeddings
candidate_vectors = model.encode(
    documents
)


# Create vector DB
index = CandidateIndex(
    Settings.EMBEDDING_DIMENSION
)


index.add(candidate_vectors)


# JD embedding
jd = extract_job_description(
    Settings.JOB_DESCRIPTION_FILE
)

jd = clean_text(jd)


query_vector = model.encode(
    [jd]
)


# Search
scores, ids = index.search(
    query_vector,
    Settings.TOP_K_RETRIEVAL
)


print("\nTop Candidates\n")

valid_ids = [idx for idx in ids if idx >= 0]
for i in range(min(10, len(valid_ids))):
    candidate = candidates[valid_ids[i]]

    print(
        f"Rank {i+1}"
    )

    print(
        "Score:",
        round(float(scores[i]), 3)
    )

    print(
        "Candidate ID:",
        candidate.get(
            "candidate_id"
        )
    )

    print("-" * 50)