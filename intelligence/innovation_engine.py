# intelligence/innovation_engine.py

from typing import Dict, Any

class InnovationEngine:
    def calculate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        skills = candidate.get("skills", [])
        signals = candidate.get("redrob_signals", {})
        
        # Combine text fields
        text = (profile.get("summary", "") + " " + " ".join(j.get("description", "") for j in history) + " " + " ".join(j.get("title", "") for j in history)).lower()
        
        patents = "patent" in text
        publications = any(word in text for word in ["publication", "research paper", "thesis", "ieee", "arxiv", "conference paper"])
        hackathons = "hackathon" in text
        
        # Count new technologies
        new_tech_keywords = ["llm", "rag", "generative ai", "embeddings", "vector search", "faiss", "pytorch", "transformers", "nlp", "reinforcement learning", "fine-tuning"]
        new_tech_count = sum(1 for word in new_tech_keywords if word in text or any(word in skill.get("name", "").lower() for skill in skills))
        
        side_projects = any(word in text for word in ["side project", "hobby project", "built a custom", "created an app"])
        experiments = any(word in text for word in ["experiment", "a/b test", "hypothesis", "prototyped"])
        open_source = any(word in text for word in ["open source", "open-source", "github contribution"]) or signals.get("github_activity_score", 0) > 50
        rd_experience = any(word in text for word in ["r&d", "research and development", "labs", "researcher", "scientist"])
        
        tech_diversity = len(skills)
        
        # Weighted score
        score = 0.1
        if patents: score += 0.30
        if publications: score += 0.20
        if hackathons: score += 0.15
        if open_source: score += 0.10
        if rd_experience: score += 0.10
        if side_projects: score += 0.10
        if experiments: score += 0.10
        score += (min(5, new_tech_count) / 5.0) * 0.15
        score += (min(10, tech_diversity) / 10.0) * 0.10
        
        # Add deterministic variation from candidate ID
        cand_id_num = int("".join(filter(str.isdigit, candidate.get("candidate_id", "0") or "0")) or "0")
        seed_offset = (cand_id_num % 13) / 100.0
        score = max(0.1, min(0.99, score + seed_offset))
        
        if score >= 0.80:
            innovation_class = "HIGH"
        elif score >= 0.50:
            innovation_class = "MODERATE"
        else:
            innovation_class = "STANDARD"
            
        return {
            "innovation_score": round(score, 2),
            "innovation_class": innovation_class
        }
