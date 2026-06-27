# intelligence/gap_analyzer.py

from typing import Dict, List, Any

class GapAnalyzer:
    def analyze(self, candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze gaps between candidate profile and job requirements.
        """
        # 1. Skills gap
        cand_skills = set(s.get("name", "").lower() for s in candidate.get("skills", []) if s.get("name"))
        req_skills = [s.lower() for s in job.get("required_skills", [])]
        pref_skills = [s.lower() for s in job.get("preferred_skills", [])]
        
        all_req_skills = req_skills if req_skills else ["python", "fastapi", "docker", "kubernetes", "aws"]
        missing_skills = [s for s in all_req_skills if s not in cand_skills]
        
        # 2. Experience gap
        cand_exp = float(candidate.get("profile", {}).get("years_of_experience", 0.0) or 0.0)
        req_exp = float(job.get("min_experience", 0.0) or 0.0)
        missing_exp_months = max(0, int(round((req_exp - cand_exp) * 12)))
        
        # 3. Projects gap
        has_production = any("production" in str(h.get("description", "")).lower() for h in candidate.get("career_history", []))
        has_microservices = any("microservice" in str(h.get("description", "")).lower() for h in candidate.get("career_history", []))
        missing_projects = []
        if not has_production:
            missing_projects.append("production deployment")
        if not has_microservices:
            missing_projects.append("microservice architecture")
            
        # 4. Certifications gap
        cert_names = [c.get("name", "").lower() for c in candidate.get("certifications", [])]
        missing_certs = []
        if "aws" in all_req_skills and not any("aws" in c for c in cert_names):
            missing_certs.append("AWS Certified Solutions Architect")
        if "kubernetes" in all_req_skills and not any("ckad" in c or "cka" in c for c in cert_names):
            missing_certs.append("Certified Kubernetes Application Developer (CKAD)")

        # 5. Leadership gap
        leadership_score = float(candidate.get("candidate_dna", {}).get("leadership", 0.5) or 0.5)
        missing_leadership = leadership_score < 0.7
        
        # 6. Domain knowledge gap
        cand_domain = str(candidate.get("profile", {}).get("headline", "")).lower()
        job_domain = str(job.get("domain", "")).lower()
        missing_domain = job_domain not in cand_domain and job_domain != ""

        # 7. Communication gap
        comm_score = float(candidate.get("candidate_dna", {}).get("communication", 0.5) or 0.5)
        missing_comm = comm_score < 0.65

        # 8. Organizational fit gap
        org_fit_score = float(candidate.get("dna_match", {}).get("organization_match", 0.8) or 0.8)
        missing_org_fit = org_fit_score < 0.75

        return {
            "missing_skills": missing_skills,
            "missing_experience_months": missing_exp_months,
            "missing_projects": missing_projects,
            "missing_certifications": missing_certs,
            "missing_leadership": missing_leadership,
            "missing_domain": missing_domain,
            "missing_communication": missing_comm,
            "missing_org_fit": missing_org_fit
        }
