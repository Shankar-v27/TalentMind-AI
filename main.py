# main.py

from config.settings import Settings

# ==============================
# Preprocessing
# ==============================

from preprocessing.parser import load_candidates
from preprocessing.jd_extractor import extract_job_description
from preprocessing.cleaner import clean_text


# ==============================
# Embeddings
# ==============================

from embeddings.embedder import EmbeddingModel
from embeddings.faiss_index import CandidateIndex
from embeddings.candidate_search import build_candidate_text
from embeddings.cache_manager import CacheManager


# ==============================
# Intelligence
# ==============================

from intelligence.jd_analyzer import JDAnalyzer


# ==============================
# Ranking
# ==============================

from ranking.feature_builder import FeatureBuilder
from ranking.scorer import FinalScorer
from ranking.ranker import CandidateRanker


# ==============================
# Explainability
# ==============================

from explainability.reason_generator import ReasonGenerator
from explainability.batch_processor import create_batches
from explainability.submission_generator import SubmissionGenerator


# =========================================================
# Load or create FAISS search engine
# =========================================================

def get_search_engine(candidates):

    cache = CacheManager(Settings)

    # Use cached FAISS
    if cache.cache_exists():

        print("\nLoading cached FAISS index...")

        _, faiss_index, _ = cache.load()

        index = CandidateIndex(
            existing_index=faiss_index
        )

        print(
            f"FAISS loaded successfully. "
            f"Candidates indexed: {index.count()}"
        )

        return index


    # Build new embeddings if cache missing
    print(
        "\nNo cache found. Creating embeddings..."
    )

    documents = [
        build_candidate_text(candidate)
        for candidate in candidates
    ]

    model = EmbeddingModel()

    vectors = model.encode(
        documents
    )


    index = CandidateIndex(
        Settings.EMBEDDING_DIMENSION
    )

    index.add(vectors)


    candidate_ids = [
        c["candidate_id"]
        for c in candidates
    ]


    cache.save(
        vectors,
        index,
        candidate_ids
    )

    print("New FAISS cache created.")

    return index



# =========================================================
# Main Pipeline
# =========================================================

def main():

    print("\n" + "=" * 60)
    print("          TalentMind AI Recruiter")
    print("=" * 60)


    # -------------------------------------
    # Step 1: Load candidates
    # -------------------------------------

    print("\nLoading candidate database...")

    candidates = load_candidates(
        Settings.CANDIDATE_FILE
    )


    # -------------------------------------
    # Step 2: Load JD
    # -------------------------------------

    print("\nLoading Job Description...")

    jd = extract_job_description(
        Settings.JOB_DESCRIPTION_FILE
    )

    jd = clean_text(jd)


    # -------------------------------------
    # Step 3: JD analysis using Groq
    # -------------------------------------

    print("\nAnalyzing JD with Groq...")

    analyzer = JDAnalyzer()

    jd_data = analyzer.analyze(
        jd
    )

    print("\nExtracted Requirements:")
    print(jd_data)


    # -------------------------------------
    # Step 4: Load FAISS
    # -------------------------------------

    index = get_search_engine(
        candidates
    )


    # -------------------------------------
    # Step 5: Embed JD
    # -------------------------------------

    print("\nEmbedding Job Description...")

    model = EmbeddingModel()

    jd_vector = model.encode(
        [jd]
    )


    # -------------------------------------
    # Step 6: Semantic Search
    # -------------------------------------

    print("\nSearching top candidates...")

    scores, ids = index.search(
        jd_vector,
        Settings.TOP_K_RETRIEVAL
    )


    top_candidates = [
        candidates[idx]
        for idx in ids
    ]

    print(
        f"Retrieved {len(top_candidates)} candidates"
    )


    # -------------------------------------
    # Step 7: Feature Engineering
    # -------------------------------------

    print(
        "\nCalculating AI recruiter scores..."
    )

    feature_builder = FeatureBuilder()
    scorer = FinalScorer()

    ranked_data = []


    for candidate in top_candidates:

        features = feature_builder.build(
            candidate,
            jd_data
        )


        score = scorer.calculate(
            features
        )


        ranked_data.append(
            {
                "candidate_id":
                    candidate["candidate_id"],

                "candidate":
                    candidate,

                "features":
                    features,

                "score":
                    score
            }
        )


    # -------------------------------------
    # Step 8: Rank candidates
    # -------------------------------------

    print("\nRanking candidates...")

    ranker = CandidateRanker()

    ranked_data = ranker.rank(
        ranked_data
    )


    final_candidates = ranked_data[
        :Settings.TOP_K_CANDIDATES
    ]


    print(
        f"Selected top "
        f"{len(final_candidates)} candidates"
    )


    # -------------------------------------
    # Step 9: Generate Groq reasoning
    # -------------------------------------

    print(
        "\nGenerating recruiter explanations..."
    )


    reason_generator = ReasonGenerator()


    batches = create_batches(
        final_candidates,
        Settings.GROQ_BATCH_SIZE
    )


    for i, batch in enumerate(batches):

        print(
            f"Groq Batch {i+1}/"
            f"{len(batches)}"
        )


        responses = (
            reason_generator.generate_batch(
                batch,
                jd_data
            )
        )


        reasoning_map = {
            item["candidate_id"]:
            item["reasoning"]

            for item in responses
        }


        for candidate in batch:

            candidate["reasoning"] = (
                reasoning_map.get(
                    candidate["candidate_id"],
                    "Strong technical candidate with relevant experience."
                )
            )


    # -------------------------------------
    # Step 10: Create CSV
    # -------------------------------------

    print(
        "\nCreating submission file..."
    )


    submission = SubmissionGenerator()

    submission.create(
        final_candidates,
        Settings.OUTPUT_FILE
    )


    print("\n" + "=" * 60)
    print("TalentMind AI Completed Successfully")
    print("=" * 60)


# Entry Point
if __name__ == "__main__":
    main()