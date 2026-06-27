# tests/test_rmg.py

import sys
import os

# Include root in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intelligence.recruiter_memory import RecruiterMemoryGraphManager

def test_rmg_integration():
    print("Initializing RecruiterMemoryGraphManager...")
    rmg = RecruiterMemoryGraphManager()
    
    # Mock candidates
    candidates = [
        {
            "candidate_id": "cand_x",
            "name": "Candidate X",
            "score": 90.0,
            "communication_score": 85,
            "leadership_score": 88,
            "learning_velocity": 0.8,
            "retention_probability": 0.85,
            "redrob_signals": {
                "github_activity_score": 92,
                "has_open_source_contributions": True,
                "salary_requirement": 20.0
            }
        },
        {
            "candidate_id": "cand_y",
            "name": "Candidate Y",
            "score": 75.0,
            "communication_score": 60,
            "leadership_score": 50,
            "learning_velocity": 0.6,
            "retention_probability": 0.90,
            "redrob_signals": {
                "github_activity_score": 40,
                "has_open_source_contributions": False,
                "salary_requirement": 10.0
            }
        }
    ]
    
    actions = [
        {"recruiter_id": "rec_01", "candidate_id": "cand_x", "action": "hired"},
        {"recruiter_id": "rec_01", "candidate_id": "cand_y", "action": "rejected"}
    ]
    
    print("Running RMG profiling pipeline...")
    res = rmg.process_recruiter_profile(
        recruiter_id="rec_01",
        candidates=candidates,
        actions=actions
    )
    
    assert res is not None
    assert "preferences" in res
    assert "behavior" in res
    assert "personalized_candidates" in res
    assert "dna" in res
    assert "visualization" in res
    
    print("RMG Integration Test completed successfully!")
    print(f"Top Candidate after Personalization: {res['personalized_candidates'][0]['name']}")
    print(f"GitHub Preference Weight: {res['preferences']['github']}")
    print(f"Risk Tolerance Metric: {res['behavior']['risk_tolerance']}")

if __name__ == "__main__":
    test_rmg_integration()
