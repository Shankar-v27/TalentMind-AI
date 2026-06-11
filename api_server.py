import logging
from io import BytesIO

from docx import Document
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware

from config.settings import Settings
from intelligence.jd_analyzer import JDAnalyzer
from preprocessing.cleaner import clean_text
from preprocessing.parser import load_candidates
from ranking.feature_builder import FeatureBuilder
from ranking.ranker import CandidateRanker
from ranking.scorer import FinalScorer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TalentMind AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_candidates_cache = None
_last_ranked_candidates = []
_current_jd_analysis = None  # Store current session's JD analysis


def _load_candidates():
    global _candidates_cache

    if _candidates_cache is None:
        logger.info(f"Loading candidates from {Settings.CANDIDATE_FILE}...")
        try:
            _candidates_cache = load_candidates(Settings.CANDIDATE_FILE)
            logger.info(f"Successfully loaded {len(_candidates_cache)} candidates")
        except Exception as e:
            logger.error(f"Error loading candidates: {str(e)}", exc_info=True)
            # Return empty list on error to prevent full system failure
            _candidates_cache = []
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load candidate database: {str(e)}"
            )

    return _candidates_cache


async def _read_docx(upload: UploadFile):
    contents = await upload.read()
    document = Document(BytesIO(contents))
    paragraphs = [para.text.strip() for para in document.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)


def _to_frontend_analysis(jd_data):
    min_experience = jd_data.get("min_experience") or 0
    experience = f"{min_experience:g}+ years" if min_experience else "Not specified"

    return {
        "role": jd_data.get("role") or jd_data.get("seniority") or "Parsed job description",
        "requiredSkills": jd_data.get("required_skills", []),
        "preferredSkills": jd_data.get("preferred_skills", []),
        "experienceRange": experience,
        "seniority": jd_data.get("seniority") or "Not specified",
        "domain": jd_data.get("domain") or "Not specified",
        "location": jd_data.get("location") or "Not specified",
        "workMode": jd_data.get("work_mode") or "Not specified",
    }


def _percent(value):
    return int(round(max(0, min(float(value or 0), 1)) * 100))


def _candidate_text(candidate):
    profile = candidate.get("profile", {})
    parts = [
        profile.get("headline", ""),
        profile.get("summary", ""),
        profile.get("current_title", ""),
        profile.get("current_company", ""),
        profile.get("location", ""),
    ]
    parts.extend(skill.get("name", "") for skill in candidate.get("skills", []))
    parts.extend(job.get("title", "") for job in candidate.get("career_history", []))
    return " ".join(parts).lower()


def _prefilter_candidates(candidates, jd_data, limit=2500):
    terms = [
        skill.lower()
        for skill in jd_data.get("required_skills", []) + jd_data.get("preferred_skills", [])
        if skill
    ]

    if not terms:
        return candidates[:limit]

    scored = []
    for candidate in candidates:
        text = _candidate_text(candidate)
        hits = sum(1 for term in terms if term in text)
        if hits:
            scored.append((hits, candidate))

    if not scored:
        return candidates[:limit]

    scored.sort(key=lambda item: item[0], reverse=True)
    return [candidate for _, candidate in scored[:limit]]


def _reason(candidate, jd_data, features):
    profile = candidate.get("profile", {})
    required = {skill.lower() for skill in jd_data.get("required_skills", [])}
    candidate_skills = [skill.get("name", "") for skill in candidate.get("skills", [])]
    matched = [skill for skill in candidate_skills if skill.lower() in required][:4]

    match_text = ", ".join(matched) if matched else "adjacent skills"
    experience = profile.get("years_of_experience", 0)

    return (
        f"Matches {match_text}; {experience:g} yrs experience with "
        f"{_percent(features.get('reliability'))}% reliability and "
        f"{_percent(features.get('intent'))}% intent signals."
    )


def _to_frontend_candidate(item, rank):
    candidate = item["candidate"]
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    features = item["features"]

    skills = [skill.get("name", "") for skill in candidate.get("skills", []) if skill.get("name")]

    return {
        "id": candidate.get("candidate_id"),
        "name": profile.get("anonymized_name") or candidate.get("candidate_id"),
        "rank": rank,
        "score": _percent(item["score"]),
        "role": profile.get("current_title") or profile.get("headline") or "Candidate",
        "experience": profile.get("years_of_experience", 0),
        "location": profile.get("location") or profile.get("country") or "Not specified",
        "company": profile.get("current_company") or "Not specified",
        "skills": skills[:8],
        "trust": _percent(features.get("trust")),
        "behavioral": _percent(
            (features.get("reliability", 0) + features.get("intent", 0) + features.get("activity", 0)) / 3
        ),
        "shortlisted": False,
        "reasoning": item.get("reasoning", ""),
        "openToWork": bool(signals.get("open_to_work_flag")),
        "workMode": signals.get("preferred_work_mode", "flexible"),
        "willingToRelocate": bool(signals.get("willing_to_relocate")),
    }


def _rank_candidates(jd_data):
    candidates = _prefilter_candidates(_load_candidates(), jd_data)
    feature_builder = FeatureBuilder()
    scorer = FinalScorer()
    ranker = CandidateRanker()
    ranked = []

    for candidate in candidates:
        features = feature_builder.build(candidate, jd_data)
        score = scorer.calculate(features)
        ranked.append(
            {
                "candidate_id": candidate["candidate_id"],
                "candidate": candidate,
                "features": features,
                "score": score,
            }
        )

    ranked = ranker.rank(ranked)[:25]

    for item in ranked:
        item["reasoning"] = _reason(item["candidate"], jd_data, item["features"])

    return [_to_frontend_candidate(item, index + 1) for index, item in enumerate(ranked)]


@app.post("/api/jobs/analyze")
async def analyze_job(text: str = Form(""), file: UploadFile | None = File(None)):
    """
    Analyze a job description using Groq AI.
    
    Returns structured JD analysis (required skills, seniority, location, etc).
    Does NOT perform candidate ranking.
    """
    global _current_jd_analysis
    
    if not Settings.GROQ_API_KEY:
        logger.error("GROQ_API_KEY is not set")
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not set in the environment.")

    jd_text = text or ""
    logger.info(f"Analyzing JD - text length: {len(text)}, file: {file.filename if file else 'None'}")

    try:
        # Extract text from uploaded .docx file if provided
        if file is not None and file.filename:
            if not file.filename.lower().endswith(".docx"):
                logger.warning(f"Invalid file format: {file.filename}")
                raise HTTPException(status_code=400, detail="Please upload a .docx job description.")
            
            logger.info(f"Extracting text from {file.filename}...")
            file_text = await _read_docx(file)
            jd_text = f"{jd_text}\n{file_text}".strip()
            logger.info(f"Extracted {len(file_text)} characters from .docx file")

        # Clean and validate JD text
        jd_text = clean_text(jd_text)
        
        if not jd_text:
            logger.warning("No JD text provided")
            raise HTTPException(
                status_code=400,
                detail="Paste a JD or upload a .docx file before running analysis."
            )

        logger.info(f"Sending JD for Groq analysis (length: {len(jd_text)})")
        
        # Analyze JD using Groq
        jd_data = JDAnalyzer().analyze(jd_text)
        
        # Store current session's JD analysis
        _current_jd_analysis = {
            "jd_text": jd_text,
            "jd_data": jd_data
        }
        
        logger.info(f"JD analysis successful. Required skills: {jd_data.get('required_skills', [])}")
        
        # Return frontend-formatted analysis
        return {
            "success": True,
            "analysis": _to_frontend_analysis(jd_data),
            "raw_jd_data": jd_data  # For debugging
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing JD: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze job description: {str(e)}"
        )


@app.post("/api/candidates/rank")
async def rank_candidates(payload: dict = Body(default={})):
    """
    Rank candidates using the provided JD data or current session's analyzed JD.
    """
    global _last_ranked_candidates, _current_jd_analysis
    
    logger.info("Starting candidate ranking pipeline...")
    
    try:
        # Extract jd_data from request body or use current session
        jd_data = None
        if payload and isinstance(payload, dict):
            jd_data = payload.get("jd_data")
        
        if jd_data is None:
            if _current_jd_analysis is None:
                raise HTTPException(
                    status_code=400,
                    detail="No JD analysis available. Please analyze a JD first."
                )
            jd_data = _current_jd_analysis["jd_data"]
        
        logger.info(f"Ranking candidates for: {jd_data.get('role', 'Unknown role')}")
        
        # Load candidates (with graceful error handling)
        try:
            candidates = _load_candidates()
            if not candidates:
                raise HTTPException(
                    status_code=500,
                    detail="No candidates available to rank"
                )
        except Exception as e:
            logger.error(f"Failed to load candidates: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to load candidate database"
            )
        
        # Perform ranking pipeline
        ranked_candidates = _rank_candidates(jd_data)
        _last_ranked_candidates = ranked_candidates
        
        logger.info(f"Successfully ranked candidates. Top 25 returned.")
        
        return {
            "success": True,
            "candidates": ranked_candidates,
            "total_ranked": len(ranked_candidates)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ranking candidates: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to rank candidates: {str(e)}"
        )


@app.get("/api/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    for candidate in _last_ranked_candidates:
        if candidate["id"] == candidate_id:
            return candidate

    raise HTTPException(status_code=404, detail="Candidate not found in current ranking.")


@app.post("/api/clear-session")
def clear_session():
    """Clear the current session's JD analysis and ranking results."""
    global _current_jd_analysis, _last_ranked_candidates
    _current_jd_analysis = None
    _last_ranked_candidates = []
    logger.info("Session cleared")
    return {"success": True, "message": "Session cleared successfully"}
