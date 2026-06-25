"""
TalentMind-AI — Candidate Ranking Pipeline
============================================
5-stage AI pipeline for ranking candidates against a job description.
Stage 1 : Deep Semantic Understanding  (sentence-transformers + FAISS)
Stage 2 : Multi-Dimensional Scoring    (8 dimensions)
Stage 3 : Weighted Fusion Engine
Stage 4 : LLM Reasoning Layer          (Groq / Anthropic Claude)
Stage 5 : Output Generation            (submission.csv)

Author  : Shankar V
Challenge: India Runs Data & AI Challenge — Redrob
"""

import sys
from config.settings import Settings
from preprocessing.parser import load_candidates
from preprocessing.jd_extractor import extract_job_description
from preprocessing.cleaner import clean_text
from embeddings.embedder import EmbeddingModel
from embeddings.faiss_index import CandidateIndex
from embeddings.candidate_search import build_candidate_text
from embeddings.cache_manager import CacheManager
from intelligence.jd_analyzer import JDAnalyzer
from ranking.feature_builder import FeatureBuilder
from ranking.scorer import FinalScorer
from ranking.ranker import CandidateRanker
from explainability.reason_generator import ReasonGenerator
from explainability.batch_processor import create_batches
from explainability.submission_generator import SubmissionGenerator

def run_pipeline():
    print("\n" + "=" * 60)
    print("      Starting TalentMind AI 5-Stage Ranking Pipeline")
    print("=" * 60)

    # 1. Load Data
    print("\n[Stage 0] Loading Candidates and Job Description...")
    candidates = load_candidates(Settings.CANDIDATE_FILE)
    jd_raw = extract_job_description(Settings.JOB_DESCRIPTION_FILE)
    jd_clean = clean_text(jd_raw)

    # 2. JD Analysis (LLM parsing)
    print("\n[Stage 1] Analyzing Job Description requirements using AI...")
    analyzer = JDAnalyzer()
    jd_data = analyzer.analyze(jd_clean)
    print("Extracted JD Requirements:", jd_data)

    # 3. FAISS Retrieval (Semantic Search)
    print("\n[Stage 1] Embedding Job Description and searching candidates via FAISS...")
    cache = CacheManager(Settings)
    if cache.cache_exists():
        _, faiss_index, _ = cache.load()
        index = CandidateIndex(existing_index=faiss_index)
    else:
        print("FAISS index cache not found. Generating new candidate embeddings...")
        documents = [build_candidate_text(c) for c in candidates]
        model = EmbeddingModel()
        vectors = model.encode(documents)
        index = CandidateIndex(Settings.EMBEDDING_DIMENSION)
        index.add(vectors)
        candidate_ids = [c["candidate_id"] for c in candidates]
        cache.save(vectors, index, candidate_ids)

    model = EmbeddingModel()
    jd_vector = model.encode([jd_clean])
    scores, ids = index.search(jd_vector, Settings.TOP_K_RETRIEVAL)
    top_candidates = [candidates[idx] for idx in ids if idx >= 0]
    print(f"Retrieved top {len(top_candidates)} candidate profiles semantically matched.")

    # 4. Multi-Dimensional Scoring (Stage 2) & Weighted Fusion (Stage 3)
    print("\n[Stage 2 & 3] Engineering multi-dimensional features and calculating Fusion scores...")
    feature_builder = FeatureBuilder()
    scorer = FinalScorer()
    ranked_data = []

    for candidate in top_candidates:
        features = feature_builder.build(candidate, jd_data)
        score = scorer.calculate(features)
        ranked_data.append({
            "candidate_id": candidate["candidate_id"],
            "candidate": candidate,
            "features": features,
            "score": score
        })

    ranker = CandidateRanker()
    ranked_data = ranker.rank(ranked_data)
    final_candidates = ranked_data[:Settings.TOP_K_CANDIDATES]
    print(f"Candidates ranked. Selected top {len(final_candidates)} candidates.")

    # 5. LLM Reasoning Layer (Stage 4)
    print("\n[Stage 4] Generating natural language hiring reasoning...")
    reason_generator = ReasonGenerator()
    batches = create_batches(final_candidates, Settings.GROQ_BATCH_SIZE)

    for i, batch in enumerate(batches):
        print(f"Processing reasoning batch {i + 1}/{len(batches)}...")
        responses = reason_generator.generate_batch(batch, jd_data)
        reasoning_map = {item["candidate_id"]: item["reasoning"] for item in responses}
        for candidate in batch:
            candidate["reasoning"] = reasoning_map.get(
                candidate["candidate_id"],
                "Strong technical candidate matching required skill profile."
            )

    # 6. Output Generation (Stage 5)
    print("\n[Stage 5] Saving final ranking results to CSV...")
    submission = SubmissionGenerator()
    submission.create(final_candidates, Settings.OUTPUT_FILE)
    
    print("\n" + "=" * 60)
    print("            Pipeline Completed Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()