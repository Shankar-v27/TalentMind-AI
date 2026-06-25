import os
import logging
from groq import Groq
from config.settings import Settings

logger = logging.getLogger(__name__)


class GroqClient:

    def __init__(self):
        self.api_key = Settings.GROQ_API_KEY
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}. Falling back to mock responses.")
                self.client = None
        else:
            logger.warning("GROQ_API_KEY not found in environment. Running in mock offline mode.")
            self.client = None

    def generate(
        self,
        prompt,
        temperature=0.2
    ):
        if not self.client:
            # Fallback to mock response based on prompt type
            if "hiring reason" in prompt or "candidate_id" in prompt:
                import re
                import json
                # Extract candidate IDs from prompt
                candidate_ids = re.findall(r"'candidate_id':\s*'([^']+)'", prompt)
                if not candidate_ids:
                    candidate_ids = re.findall(r'"candidate_id":\s*"([^"]+)"', prompt)
                
                mock_reasons = [
                    {
                        "candidate_id": cid,
                        "reasoning": "Strong technical match with hands-on experience in Python, LLMs, and RAG pipelines. Excellent behavioral signals."
                    }
                    for cid in candidate_ids
                ]
                return json.dumps(mock_reasons)
            else:
                return """
{
    "role": "Senior Machine Learning Engineer",
    "required_skills": ["Python", "LLMs", "RAG", "Embeddings", "FAISS", "FastAPI"],
    "preferred_skills": ["LangChain", "Vector Databases", "MLOps"],
    "seniority": "Senior IC",
    "min_experience": 5.0,
    "domain": "AI Search and Recruitment Intelligence",
    "location": "Bengaluru / Remote",
    "work_mode": "Hybrid"
}
"""

        try:
            response = self.client.chat.completions.create(
                model=Settings.GROQ_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API call failed: {e}. Falling back to mock response.")
            if "hiring reason" in prompt or "candidate_id" in prompt:
                import re
                import json
                candidate_ids = re.findall(r"'candidate_id':\s*'([^']+)'", prompt)
                if not candidate_ids:
                    candidate_ids = re.findall(r'"candidate_id":\s*"([^"]+)"', prompt)
                mock_reasons = [
                    {
                        "candidate_id": cid,
                        "reasoning": "Strong technical match with hands-on experience in Python, LLMs, and RAG pipelines. Excellent behavioral signals."
                    }
                    for cid in candidate_ids
                ]
                return json.dumps(mock_reasons)
            else:
                return """
{
    "role": "Senior Machine Learning Engineer",
    "required_skills": ["Python", "LLMs", "RAG", "Embeddings", "FAISS", "FastAPI"],
    "preferred_skills": ["LangChain", "Vector Databases", "MLOps"],
    "seniority": "Senior IC",
    "min_experience": 5.0,
    "domain": "AI Search and Recruitment Intelligence",
    "location": "Bengaluru / Remote",
    "work_mode": "Hybrid"
}
"""