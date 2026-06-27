import logging
from io import BytesIO
# pyrefly: ignore [missing-import]
from docx import Document
from pypdf import PdfReader
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware

from config.settings import Settings
from intelligence.jd_analyzer import JDAnalyzer
from preprocessing.cleaner import clean_text
from preprocessing.parser import load_candidates
from ranking.feature_builder import FeatureBuilder
from ranking.ranker import CandidateRanker
from ranking.scorer import FinalScorer
from intelligence.digital_twin import DigitalTwinGenerator
from ranking.future_scorer import FutureScorer

# New Organizational DNA Matching Engine Imports
from intelligence.candidate_dna import CandidateDNA
from intelligence.organization_dna import OrganizationDNA
from intelligence.dna_similarity import DNASimilarity
from intelligence.team_compatibility import TeamCompatibilityEngine
from intelligence.culture_failure import CultureFailurePredictor
from intelligence.future_culture import FutureCultureEngine
from intelligence.personality_engine import PersonalityEngine
from intelligence.explainability_engine import ExplainabilityEngine
from ranking.organization_score import OrganizationScorer
from intelligence.counterfactual_engine import CounterfactualEngine
from intelligence.risk_simulator.engine import HiringRiskSimulatorEngine
from agents.orchestrator import AgentOrchestrator
from intelligence.career_forecasting.trajectory_forecaster import CareerTrajectoryForecastingEngine
from intelligence.team_compatibility.compatibility_orchestrator import TeamCompatibilityOrchestrator
from intelligence.skill_evolution.evolution_orchestrator import SkillEvolutionOrchestrator
from intelligence.digital_twin.twin_orchestrator import TalentTwinOrchestrator
from intelligence.time_machine import (
    StateManager,
    WeightEngine,
    ConstraintEngine,
    ScenarioEngine,
    SimulationEngine,
    RealtimeRanker,
    SensitivityEngine,
    StabilityEngine,
    CandidateMovementEngine,
    CounterfactualEngine as TMCounterfactualEngine,
    OptimizationEngine,
    ImpactEngine,
    TimeMachineExplainabilityEngine,
    TimeMachineVisualizationEngine
)
from intelligence.optimizer import MultiObjectiveHiringOptimizer
from intelligence.recruiter_memory import RecruiterMemoryGraphManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TalentMind AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_candidates_cache = None
_last_ranked_candidates = []
_current_jd_analysis = None  # Store current session's JD analysis

tm_state = StateManager()
tm_weights = WeightEngine()
tm_constraints = ConstraintEngine()
tm_scenarios = ScenarioEngine()
tm_simulation = SimulationEngine()
tm_ranker = RealtimeRanker()
tm_sensitivity = SensitivityEngine()
tm_stability = StabilityEngine()
tm_movement = CandidateMovementEngine()
tm_counterfactual = TMCounterfactualEngine()
tm_optimization = OptimizationEngine()
tm_impact = ImpactEngine()
tm_explain = TimeMachineExplainabilityEngine()
tm_visual = TimeMachineVisualizationEngine()

moho_optimizer = MultiObjectiveHiringOptimizer()
rmg_manager = RecruiterMemoryGraphManager()





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


async def _read_pdf(upload: UploadFile) -> str:
    """Extract plain text from an uploaded PDF file using pypdf."""
    contents = await upload.read()
    reader = PdfReader(BytesIO(contents))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text.strip())
    return "\n".join(pages_text)


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
        "score": item["score"],
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
        
        # DNA matching variables
        "candidate_dna": item["candidate_dna"],
        "organization_dna": item["organization_dna"],
        "dna_match": item["sim_data"],
        "team_compatibility": item["team_compatibility"],
        "culture_failure": item["culture_failure"],
        "future_growth": item["future_growth"],
        "personality": item["personality"]
    }


def _rank_candidates(jd_data):
    candidates = _prefilter_candidates(_load_candidates(), jd_data)
    feature_builder = FeatureBuilder()
    scorer = FinalScorer()
    ranked = []

    # Detect company type
    company_type = "corporate"
    jd_desc_lower = (jd_data.get("role", "") + " " + " ".join(jd_data.get("required_skills", []))).lower()
    if any(kw in jd_desc_lower for kw in ["startup", "early stage", "fast-paced", "disrupt", "agile"]):
        company_type = "startup"
    elif any(kw in jd_desc_lower for kw in ["government", "agency", "federal", "ministry", "public sector", "compliance"]):
        company_type = "government"

    # Instantiate Engines
    cand_dna_eng = CandidateDNA()
    org_dna_eng = OrganizationDNA()
    similarity_eng = DNASimilarity()
    team_comp_eng = TeamCompatibilityEngine()
    failure_eng = CultureFailurePredictor()
    future_eng = FutureCultureEngine()
    personality_eng = PersonalityEngine()
    org_scorer = OrganizationScorer()
    explain_eng = ExplainabilityEngine()

    company_dna = org_dna_eng.generate(company_type)

    for candidate in candidates:
        features = feature_builder.build(candidate, jd_data)
        skill_match_score = scorer.calculate(features)
        
        c_dna = cand_dna_eng.generate(candidate)
        sim_data = similarity_eng.calculate(c_dna, company_dna)
        team_comp = team_comp_eng.calculate({}, c_dna)
        fail_data = failure_eng.calculate(c_dna, sim_data, team_comp)
        
        current_role = candidate.get("career_history", [{}])[0].get("title", "Software Engineer")
        fut_growth = future_eng.simulate(c_dna, sim_data, current_role)
        personality = personality_eng.calculate(candidate)
        
        # Calculate Final Organization Score
        org_scores = org_scorer.calculate(
            skill_match=skill_match_score,
            organization_match=sim_data["organization_match"],
            leadership=c_dna["leadership"],
            innovation=c_dna["innovation"],
            communication=c_dna["communication"],
            learning=c_dna["learning"],
            retention=c_dna["stability"],
            team_compatibility=team_comp["compatibility"]
        )
        final_score = org_scores["organization_score"]
        
        explain_text = explain_eng.explain(
            candidate_name=candidate.get("profile", {}).get("anonymized_name") or candidate.get("candidate_id"),
            candidate_dna=c_dna,
            sim_data=sim_data,
            personality=personality,
            future_data=fut_growth,
            failure_data=fail_data
        )

        ranked.append(
            {
                "candidate_id": candidate["candidate_id"],
                "candidate": candidate,
                "features": features,
                "score": final_score,
                "candidate_dna": c_dna,
                "organization_dna": company_dna,
                "sim_data": sim_data,
                "team_compatibility": team_comp,
                "culture_failure": fail_data,
                "future_growth": fut_growth,
                "personality": personality,
                "reasoning": explain_text
            }
        )

    # Sort candidates by composite organization score
    ranked.sort(key=lambda x: x["score"], reverse=True)
    ranked = ranked[:25]

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
        logger.warning("GROQ_API_KEY is not set. Proceeding in mock offline mode.")

    jd_text = text or ""
    logger.info(f"Analyzing JD - text length: {len(text)}, file: {file.filename if file else 'None'}")

    try:
        # Extract text from uploaded .docx or .pdf file if provided
        if file is not None and file.filename:
            fname_lower = file.filename.lower()
            if fname_lower.endswith(".docx"):
                logger.info(f"Extracting text from DOCX: {file.filename}")
                file_text = await _read_docx(file)
            elif fname_lower.endswith(".pdf"):
                logger.info(f"Extracting text from PDF: {file.filename}")
                file_text = await _read_pdf(file)
                if not file_text.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Could not extract text from this PDF. It may be a scanned image. Please paste the JD text manually."
                    )
            else:
                logger.warning(f"Unsupported file format: {file.filename}")
                raise HTTPException(status_code=400, detail="Please upload a .docx or .pdf job description file.")
            jd_text = f"{jd_text}\n{file_text}".strip()
            logger.info(f"Extracted {len(file_text)} characters from file")

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
    global _current_jd_analysis
    for candidate in _last_ranked_candidates:
        if candidate["id"] == candidate_id:
            if "counterfactual" not in candidate:
                try:
                    job = _current_jd_analysis["jd_data"] if _current_jd_analysis else {
                        "required_skills": ["python", "fastapi", "docker", "kubernetes", "aws"],
                        "min_experience": 5.0,
                        "domain": "DevOps"
                    }
                    current_score = float(candidate.get("score", 85.0))
                    cf_data = CounterfactualEngine().run_all(candidate, job, current_score, 1)
                    candidate["counterfactual"] = cf_data
                except Exception as ex:
                    logger.error(f"Failed to generate counterfactual for candidate {candidate_id}: {ex}")
            
            if "risk_profile" not in candidate:
                try:
                    # Resolve full candidate metadata
                    cand_data = {}
                    try:
                        candidates = _load_candidates()
                        for c in candidates:
                            if c.get("candidate_id") == candidate_id:
                                cand_data = c
                                break
                    except Exception:
                        pass
                    if not cand_data:
                        cand_data = candidate
                        
                    risk_data = HiringRiskSimulatorEngine().run_simulation(cand_data)
                    candidate["risk_profile"] = risk_data
                except Exception as ex:
                    logger.error(f"Failed to generate risk profile for candidate {candidate_id}: {ex}")
            
            if "debate_committee" not in candidate:
                try:
                    # Resolve full candidate metadata
                    cand_data = {}
                    try:
                        candidates = _load_candidates()
                        for c in candidates:
                            if c.get("candidate_id") == candidate_id:
                                cand_data = c
                                break
                    except Exception:
                        pass
                    if not cand_data:
                        cand_data = candidate
                    
                    if "risk_profile" in candidate:
                        cand_data["risk_profile"] = candidate["risk_profile"]
                        
                    debate_data = AgentOrchestrator().run_board(cand_data)
                    candidate["debate_committee"] = debate_data
                except Exception as ex:
                    logger.error(f"Failed to generate debate board for candidate {candidate_id}: {ex}")
            
            if "career_forecast" not in candidate:
                try:
                    # Resolve full candidate metadata
                    cand_data = {}
                    try:
                        candidates = _load_candidates()
                        for c in candidates:
                            if c.get("candidate_id") == candidate_id:
                                cand_data = c
                                break
                    except Exception:
                        pass
                    if not cand_data:
                        cand_data = candidate
                    
                    if "risk_profile" in candidate:
                        cand_data["risk_profile"] = candidate["risk_profile"]
                        
                    forecast_data = CareerTrajectoryForecastingEngine().run_forecasts(cand_data)
                    candidate["career_forecast"] = forecast_data
                except Exception as ex:
                    logger.error(f"Failed to generate career forecasts for candidate {candidate_id}: {ex}")
            
            if "team_compatibility" not in candidate:
                try:
                    # Resolve full candidate metadata
                    cand_data = {}
                    try:
                        candidates = _load_candidates()
                        for c in candidates:
                            if c.get("candidate_id") == candidate_id:
                                cand_data = c
                                break
                    except Exception:
                        pass
                    if not cand_data:
                        cand_data = candidate
                    
                    if "risk_profile" in candidate:
                        cand_data["risk_profile"] = candidate["risk_profile"]
                        
                    compat_data = TeamCompatibilityOrchestrator().run_simulation(cand_data)
                    candidate["team_compatibility"] = compat_data
                except Exception as ex:
                    logger.error(f"Failed to run team compatibility simulation for candidate {candidate_id}: {ex}")
            
            if "skill_evolution" not in candidate:
                try:
                    # Resolve full candidate metadata
                    cand_data = {}
                    try:
                        candidates = _load_candidates()
                        for c in candidates:
                            if c.get("candidate_id") == candidate_id:
                                cand_data = c
                                break
                    except Exception:
                        pass
                    if not cand_data:
                        cand_data = candidate
                    
                    if "risk_profile" in candidate:
                        cand_data["risk_profile"] = candidate["risk_profile"]
                        
                    skill_data = SkillEvolutionOrchestrator().run_forecasting(cand_data)
                    candidate["skill_evolution"] = skill_data
                except Exception as ex:
                    logger.error(f"Failed to run skill evolution forecasting for candidate {candidate_id}: {ex}")
            
            if "digital_twin" not in candidate:
                try:
                    # Resolve full candidate metadata
                    cand_data = {}
                    try:
                        candidates = _load_candidates()
                        for c in candidates:
                            if c.get("candidate_id") == candidate_id:
                                cand_data = c
                                break
                    except Exception:
                        pass
                    if not cand_data:
                        cand_data = candidate
                    
                    if "risk_profile" in candidate:
                        cand_data["risk_profile"] = candidate["risk_profile"]
                        
                    twin_data = TalentTwinOrchestrator().run_twin(cand_data)
                    candidate["digital_twin"] = twin_data
                except Exception as ex:
                    logger.error(f"Failed to run digital twin simulation for candidate {candidate_id}: {ex}")
                    
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


@app.post("/api/copilot/chat")
async def copilot_chat(payload: dict = Body(default={})):
    """AI Copilot chat assistant helping recruiter with queries."""
    message = payload.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required.")

    global _last_ranked_candidates, _current_jd_analysis

    context = ""
    if _current_jd_analysis:
        context += f"Job Description Requirements: {_current_jd_analysis.get('jd_data')}\n"
    if _last_ranked_candidates:
        # Extract basic info from top candidates for context
        candidate_summary = [
            {
                "name": c.get("name"),
                "score": c.get("score"),
                "skills": c.get("skills", []),
                "experience": c.get("experience", ""),
                "location": c.get("location", "")
            }
            for c in _last_ranked_candidates[:10]
        ]
        context += f"Top Ranked Candidates in Session: {candidate_summary}\n"

    prompt = f"""
You are the TalentMind AI Recruiter Copilot, a helpful AI assistant aiding a recruiter.

Context of current recruitment session:
{context}

Recruiter's query:
{message}

Answer the recruiter's query professionally, concisely, and contextually based on the candidate details provided (if any). Maximum 100 words.
"""
    try:
        from utils.groq_client import GroqClient
        llm = GroqClient()
        response = llm.generate(prompt)
        
        # Parse potential JSON response from mock fallback
        import json
        answer = response
        try:
            parsed = json.loads(response)
            if isinstance(parsed, list) and len(parsed) > 0 and "reasoning" in parsed[0]:
                answer = parsed[0]["reasoning"]
        except Exception:
            pass

        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error in copilot chat: {e}")
        return {"answer": "I'm having trouble answering right now. Please try again."}


# =========================================================
# Part 18: Organizational DNA Matching API Design
# =========================================================

def _get_candidate_by_id_or_data(payload: dict) -> dict:
    candidate = payload.get("candidate")
    if not candidate and payload.get("candidate_id"):
        try:
            candidates = _load_candidates()
            for c in candidates:
                if c.get("candidate_id") == payload.get("candidate_id"):
                    candidate = c
                    break
        except Exception:
            pass
    if not candidate:
        # Graceful fallback mock candidate
        candidate = {
            "candidate_id": payload.get("candidate_id") or "CAND_FALLBACK",
            "profile": {
                "headline": "Full-Stack Engineer",
                "summary": "Experienced engineer with a background in designing high-velocity AI platforms and distributed systems."
            },
            "skills": [
                {"name": "Python", "duration_months": 36, "endorsements": 8},
                {"name": "FastAPI", "duration_months": 24, "endorsements": 4}
            ],
            "career_history": [
                {"title": "Software Engineer", "description": "Led team processes and designed R&D platforms."}
            ],
            "education": [{"tier": "tier_1", "degree": "B.Tech", "school": "IIT"}],
            "redrob_signals": {
                "recruiter_response_rate": 0.85,
                "interview_completion_rate": 0.90,
                "offer_acceptance_rate": 0.80,
                "github_activity_score": 75,
                "willing_to_relocate": True
            }
        }
    return candidate


@app.post("/api/dna/candidate")
def get_candidate_dna(payload: dict = Body(default={})):
    """Calculate and return a candidate's 20-dimensional personality DNA vector."""
    candidate = _get_candidate_by_id_or_data(payload)
    dna = CandidateDNA().generate(candidate)
    return {"dna": dna}


@app.post("/api/dna/company")
def get_company_dna(payload: dict = Body(default={})):
    """Retrieve the multidimensional DNA vector for a specified organization type (startup, corporate, government)."""
    company_type = payload.get("company_type", "corporate")
    custom_dims = payload.get("custom_dimensions")
    dna = OrganizationDNA().generate(company_type, custom_dims)
    return {"dna": dna}


@app.post("/api/dna/match")
def match_dna(payload: dict = Body(default={})):
    """Calculate similarity metrics (cosine, Euclidean, Manhattan, weighted) between candidate and company DNA."""
    candidate_dna = payload.get("candidate_dna")
    organization_dna = payload.get("organization_dna")
    
    if not candidate_dna or not organization_dna:
        # If parameters not provided, compute from sample/default
        candidate = _get_candidate_by_id_or_data(payload)
        candidate_dna = CandidateDNA().generate(candidate)
        organization_dna = OrganizationDNA().generate(payload.get("company_type", "corporate"))
        
    similarity = DNASimilarity().calculate(candidate_dna, organization_dna)
    return similarity


@app.post("/api/team/compatibility")
def get_team_compatibility(payload: dict = Body(default={})):
    """Calculate collaborative compatibility, conflict probability, and team synergy indices."""
    candidate_dna = payload.get("candidate_dna")
    team_dna = payload.get("team_dna", {})
    
    if not candidate_dna:
        candidate = _get_candidate_by_id_or_data(payload)
        candidate_dna = CandidateDNA().generate(candidate)
        
    compatibility = TeamCompatibilityEngine().calculate(team_dna, candidate_dna)
    return compatibility


@app.post("/api/culture/predict")
def predict_culture_failure(payload: dict = Body(default={})):
    """Predict culture mismatch, performance degradation hazards, resignation, and burnout probabilities."""
    candidate_dna = payload.get("candidate_dna")
    org_match = payload.get("organization_match_data")
    team_comp = payload.get("team_compatibility_data")
    
    if not candidate_dna or not org_match or not team_comp:
        candidate = _get_candidate_by_id_or_data(payload)
        candidate_dna = CandidateDNA().generate(candidate)
        company_dna = OrganizationDNA().generate(payload.get("company_type", "corporate"))
        org_match = DNASimilarity().calculate(candidate_dna, company_dna)
        team_comp = TeamCompatibilityEngine().calculate({}, candidate_dna)
        
    failure_data = CultureFailurePredictor().calculate(candidate_dna, org_match, team_comp)
    return failure_data


@app.post("/api/future/growth")
def predict_future_growth(payload: dict = Body(default={})):
    """Simulate 6-to-36 month adaptability, leadership potential maturation, and future roles."""
    candidate_dna = payload.get("candidate_dna")
    org_match = payload.get("organization_match_data")
    current_role = payload.get("current_role", "Software Engineer")
    
    if not candidate_dna or not org_match:
        candidate = _get_candidate_by_id_or_data(payload)
        candidate_dna = CandidateDNA().generate(candidate)
        company_dna = OrganizationDNA().generate(payload.get("company_type", "corporate"))
        org_match = DNASimilarity().calculate(candidate_dna, company_dna)
        current_role = candidate.get("career_history", [{}])[0].get("title", "Software Engineer")
        
    growth_data = FutureCultureEngine().simulate(candidate_dna, org_match, current_role)
    return growth_data


@app.post("/api/personality/analyze")
def analyze_personality(payload: dict = Body(default={})):
    """Classify the candidate profile into primary, secondary, and tertiary personality personas."""
    candidate = _get_candidate_by_id_or_data(payload)
    personality = PersonalityEngine().calculate(candidate)
    return personality


# =========================================================
# Part 22: Counterfactual Hiring AI Endpoints
# =========================================================

@app.post("/api/counterfactual/analyze")
def analyze_counterfactual(payload: dict = Body(default={})):
    """Calculate complete counterfactual hiring simulation for a candidate."""
    candidate = _get_candidate_by_id_or_data(payload)
    company_type = payload.get("company_type") or payload.get("company", "corporate")
    company_dna = OrganizationDNA().generate(company_type)
    job = payload.get("job") or {
        "required_skills": ["python", "fastapi", "docker", "kubernetes", "aws"],
        "min_experience": 5.0,
        "domain": "DevOps"
    }
    
    current_score = float(candidate.get("score") or payload.get("ranking_score", 89))
    target_rank = int(payload.get("target_rank", 1))
    
    cf_data = CounterfactualEngine().run_all(candidate, job, current_score, target_rank)
    return cf_data


@app.post("/api/counterfactual/skills")
def counterfactual_skills(payload: dict = Body(default={})):
    """Determine which skills are missing to reach the target rank."""
    candidate = _get_candidate_by_id_or_data(payload)
    job = payload.get("job") or {"required_skills": ["python", "fastapi", "docker", "kubernetes", "aws"]}
    gaps = GapAnalyzer().analyze(candidate, job)
    skills_cf = SkillCounterfactual().evaluate(gaps)
    return skills_cf


@app.post("/api/counterfactual/experience")
def counterfactual_experience(payload: dict = Body(default={})):
    """Analyze additional months of experience required."""
    candidate = _get_candidate_by_id_or_data(payload)
    job = payload.get("job") or {"min_experience": 5.0}
    current_score = float(payload.get("current_score", 85.0))
    gaps = GapAnalyzer().analyze(candidate, job)
    exp_cf = ExperienceCounterfactual().evaluate(gaps, current_score)
    return exp_cf


@app.post("/api/counterfactual/projects")
def counterfactual_projects(payload: dict = Body(default={})):
    """Determine what missing projects would optimize hiring probability."""
    candidate = _get_candidate_by_id_or_data(payload)
    job = payload.get("job") or {}
    gaps = GapAnalyzer().analyze(candidate, job)
    proj_cf = ProjectCounterfactual().evaluate(gaps)
    return proj_cf


@app.post("/api/counterfactual/career")
def counterfactual_career(payload: dict = Body(default={})):
    """Evaluate and optimize career progression paths."""
    candidate = _get_candidate_by_id_or_data(payload)
    career_cf = CareerCounterfactual().evaluate(candidate)
    return career_cf


@app.post("/api/counterfactual/salary")
def counterfactual_salary(payload: dict = Body(default={})):
    """Compute salary multipliers based on upskilling paths."""
    skills_to_learn = payload.get("skills_to_learn") or ["Kubernetes", "Terraform"]
    salary_cf = SalaryCounterfactual().evaluate(skills_to_learn)
    return salary_cf


@app.post("/api/counterfactual/retention")
def counterfactual_retention(payload: dict = Body(default={})):
    """Formulate optimal retention strategy suggestions."""
    candidate = _get_candidate_by_id_or_data(payload)
    retention_cf = RetentionCounterfactual().evaluate(candidate)
    return retention_cf


@app.post("/api/counterfactual/future")
def counterfactual_future(payload: dict = Body(default={})):
    """Simulate future score progression values."""
    current_score = float(payload.get("current_score", 85.0))
    optimal_gain = float(payload.get("optimal_gain", 10.0))
    future_cf = FutureCounterfactual().evaluate(current_score, optimal_gain)
    return future_cf


@app.post("/api/counterfactual/explain")
def counterfactual_explain(payload: dict = Body(default={})):
    """Generate Natural Language recruiter explanations for counterfactual options."""
    explain_data = payload.get("explain_data") or {
        "name": "Candidate",
        "current_rank": 2,
        "current_score": 89,
        "potential_score": 98,
        "missing_skills": ["Kubernetes", "Production deployment"],
        "cost": "₹15,000",
        "months": 6,
        "success_probability": 0.87,
        "future_role": "Senior DevOps Architect"
    }
    explanation = CounterfactualExplainabilityEngine().explain(explain_data)
    return {"explanation": explanation}


# =========================================================
# Part 23: Hiring Risk Simulator & Workforce Outcome Endpoints
# =========================================================

@app.post("/api/risk/offer")
def predict_offer_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate will accept the job offer."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().offer_acc.predict(candidate, payload)


@app.post("/api/risk/ghosting")
def predict_ghosting_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate will ghost the interview."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().ghosting.predict(candidate, payload)


@app.post("/api/risk/joining")
def predict_joining_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate will actually join on the start date."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().joining.predict(candidate, payload)


@app.post("/api/risk/retention")
def predict_retention_risk(payload: dict = Body(default={})):
    """Predict retention probability over multiple milestones (3-60 months)."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().retention.predict(candidate, payload)


@app.post("/api/risk/resignation")
def predict_resignation_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate will resign within 24 months."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().resignation.predict(candidate, payload)


@app.post("/api/risk/burnout")
def predict_burnout_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate will experience significant career burnout."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().burnout.predict(candidate, payload)


@app.post("/api/risk/promotion")
def predict_promotion_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate will earn a promotion within 12-24 months."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().promotion.predict(candidate, payload)


@app.post("/api/risk/leadership")
def predict_leadership_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate becomes a key leader."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().leadership.predict(candidate, payload)


@app.post("/api/risk/salary")
def predict_salary_risk(payload: dict = Body(default={})):
    """Evaluate and project compensation progression (LPA) over 1, 2, 5, and 10 years."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().salary.predict(candidate, payload)


@app.post("/api/risk/teamlead")
def predict_teamlead_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate secures a Team Lead role."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().teamlead.predict(candidate, payload)


@app.post("/api/risk/manager")
def predict_manager_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate secures a Manager role."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().manager.predict(candidate, payload)


@app.post("/api/risk/director")
def predict_director_risk(payload: dict = Body(default={})):
    """Evaluate probability that the candidate secures a Director role."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().director.predict(candidate, payload)


@app.post("/api/risk/success")
def predict_success_risk(payload: dict = Body(default={})):
    """Evaluate future success score and performance categorization."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().success.predict(candidate, payload)


@app.post("/api/risk/simulate")
def simulate_workforce_risks(payload: dict = Body(default={})):
    """Orchestrate full workforce prediction and risk simulation."""
    candidate = _get_candidate_by_id_or_data(payload)
    return HiringRiskSimulatorEngine().run_simulation(candidate, payload)


# =========================================================
# Part 28: AI Hiring Debate System Endpoints
# =========================================================

@app.post("/api/debate/start")
def start_debate(payload: dict = Body(default={})):
    """Initialize hiring board debate for a candidate."""
    candidate = _get_candidate_by_id_or_data(payload)
    if "risk_profile" in candidate:
        pass
    else:
        candidate["risk_profile"] = HiringRiskSimulatorEngine().run_simulation(candidate)
    return AgentOrchestrator().run_board(candidate, payload)


@app.post("/api/debate/round")
def debate_round(payload: dict = Body(default={})):
    """Retrieve multi-round debate conversations."""
    candidate = _get_candidate_by_id_or_data(payload)
    return AgentOrchestrator().debate.simulate_debate(candidate, payload)


@app.post("/api/debate/negotiate")
def debate_negotiate(payload: dict = Body(default={})):
    """Negotiate initial hire and reject confidence thresholds."""
    hire_conf = float(payload.get("hire_confidence", 0.90))
    reject_conf = float(payload.get("reject_confidence", 0.80))
    return AgentOrchestrator().negotiation.negotiate(hire_conf, reject_conf)


@app.post("/api/debate/vote")
def debate_vote(payload: dict = Body(default={})):
    """Consensus voting engine result."""
    candidate = _get_candidate_by_id_or_data(payload)
    return AgentOrchestrator().consensus.vote(candidate, payload)


@app.post("/api/debate/judge")
def debate_judge(payload: dict = Body(default={})):
    """Arbitrate final decision by Judge Agent."""
    summary = payload.get("debate_summary") or {"consensus": {"decision": "HIRE", "consensus_percentage": 83}}
    return AgentOrchestrator().judge.evaluate(summary)


@app.post("/api/debate/simulate")
def debate_simulate(payload: dict = Body(default={})):
    """Run 1,000 Monte Carlo hiring committee simulations."""
    candidate = _get_candidate_by_id_or_data(payload)
    return AgentOrchestrator().sim.simulate(candidate)


@app.post("/api/debate/explain")
def debate_explain(payload: dict = Body(default={})):
    """Generate Natural Language committee decision explainability."""
    candidate = _get_candidate_by_id_or_data(payload)
    orchestrated = AgentOrchestrator().run_board(candidate, payload)
    return {"explanation": orchestrated.get("explanation")}


# =========================================================
# Part 22: Career Trajectory Forecasting Engine Endpoints
# =========================================================

@app.post("/api/career/forecast")
def get_career_forecast(payload: dict = Body(default={})):
    """Orchestrate full career forecasting model predictions."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().run_forecasts(candidate, payload)


@app.post("/api/career/velocity")
def get_career_velocity(payload: dict = Body(default={})):
    """Evaluate vertical levels growth rate per year."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().velocity.calculate(candidate, payload)


@app.post("/api/career/promotions")
def get_career_promotions(payload: dict = Body(default={})):
    """Evaluate promotion milestones and probabilities."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().promotion.predict(candidate, payload)


@app.post("/api/career/timeline")
def get_career_timeline(payload: dict = Body(default={})):
    """Generate expected career level progression years list."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().timeline.generate(candidate, payload)


@app.post("/api/career/skills")
def get_career_skills(payload: dict = Body(default={})):
    """Forecast future skills acquisition path."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().skills.predict(candidate, payload)


@app.post("/api/career/ceiling")
def get_career_ceiling(payload: dict = Body(default={})):
    """Evaluate career ceiling limits and confidence scores."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().ceiling.predict(candidate, payload)


@app.post("/api/career/founder")
def get_career_founder(payload: dict = Body(default={})):
    """Predict founder track likelihood percentage."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().founder.predict(candidate, payload)


@app.post("/api/career/executive")
def get_career_executive(payload: dict = Body(default={})):
    """Predict VP/CTO executive tier target possibilities."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().executive.predict(candidate, payload)


@app.post("/api/career/simulation")
def get_career_simulation(payload: dict = Body(default={})):
    """Simulate startup vs corporate vs FAANG progression trajectories."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().simulator.simulate(candidate, payload)


@app.post("/api/career/value")
def get_career_value(payload: dict = Body(default={})):
    """Calculate current and future human capital valuations."""
    candidate = _get_candidate_by_id_or_data(payload)
    return CareerTrajectoryForecastingEngine().value.calculate(candidate, payload)


# =========================================================
# Part 23: Team Compatibility & Simulation Endpoints
# =========================================================

@app.post("/api/team/dna")
def get_team_dna(payload: dict = Body(default={})):
    """Retrieve candidate, team, and organization DNA profiles."""
    candidate = _get_candidate_by_id_or_data(payload)
    orch = TeamCompatibilityOrchestrator()
    cand_dna = orch.cand_builder.build(candidate)
    team_dna = orch.team_builder.build(payload.get("team_profile"))
    org_dna = orch.org_builder.build(payload.get("org_profile"))
    return {
        "candidate_dna": cand_dna,
        "team_dna": team_dna,
        "org_dna": org_dna
    }


@app.post("/api/team/compatibility")
def get_team_compatibility(payload: dict = Body(default={})):
    """Calculate integrated team compatibility score."""
    candidate = _get_candidate_by_id_or_data(payload)
    orch = TeamCompatibilityOrchestrator()
    cand_dna = orch.cand_builder.build(candidate)
    team_dna = orch.team_builder.build(payload.get("team_profile"))
    org_dna = orch.org_builder.build(payload.get("org_profile"))
    return orch.compat.calculate(cand_dna, team_dna, org_dna)


@app.post("/api/team/conflict")
def get_team_conflict(payload: dict = Body(default={})):
    """Predict conflict probability metrics."""
    candidate = _get_candidate_by_id_or_data(payload)
    orch = TeamCompatibilityOrchestrator()
    cand_dna = orch.cand_builder.build(candidate)
    team_dna = orch.team_builder.build(payload.get("team_profile"))
    return orch.conflict.evaluate(cand_dna, team_dna)


@app.post("/api/team/diversity")
def get_team_diversity(payload: dict = Body(default={})):
    """Evaluate cognitive knowledge diversity score."""
    candidate = _get_candidate_by_id_or_data(payload)
    orch = TeamCompatibilityOrchestrator()
    team_dna = orch.team_builder.build(payload.get("team_profile"))
    return orch.diversity.evaluate(candidate, team_dna)


@app.post("/api/team/productivity")
def get_team_productivity(payload: dict = Body(default={})):
    """Predict team productivity gain rates."""
    candidate = _get_candidate_by_id_or_data(payload)
    orch = TeamCompatibilityOrchestrator()
    cand_dna = orch.cand_builder.build(candidate)
    team_dna = orch.team_builder.build(payload.get("team_profile"))
    return orch.prod.evaluate(cand_dna, team_dna)


@app.post("/api/team/innovation")
def get_team_innovation(payload: dict = Body(default={})):
    """Predict team innovation boosts."""
    candidate = _get_candidate_by_id_or_data(payload)
    orch = TeamCompatibilityOrchestrator()
    cand_dna = orch.cand_builder.build(candidate)
    team_dna = orch.team_builder.build(payload.get("team_profile"))
    return orch.innov.evaluate(cand_dna, team_dna)


@app.post("/api/team/simulation")
def get_team_simulation(payload: dict = Body(default={})):
    """Simulate team milestones changes over 2 years."""
    candidate = _get_candidate_by_id_or_data(payload)
    orch = TeamCompatibilityOrchestrator()
    cand_dna = orch.cand_builder.build(candidate)
    team_dna = orch.team_builder.build(payload.get("team_profile"))
    return orch.sim.simulate(cand_dna, team_dna)


@app.post("/api/team/montecarlo")
def get_team_montecarlo(payload: dict = Body(default={})):
    """Run 10,000 Monte Carlo team integration simulations."""
    candidate = _get_candidate_by_id_or_data(payload)
    orch = TeamCompatibilityOrchestrator()
    cand_dna = orch.cand_builder.build(candidate)
    team_dna = orch.team_builder.build(payload.get("team_profile"))
    org_dna = orch.org_builder.build(payload.get("org_profile"))
    comp = orch.compat.calculate(cand_dna, team_dna, org_dna)["compatibility"]
    conflict = orch.conflict.evaluate(cand_dna, team_dna)["conflict_probability"]
    return orch.mc.simulate(comp, conflict)


@app.post("/api/team/explain")
def get_team_explain(payload: dict = Body(default={})):
    """Generate Natural Language team simulation explainability."""
    candidate = _get_candidate_by_id_or_data(payload)
    res = TeamCompatibilityOrchestrator().run_simulation(candidate, payload)
    return {"explanation": res.get("explanation")}


# =========================================================
# Part 23: Skill Evolution & Potential Endpoints
# =========================================================

@app.post("/api/skills/timeline")
def get_skills_timeline(payload: dict = Body(default={})):
    """Retrieve historical skill acquisition timelines."""
    candidate = _get_candidate_by_id_or_data(payload)
    return SkillEvolutionOrchestrator().timeline.build_timeline(candidate)


@app.post("/api/skills/velocity")
def get_skills_velocity(payload: dict = Body(default={})):
    """Calculate skill learning velocity ratings."""
    candidate = _get_candidate_by_id_or_data(payload)
    timeline_data = SkillEvolutionOrchestrator().timeline.build_timeline(candidate)
    return SkillEvolutionOrchestrator().velocity.calculate(timeline_data)


@app.post("/api/skills/github")
def get_skills_github(payload: dict = Body(default={})):
    """Analyze repository and commit activity indicators."""
    candidate = _get_candidate_by_id_or_data(payload)
    return SkillEvolutionOrchestrator().github.analyze(candidate)


@app.post("/api/skills/project")
def get_skills_project(payload: dict = Body(default={})):
    """Evaluate complex project adoption rates."""
    candidate = _get_candidate_by_id_or_data(payload)
    return SkillEvolutionOrchestrator().proj_velocity.calculate(candidate)


@app.post("/api/skills/future")
def get_skills_future(payload: dict = Body(default={})):
    """Forecast future skills and strengths (NOW, 6M, 12M, 24M)."""
    candidate = _get_candidate_by_id_or_data(payload)
    extracted = SkillEvolutionOrchestrator().extractor.extract_skills(candidate)
    future_sk = SkillEvolutionOrchestrator().future.predict_future_skills(candidate)
    strengths = SkillEvolutionOrchestrator().future.forecast_strengths(extracted)
    return {
        "future_skills": future_sk.get("future_skills", []),
        "strengths": strengths
    }


@app.post("/api/skills/obsolescence")
def get_skills_obsolescence(payload: dict = Body(default={})):
    """Predict skill decay and obsolescence risk ratios."""
    candidate = _get_candidate_by_id_or_data(payload)
    return SkillEvolutionOrchestrator().obsolescence.predict_obsolescence(candidate)


@app.post("/api/skills/specialization")
def get_skills_specialization(payload: dict = Body(default={})):
    """Classify predicted specialization archetype tracks."""
    candidate = _get_candidate_by_id_or_data(payload)
    return SkillEvolutionOrchestrator().specialization.predict_specialization(candidate)


@app.post("/api/skills/leadership")
def get_skills_leadership(payload: dict = Body(default={})):
    """Predict 24-month leadership capacity growth."""
    candidate = _get_candidate_by_id_or_data(payload)
    return SkillEvolutionOrchestrator().leadership.predict_growth(candidate)


@app.post("/api/skills/career")
def get_skills_career(payload: dict = Body(default={})):
    """Forecast vertical career ladder milestones."""
    candidate = _get_candidate_by_id_or_data(payload)
    return SkillEvolutionOrchestrator().career.predict_evolution(candidate)


@app.post("/api/skills/simulation")
def get_skills_simulation(payload: dict = Body(default={})):
    """Simulate skill path scenarios (Startup, Corporate, Research)."""
    candidate = _get_candidate_by_id_or_data(payload)
    return SkillEvolutionOrchestrator().twin.simulate_scenarios(candidate)


@app.post("/api/skills/potential")
def get_skills_potential(payload: dict = Body(default={})):
    """Calculate overall human potential index."""
    candidate = _get_candidate_by_id_or_data(payload)
    timeline_data = SkillEvolutionOrchestrator().timeline.build_timeline(candidate)
    vel_res = SkillEvolutionOrchestrator().velocity.calculate(timeline_data)
    velocity = float(vel_res["learning_velocity"])
    return SkillEvolutionOrchestrator().potential.calculate(candidate, velocity)


@app.post("/api/skills/explain")
def get_skills_explain(payload: dict = Body(default={})):
    """Generate Natural Language explainability outputs."""
    candidate = _get_candidate_by_id_or_data(payload)
    res = SkillEvolutionOrchestrator().run_forecasting(candidate, payload)
    return {"explanation": res.get("explanation")}


# =========================================================
# Part 23: Talent Digital Twin Engine Endpoints
# =========================================================

@app.post("/api/digital-twin/create")
def create_digital_twin(payload: dict = Body(default={})):
    """Create complete candidate digital twin simulation model."""
    candidate = _get_candidate_by_id_or_data(payload)
    return TalentTwinOrchestrator().run_twin(candidate)


@app.post("/api/digital-twin/career")
def get_twin_career(payload: dict = Body(default={})):
    """Forecast future career timeline increments."""
    candidate = _get_candidate_by_id_or_data(payload)
    return TalentTwinOrchestrator().career.predict_career(candidate)


@app.post("/api/digital-twin/leadership")
def get_twin_leadership(payload: dict = Body(default={})):
    """Forecast today, y2, and y5 leadership indices."""
    candidate = _get_candidate_by_id_or_data(payload)
    return TalentTwinOrchestrator().leadership.predict_leadership(candidate)


@app.post("/api/digital-twin/retention")
def get_twin_retention(payload: dict = Body(default={})):
    """Predict retention probability rates."""
    candidate = _get_candidate_by_id_or_data(payload)
    return TalentTwinOrchestrator().retention.predict_retention(candidate)


@app.post("/api/digital-twin/promotion")
def get_twin_promotion(payload: dict = Body(default={})):
    """Predict multi-year promotion likelihoods."""
    candidate = _get_candidate_by_id_or_data(payload)
    return TalentTwinOrchestrator().promotion.predict_promotion(candidate)


@app.post("/api/digital-twin/burnout")
def get_twin_burnout(payload: dict = Body(default={})):
    """Evaluate psychological safety and stress burnout probability."""
    candidate = _get_candidate_by_id_or_data(payload)
    return TalentTwinOrchestrator().burnout.predict_burnout(candidate)


@app.post("/api/digital-twin/simulate")
def get_twin_simulate(payload: dict = Body(default={})):
    """Simulate milestones and organizational outcomes."""
    candidate = _get_candidate_by_id_or_data(payload)
    return TalentTwinOrchestrator().simulation.simulate(candidate)


@app.post("/api/digital-twin/montecarlo")
def get_twin_montecarlo(payload: dict = Body(default={})):
    """Run 10,000 Monte Carlo digital twin runs."""
    candidate = _get_candidate_by_id_or_data(payload)
    score_val = float(candidate.get("score", 85))
    return TalentTwinOrchestrator().mc.simulate(score_val)


@app.post("/api/digital-twin/explain")
def get_twin_explain(payload: dict = Body(default={})):
    """Generate Natural Language digital twin explanations."""
    candidate = _get_candidate_by_id_or_data(payload)
    res = TalentTwinOrchestrator().run_twin(candidate)
    return {"explanation": res.get("explanation")}


# =========================================================
# RECRUITER TIME MACHINE API ENDPOINTS
# =========================================================

@app.post("/api/timemachine/state")
def post_time_machine_state(payload: dict = Body(default={})):
    """Update current recruiter configuration state."""
    new_state = tm_state.update_state(payload)
    weights = tm_weights.calculate_weights(new_state)
    candidates = _load_candidates()
    ranked = tm_ranker.rank_candidates(candidates, new_state, weights, new_state)
    return {
        "state": new_state,
        "weights": weights,
        "rankings": ranked[:50] # return top 50
    }

@app.post("/api/timemachine/rank")
def post_time_machine_rank(payload: dict = Body(default={})):
    """Calculate rankings based on explicit weights/constraints."""
    state = payload.get("state") or tm_state.get_state()
    weights = tm_weights.calculate_weights(state)
    candidates = _load_candidates()
    ranked = tm_ranker.rank_candidates(candidates, state, weights, state)
    
    # Calculate optimization selections
    opt_selections = tm_optimization.optimize_hiring(candidates)
    
    return {
        "rankings": ranked[:50],
        "optimization": opt_selections
    }

@app.post("/api/timemachine/scenario")
def post_time_machine_scenario(payload: dict = Body(default={})):
    """Apply a pre-defined weight scenario preset."""
    scenario_id = payload.get("scenario_id", "high_skill")
    preset = tm_scenarios.get_preset(scenario_id)
    
    # Merge preset weights into current state
    current_s = tm_state.get_state()
    current_s.update({
        "skill_weight": preset["weights"].get("skill", 0.3),
        "experience_weight": preset["weights"].get("experience", 0.2),
        "leadership": preset["weights"].get("leadership", 0.3),
        "future_potential": preset["weights"].get("future", 0.3),
        "retention": preset["weights"].get("retention", 0.5),
        "risk": 1.0 - preset["weights"].get("risk", 0.5)
    })
    
    updated_state = tm_state.update_state(current_s)
    candidates = _load_candidates()
    ranked = tm_ranker.rank_candidates(candidates, updated_state, preset["weights"], updated_state)
    
    return {
        "preset": preset,
        "state": updated_state,
        "rankings": ranked[:50]
    }

@app.post("/api/timemachine/simulate")
def post_time_machine_simulate(payload: dict = Body(default={})):
    """Run 1,000 Monte Carlo simulation runs."""
    state = payload.get("state") or tm_state.get_state()
    candidates = _load_candidates()
    sim_runs = int(payload.get("runs", 200))
    results = tm_simulation.run_monte_carlo(candidates, state, tm_ranker, tm_weights, runs=sim_runs)
    return {"simulation_wins": results}

@app.post("/api/timemachine/stability")
def post_time_machine_stability(payload: dict = Body(default={})):
    """Calculate candidate ranking stability index."""
    state = payload.get("state") or tm_state.get_state()
    candidates = _load_candidates()
    stability = tm_stability.calculate_stability(candidates, state, tm_ranker, tm_weights)
    return {"stability": stability}

@app.post("/api/timemachine/sensitivity")
def post_time_machine_sensitivity(payload: dict = Body(default={})):
    """Calculate parameter sensitivity weight changes."""
    state = payload.get("state") or tm_state.get_state()
    candidates = _load_candidates()
    sensitivity = tm_sensitivity.analyze_sensitivity(candidates, state, tm_ranker, tm_weights, tm_constraints)
    return {"sensitivity": sensitivity}

@app.post("/api/timemachine/counterfactual")
def post_time_machine_counterfactual(payload: dict = Body(default={})):
    """Generate conditions needed for a candidate to reach Rank 1."""
    candidate_id = payload.get("candidate_id")
    if not candidate_id:
        raise HTTPException(status_code=400, detail="Missing candidate_id parameter")
    state = payload.get("state") or tm_state.get_state()
    candidates = _load_candidates()
    res = tm_counterfactual.explain_how_to_win(candidate_id, candidates, state, tm_ranker, tm_weights)
    return res

@app.post("/api/timemachine/movement")
def post_time_machine_movement(payload: dict = Body(default={})):
    """Track candidate movements between two states."""
    state1 = payload.get("baseline_state") or tm_state.get_state()
    state2 = payload.get("comparison_state")
    
    if not state2:
        # Create a mock slightly different state if comparison is not passed
        state2 = state1.copy()
        state2["experience"] = max(0, state2.get("experience", 5) - 2)
        
    candidates = _load_candidates()
    
    w1 = tm_weights.calculate_weights(state1)
    ranks1 = tm_ranker.rank_candidates(candidates, state1, w1, state1)
    
    w2 = tm_weights.calculate_weights(state2)
    ranks2 = tm_ranker.rank_candidates(candidates, state2, w2, state2)
    
    movement = tm_movement.calculate_movement(ranks1, ranks2)
    return {"movement": movement[:50]}

@app.post("/api/timemachine/explain")
def post_time_machine_explain(payload: dict = Body(default={})):
    """Generate explainability narrative for rank changes."""
    candidate_name = payload.get("candidate_name", "Candidate")
    old_rank = int(payload.get("old_rank", 5))
    new_rank = int(payload.get("new_rank", 1))
    old_state = payload.get("old_state") or tm_state.get_state()
    new_state = payload.get("new_state") or tm_state.get_state()
    score_diff = float(payload.get("score_diff", 12.0))
    
    explanation = tm_explain.explain_shift(
        candidate_name=candidate_name,
        old_rank=old_rank,
        new_rank=new_rank,
        old_state=old_state,
        new_state=new_state,
        score_diff=score_diff
    )
    return {"explanation": explanation}


# =========================================================
# MULTI-OBJECTIVE HIRING OPTIMIZER (MOHO) API ENDPOINTS
# =========================================================

@app.post("/api/optimizer/run")
def post_optimizer_run(payload: dict = Body(default={})):
    """Run full Multi-Objective Hiring Optimization loop."""
    candidates = _load_candidates()
    constraints = payload.get("constraints", {
        "salary_max": float(payload.get("salary_max", 45.0)),
        "joining_max": int(payload.get("joining_max", 90)),
        "experience_min": int(payload.get("experience_min", 2)),
        "required_skills": payload.get("required_skills", [])
    })
    strategy = payload.get("strategy", "future_growth")
    scenario_id = payload.get("scenario_id", "startup")
    
    res = moho_optimizer.run_optimization(
        candidates=candidates,
        constraints=constraints,
        strategy=strategy,
        scenario_id=scenario_id
    )
    return res

@app.post("/api/optimizer/pareto")
def post_optimizer_pareto(payload: dict = Body(default={})):
    """Retrieve Pareto Frontier coordinates."""
    candidates = _load_candidates()
    # Process objectives first
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
        
    objectives_list = ["quality", "salary", "joining", "retention", "future"]
    maximize_flags = [True, False, False, True, True]
    frontier = moho_optimizer.pareto.find_pareto_frontier(candidates, objectives_list, maximize_flags)
    frontier_with_crowd = moho_optimizer.pareto.calculate_crowding_distance(frontier, objectives_list)
    return {"frontier": frontier_with_crowd}

@app.post("/api/optimizer/nsga2")
def post_optimizer_nsga2(payload: dict = Body(default={})):
    """Run NSGA-II preference search."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
    objectives_list = ["quality", "salary", "joining", "retention", "future"]
    maximize_flags = [True, False, False, True, True]
    
    res = moho_optimizer.nsga2.optimize(candidates, objectives_list, maximize_flags)
    return {"nsga2_optimal": res}

@app.post("/api/optimizer/genetic")
def post_optimizer_genetic(payload: dict = Body(default={})):
    """Run single objective GA evolution."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
        
    # Example fitness maximizing quality and minimizing salary
    def fitness_fn(cand):
        objs = cand.get("objectives", {})
        return objs.get("quality", 70.0) - objs.get("salary", 15.0)
        
    res = moho_optimizer.genetic.evolve_selection(candidates, fitness_fn)
    return res

@app.post("/api/optimizer/montecarlo")
def post_optimizer_montecarlo(payload: dict = Body(default={})):
    """Execute 10,000 workforce outcome simulations."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
    res = moho_optimizer.mc.simulate_workforce(candidates, runs=1000)
    return res

@app.post("/api/optimizer/scenario")
def post_optimizer_scenario(payload: dict = Body(default={})):
    """Evaluate weights scenario mode."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
    scenario_id = payload.get("scenario_id", "startup")
    res = moho_optimizer.scenario.run_scenario(candidates, scenario_id)
    return res

@app.post("/api/optimizer/future")
def post_optimizer_future(payload: dict = Body(default={})):
    """Compare Current Value and Career Growth."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
    res = moho_optimizer.future_value.optimize_future_value(candidates)
    return res

@app.post("/api/optimizer/diversity")
def post_optimizer_diversity(payload: dict = Body(default={})):
    """Calculate cognitive/role diversity balance."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
        
    candidate = candidates[0]
    if payload.get("candidate_id"):
        candidate = next((c for c in candidates if c.get("candidate_id") == payload.get("candidate_id")), candidate)
        
    res = moho_optimizer.diversity.optimize_diversity(candidate, candidates[:5])
    return res

@app.post("/api/optimizer/team")
def post_optimizer_team(payload: dict = Body(default={})):
    """Evaluate candidate impact on team productivity."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
        
    candidate = candidates[0]
    if payload.get("candidate_id"):
        candidate = next((c for c in candidates if c.get("candidate_id") == payload.get("candidate_id")), candidate)
        
    res = moho_optimizer.team.optimize_team(candidate)
    return res

@app.post("/api/optimizer/risk")
def post_optimizer_risk(payload: dict = Body(default={})):
    """Calculate resignation, ghosting, and burnout metrics."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
        
    candidate = candidates[0]
    if payload.get("candidate_id"):
        candidate = next((c for c in candidates if c.get("candidate_id") == payload.get("candidate_id")), candidate)
        
    res = moho_optimizer.risk.optimize_risk(candidate)
    return res

@app.post("/api/optimizer/tradeoff")
def post_optimizer_tradeoff(payload: dict = Body(default={})):
    """Get tradeoffs matrix."""
    candidates = _load_candidates()
    for c in candidates:
        c["objectives"] = moho_optimizer.objective.calculate_objectives(c)
    res = moho_optimizer.tradeoff.analyze_tradeoffs(candidates)
    return res

@app.post("/api/optimizer/explain")
def post_optimizer_explain(payload: dict = Body(default={})):
    """Get explainability narrative."""
    candidate_name = payload.get("candidate_name", "Candidate")
    objectives = payload.get("objectives", {"quality": 88.0, "future": 92.0, "retention": 91.0, "learning": 84.0, "salary": 14.5, "joining": 15})
    res = moho_optimizer.explain.explain_selection(candidate_name, objectives, {})
    return res


# =========================================================
# RECRUITER MEMORY GRAPH (RMG) API ENDPOINTS
# =========================================================

@app.post("/api/recruiter/profile")
def post_recruiter_profile(payload: dict = Body(default={})):
    """Run full RMG calculation and return recruiter profile state."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    candidates = _load_candidates()
    actions = payload.get("actions", None)
    
    res = rmg_manager.process_recruiter_profile(
        recruiter_id=recruiter_id,
        candidates=candidates,
        actions=actions
    )
    return res

@app.post("/api/recruiter/memory")
def post_recruiter_memory(payload: dict = Body(default={})):
    """Logs a recruiter activity action."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    candidate_id = payload.get("candidate_id")
    action = payload.get("action", "viewed")
    
    if not candidate_id:
        return {"error": "Missing candidate_id"}
        
    res = rmg_manager.collector.record_activity(
        recruiter_id=recruiter_id,
        candidate_id=candidate_id,
        action=action
    )
    return res

@app.post("/api/recruiter/preferences")
def post_recruiter_preferences(payload: dict = Body(default={})):
    """Retrieve computed preferences."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    logs = rmg_manager.collector.get_recruiter_logs(recruiter_id)
    candidates = _load_candidates()
    candidates_map = {c.get("candidate_id"): c for c in candidates}
    
    prefs = rmg_manager.preference.calculate_preferences(logs, candidates_map)
    return {"preferences": prefs}

@app.post("/api/recruiter/predict")
def post_recruiter_predict(payload: dict = Body(default={})):
    """Predict probabilities of recruiter actions for a candidate."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    candidate_id = payload.get("candidate_id")
    candidates = _load_candidates()
    
    candidate = candidates[0]
    if candidate_id:
        candidate = next((c for c in candidates if c.get("candidate_id") == candidate_id), candidate)
        
    logs = rmg_manager.collector.get_recruiter_logs(recruiter_id)
    candidates_map = {c.get("candidate_id"): c for c in candidates}
    prefs = rmg_manager.preference.calculate_preferences(logs, candidates_map)
    behav = rmg_manager.behavior.calculate_behavior(logs, candidates_map)
    
    preds = rmg_manager.prediction.predict_action(candidate, prefs, behav)
    return preds

@app.post("/api/recruiter/recommend")
def post_recruiter_recommend(payload: dict = Body(default={})):
    """Generate candidates list recommendations based on RMG profile."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    candidates = _load_candidates()
    logs = rmg_manager.collector.get_recruiter_logs(recruiter_id)
    candidates_map = {c.get("candidate_id"): c for c in candidates}
    prefs = rmg_manager.preference.calculate_preferences(logs, candidates_map)
    behav = rmg_manager.behavior.calculate_behavior(logs, candidates_map)
    
    personalized = rmg_manager.personalization.personalize_rankings(candidates, prefs, behav, {})
    recs = rmg_manager.recommendation.generate_recommendations(personalized, prefs)
    return recs

@app.post("/api/recruiter/similarity")
def post_recruiter_similarity(payload: dict = Body(default={})):
    """Check target candidate similarity to past hired candidates."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    candidate_id = payload.get("candidate_id")
    candidates = _load_candidates()
    
    candidate = candidates[0]
    if candidate_id:
        candidate = next((c for c in candidates if c.get("candidate_id") == candidate_id), candidate)
        
    c_embed = rmg_manager.embedding.generate_candidate_embedding(candidate)
    
    logs = rmg_manager.collector.get_recruiter_logs(recruiter_id)
    hired_embeddings = []
    for log in logs:
        if log["action"] == "hired":
            c_obj = next((c for c in candidates if c.get("candidate_id") == log["candidate_id"]), None)
            if c_obj:
                h_embed = rmg_manager.embedding.generate_candidate_embedding(c_obj)
                hired_embeddings.append(h_embed)
                
    sim = rmg_manager.similarity.calculate_similarity_to_past_hires(candidate, hired_embeddings, c_embed)
    return {"similarity_index": sim}

@app.post("/api/recruiter/habits")
def post_recruiter_habits(payload: dict = Body(default={})):
    """Returns timeline and heatmap visualization structures."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    logs = rmg_manager.collector.get_recruiter_logs(recruiter_id)
    candidates = _load_candidates()
    candidates_map = {c.get("candidate_id"): c for c in candidates}
    prefs = rmg_manager.preference.calculate_preferences(logs, candidates_map)
    behav = rmg_manager.behavior.calculate_behavior(logs, candidates_map)
    
    visual_data = rmg_manager.visual.format_visualization(prefs, behav)
    return visual_data

@app.post("/api/recruiter/dna")
def post_recruiter_dna(payload: dict = Body(default={})):
    """Returns DNA profile metrics."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    logs = rmg_manager.collector.get_recruiter_logs(recruiter_id)
    candidates = _load_candidates()
    candidates_map = {c.get("candidate_id"): c for c in candidates}
    prefs = rmg_manager.preference.calculate_preferences(logs, candidates_map)
    behav = rmg_manager.behavior.calculate_behavior(logs, candidates_map)
    
    dna = rmg_manager.habit.compile_recruiter_dna(prefs, behav)
    return dna

@app.post("/api/recruiter/graph")
def post_recruiter_graph(payload: dict = Body(default={})):
    """Returns details of the Recruiter Knowledge Graph nodes."""
    recruiter_id = payload.get("recruiter_id", "recruiter_alpha")
    logs = rmg_manager.collector.get_recruiter_logs(recruiter_id)
    candidates = _load_candidates()
    candidates_map = {c.get("candidate_id"): c for c in candidates}
    
    rmg_manager.graph.build_recruiter_nodes(recruiter_id, logs, candidates_map)
    nodes_list = []
    edges_list = []
    for node in rmg_manager.graph.graph.nodes:
        nodes_list.append({
            "id": node,
            "type": rmg_manager.graph.graph.nodes[node].get("type", "unknown"),
            "name": rmg_manager.graph.graph.nodes[node].get("name", node)
        })
    for u, v in rmg_manager.graph.graph.edges:
        edges_list.append({
            "source": u,
            "target": v,
            "relation": rmg_manager.graph.graph[u][v].get("relation", "connected")
        })
    return {"nodes": nodes_list, "edges": edges_list}

@app.post("/api/recruiter/explain")
def post_recruiter_explain(payload: dict = Body(default={})):
    """Get explanation narrative."""
    candidate_name = payload.get("candidate_name", "Candidate")
    preferences = payload.get("preferences", {"communication": 0.85, "leadership": 0.72, "github": 0.90, "opensource": 0.80})
    candidate = payload.get("candidate", {"communication_score": 88, "leadership_score": 80})
    boost = float(payload.get("boost", 12.0))
    res = rmg_manager.explain.explain_personalization(candidate_name, preferences, candidate, boost)
    return res












