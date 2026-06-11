# config/settings.py

import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class Settings:

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    # ==============================
    # Data Paths
    # ==============================

    DATA_DIR = str(PROJECT_ROOT / "data")

    CANDIDATE_FILE = str(Path(DATA_DIR) / "candidates.jsonl")

    JOB_DESCRIPTION_FILE = str(Path(DATA_DIR) / "job_description.docx")

    OUTPUT_FILE = str(Path(DATA_DIR) / "submission.csv")


    # ==============================
    # Embedding Configuration
    # ==============================

    # Recommended during development:
    # all-MiniLM-L6-v2 (fast, 384 dimensions)
    # For final submission:
    # all-mpnet-base-v2 (better quality, 768 dimensions)

    EMBEDDING_MODEL = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    EMBEDDING_DIMENSION = 384

    BATCH_SIZE = 64


    # ==============================
    # Cache Configuration
    # ==============================

    CACHE_DIR = str(PROJECT_ROOT / "cache")

    EMBEDDING_CACHE_FILE = str(Path(CACHE_DIR) / "candidate_embeddings.npy")

    FAISS_INDEX_FILE = str(Path(CACHE_DIR) / "faiss.index")

    CANDIDATE_MAPPING_FILE = str(Path(CACHE_DIR) / "candidate_mapping.pkl")


    # ==============================
    # Semantic Search
    # ==============================

    TOP_K_RETRIEVAL = 1000


    # ==============================
    # Groq LLM Configuration
    # ==============================

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    GROQ_MODEL = (
        "openai/gpt-oss-120b"
    )

    GROQ_BATCH_SIZE = 20

    GROQ_MAX_RETRIES = 3

    GROQ_RETRY_DELAY = 3









    # ==============================
    # Ranking Configuration
    # ==============================

    TOP_K_CANDIDATES = 200


    # ==============================
    # Final Weighted Scoring
    # ==============================

    SCORE_WEIGHTS = {

        "skills": 0.25,

        "career": 0.20,

        "experience": 0.15,

        "education": 0.10,

        "intent": 0.15,

        "reliability": 0.10,

        "activity": 0.03,

        "logistics": 0.02
    }


    # ==============================
    # Behavioral Calibration
    # ==============================

    MIN_BEHAVIOR_MULTIPLIER = 0.5

    MAX_BEHAVIOR_MULTIPLIER = 1.0


    # ==============================
    # Performance
    # ==============================

    SCORING_BATCH_SIZE = 256


    # ==============================
    # XGBoost Ranking Configuration
    # ==============================

    XGB_PARAMS = {

        "objective": "rank:pairwise",

        "learning_rate": 0.05,

        "max_depth": 6,

        "n_estimators": 300,

        "subsample": 0.8,

        "colsample_bytree": 0.8,

        "random_state": 42
    }

