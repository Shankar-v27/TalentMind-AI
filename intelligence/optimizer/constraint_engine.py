# intelligence/optimizer/constraint_engine.py

from typing import Dict, List, Any

class ConstraintEngine:
    def evaluate_constraints(self, candidate: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates constraint satisfaction for a candidate.
        """
        # Load candidate stats
        cand_exp = float(candidate.get("experience", 0.0) or 0.0)
        signals = candidate.get("redrob_signals", {})
        cand_salary = float(candidate.get("salary", signals.get("salary_requirement", 18.0) or 18.0))
        cand_notice = float(candidate.get("notice_period", signals.get("notice_period_days", 30) or 30))
        
        # Load constraints
        salary_max = float(constraints.get("salary_max", 999.0))
        joining_max = float(constraints.get("joining_max", 180.0))
        experience_min = float(constraints.get("experience_min", 0.0))
        
        # Evaluations
        salary_pass = cand_salary <= salary_max
        joining_pass = cand_notice <= joining_max
        exp_pass = cand_exp >= experience_min
        
        # Skill constraint
        req_skills = [s.lower() for s in constraints.get("required_skills", [])]
        cand_skills = [s.get("name", "").lower() for s in candidate.get("skills", []) if s.get("name")]
        missing = [s for s in req_skills if s not in cand_skills]
        skills_pass = len(missing) == 0
        
        eligible = salary_pass and joining_pass and exp_pass and skills_pass
        
        return {
            "eligible": eligible,
            "checks": {
                "salary": {"passed": salary_pass, "value": cand_salary, "max": salary_max},
                "joining": {"passed": joining_pass, "value": cand_notice, "max": joining_max},
                "experience": {"passed": exp_pass, "value": cand_exp, "min": experience_min},
                "skills": {"passed": skills_pass, "missing": missing}
            }
        }
