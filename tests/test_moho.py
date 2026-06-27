# tests/test_moho.py

import sys
import os

# Include root in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intelligence.optimizer import MultiObjectiveHiringOptimizer

def test_moho_integration():
    print("Initializing MultiObjectiveHiringOptimizer...")
    moho = MultiObjectiveHiringOptimizer()
    
    # Mock candidates list
    candidates = [
        {
            "candidate_id": "cand_a",
            "name": "Candidate A",
            "score": 92.0,
            "experience": 6.5,
            "salary": 24.0,
            "notice_period": 30,
            "skills": [{"name": "Python"}, {"name": "AWS"}, {"name": "Docker"}]
        },
        {
            "candidate_id": "cand_b",
            "name": "Candidate B",
            "score": 88.0,
            "experience": 4.0,
            "salary": 14.5,
            "notice_period": 15,
            "skills": [{"name": "Python"}, {"name": "AWS"}]
        },
        {
            "candidate_id": "cand_c",
            "name": "Candidate C",
            "score": 75.0,
            "experience": 2.0,
            "salary": 8.0,
            "notice_period": 7,
            "skills": [{"name": "Python"}]
        }
    ]
    
    constraints = {
        "salary_max": 30.0,
        "joining_max": 60,
        "experience_min": 2,
        "required_skills": ["python"]
    }
    
    print("Running optimization pipeline...")
    res = moho.run_optimization(
        candidates=candidates,
        constraints=constraints,
        strategy="future_growth",
        scenario_id="startup"
    )
    
    assert res is not None
    assert "recommended_candidate" in res
    assert "pareto_frontier" in res
    assert "nsga2_frontier" in res
    assert "monte_carlo" in res
    
    print("MOHO Integration Test completed successfully!")
    print(f"Recommended candidate: {res['recommended_candidate']['name']}")
    print(f"Pareto Frontier Count: {len(res['pareto_frontier'])}")

if __name__ == "__main__":
    test_moho_integration()
