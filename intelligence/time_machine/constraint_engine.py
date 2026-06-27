# intelligence/time_machine/constraint_engine.py

from typing import Dict, List, Any

class ConstraintEngine:
    def check_constraints(self, candidate: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates a candidate against constraint thresholds.
        Returns check statuses and overall eligibility.
        """
        # Read constraints
        min_exp = float(constraints.get("experience", 0))
        max_salary = float(constraints.get("salary", 9999999)) # In LPA or thousands
        max_joining = float(constraints.get("joining", 180)) # Notice period in days
        
        cand_exp = float(candidate.get("experience", 0.0) or 0.0)
        
        # Determine candidate salary (fallback if not present)
        cand_signals = candidate.get("redrob_signals", {})
        cand_salary = float(candidate.get("salary", cand_signals.get("salary_requirement", 12.0) or 12.0))
        
        # Notice period
        cand_notice = float(candidate.get("notice_period", cand_signals.get("notice_period_days", 30) or 30))
        
        # Check conditions
        exp_pass = cand_exp >= min_exp
        salary_pass = cand_salary <= max_salary
        joining_pass = cand_notice <= max_joining
        
        # Skill matching constraints
        required_skills = constraints.get("skills", [])
        cand_skills = [s.get("name", "").lower() for s in candidate.get("skills", []) if s.get("name")]
        
        missing_mandatory = []
        for r_skill in required_skills:
            if r_skill.lower() not in cand_skills:
                missing_mandatory.append(r_skill)
                
        skills_pass = len(missing_mandatory) == 0
        
        eligible = exp_pass and salary_pass and joining_pass and skills_pass
        
        return {
            "eligible": eligible,
            "checks": {
                "experience": {"passed": exp_pass, "value": cand_exp, "required": min_exp},
                "salary": {"passed": salary_pass, "value": cand_salary, "allowed_max": max_salary},
                "joining": {"passed": joining_pass, "value": cand_notice, "allowed_max": max_joining},
                "skills": {"passed": skills_pass, "missing": missing_mandatory}
            }
        }
