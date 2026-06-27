# tests/test_digital_twin.py

try:
    import pytest
except ImportError:
    # Fallback mock for environments without pytest
    class pytest:
        @staticmethod
        def fixture(func):
            return func

from intelligence.learning_velocity import LearningVelocityEngine
from intelligence.career_simulator import CareerSimulator
from intelligence.skill_evolution import SkillEvolutionPredictor
from intelligence.promotion_engine import PromotionEngine
from intelligence.retention_engine import RetentionEngine
from intelligence.burnout_engine import BurnoutEngine
from intelligence.organization_dna import OrganizationDNA
from intelligence.leadership_engine import LeadershipEngine
from intelligence.counterfactual_engine import CounterfactualEngine
from intelligence.future_simulator import FutureSimulator
from ranking.future_scorer import FutureScorer
from intelligence.digital_twin import DigitalTwinGenerator

def sample_candidate():
    return {
        "candidate_id": "CAND_TEST_99",
        "skills": [
            {"name": "python", "duration_months": 48, "endorsements": 8},
            {"name": "fastapi", "duration_months": 24, "endorsements": 4},
            {"name": "docker", "duration_months": 12, "endorsements": 2}
        ],
        "experience": 4.5,
        "career_history": [
            {"title": "Senior ML Engineer", "description": "Led backend retrieval systems and search index design using fastapi and python."},
            {"title": "Machine Learning Engineer", "description": "Shipped pipelines and model endpoints."},
            {"title": "Junior Developer", "description": "Assisted with data formatting."}
        ],
        "education": [
            {"tier": "tier_1", "degree": "B.Tech in CS", "school": "IIT Delhi"}
        ],
        "redrob_signals": {
            "recruiter_response_rate": 0.90,
            "interview_completion_rate": 0.85,
            "offer_acceptance_rate": 0.80,
            "open_to_work_flag": True,
            "applications_submitted_30d": 12,
            "willing_to_relocate": True,
            "github_activity_score": 85,
            "profile_completeness_score": 95,
            "search_appearance_30d": 210
        }
    }

def sample_jd():
    return {
        "role": "Senior AI Retrieval Engineer",
        "required_skills": ["python", "fastapi", "docker", "kubernetes"],
        "preferred_skills": ["aws", "terraform"],
        "min_experience": 5.0
    }

# Register fixtures for pytest
if hasattr(pytest, 'fixture') and not isinstance(pytest.fixture, type(lambda: None)):
    sample_candidate = pytest.fixture(sample_candidate)
    sample_jd = pytest.fixture(sample_jd)

def test_learning_velocity(sample_candidate):
    engine = LearningVelocityEngine()
    res = engine.calculate(sample_candidate)
    
    assert "learning_velocity" in res
    assert "learning_type" in res
    assert 0.0 <= res["learning_velocity"] <= 1.0
    assert res["learning_type"] in ["FAST_LEARNER", "STEADY_DEVELOPER", "CONVENTIONAL_PACER"]

def test_career_simulator(sample_candidate):
    engine = CareerSimulator()
    res = engine.simulate(sample_candidate)
    
    assert "career_acceleration" in res
    assert "predicted_role" in res
    assert "promotion_probability" in res
    assert res["current_level"] == 3  # Senior level

def test_skill_evolution(sample_candidate):
    engine = SkillEvolutionPredictor()
    res = engine.predict(sample_candidate, 0.8)
    
    assert "6_months" in res
    assert "12_months" in res
    assert "24_months" in res
    assert len(res["6_months"]) >= 1

def test_promotion_engine(sample_candidate):
    career_sim = CareerSimulator().simulate(sample_candidate)
    engine = PromotionEngine()
    res = engine.calculate(sample_candidate, career_sim, 0.8)
    
    assert "promotion_probability" in res
    assert "next_role" in res
    assert "promotion_time" in res
    assert 0.0 <= res["promotion_probability"] <= 1.0

def test_retention_engine(sample_candidate):
    career_sim = CareerSimulator().simulate(sample_candidate)
    engine = RetentionEngine()
    res = engine.calculate(sample_candidate, career_sim)
    
    assert "retention_probability" in res
    assert "attrition_risk" in res
    assert 0.0 <= res["retention_probability"] <= 1.0

def test_burnout_engine(sample_candidate):
    career_sim = CareerSimulator().simulate(sample_candidate)
    retention_res = RetentionEngine().calculate(sample_candidate, career_sim)
    engine = BurnoutEngine()
    res = engine.calculate(sample_candidate, 0.8, career_sim, retention_res)
    
    assert "burnout_probability" in res
    assert "risk" in res
    assert res["risk"] in ["HIGH", "MEDIUM", "LOW"]

def test_organization_dna(sample_candidate):
    career_sim = CareerSimulator().simulate(sample_candidate)
    engine = OrganizationDNA()
    res = engine.match(sample_candidate, 0.8, career_sim, "startup")
    
    assert "culture_fit" in res
    assert "work_style" in res
    assert 0.0 <= res["culture_fit"] <= 1.0

def test_leadership_engine(sample_candidate):
    career_sim = CareerSimulator().simulate(sample_candidate)
    engine = LeadershipEngine()
    res = engine.predict(sample_candidate, career_sim, 0.8)
    
    assert "current" in res
    assert "36_months" in res
    assert res["36_months"] >= res["current"]

def test_counterfactual_engine(sample_candidate, sample_jd):
    engine = CounterfactualEngine()
    res = engine.explain(sample_candidate, sample_jd)
    
    assert "missing_skills" in res
    assert "missing_experience" in res
    assert "predicted_rank_after_changes" in res

def test_future_simulator(sample_candidate):
    career_sim = CareerSimulator().simulate(sample_candidate)
    promo_res = PromotionEngine().calculate(sample_candidate, career_sim, 0.8)
    engine = FutureSimulator()
    res = engine.simulate(career_sim, promo_res)
    
    assert "2026" in res
    assert "2031" in res

def test_future_scorer(sample_candidate):
    twin = DigitalTwinGenerator().generate(sample_candidate, {})
    engine = FutureScorer()
    res = engine.calculate(0.85, twin)
    
    assert "current_fit" in res
    assert "future_fit" in res
    assert "future_score" in res
    assert 0 <= res["future_score"] <= 100

def test_digital_twin_generator(sample_candidate, sample_jd):
    generator = DigitalTwinGenerator()
    twin = generator.generate(sample_candidate, sample_jd)
    
    assert "learning_velocity" in twin
    assert "career_acceleration" in twin
    assert "skill_evolution" in twin
    assert "promotion_probability" in twin
    assert "retention_probability" in twin
    assert "burnout_probability" in twin
    assert "culture_fit" in twin
    assert "leadership_potential" in twin
    assert "counterfactual" in twin
    assert "timeline" in twin
