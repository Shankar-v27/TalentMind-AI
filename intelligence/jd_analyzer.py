# intelligence/jd_analyzer.py

import json
import re

from utils.groq_client import GroqClient


class JDAnalyzer:

    def __init__(self):
        self.llm = GroqClient()

    def _empty_result(self):
        return {
            "required_skills": [],
            "preferred_skills": [],
            "seniority": "",
            "min_experience": 0,
            "domain": "",
            "location": "",
            "work_mode": ""
        }

    def _parse_response(self, response):
        """
        Groq occasionally wraps valid JSON in markdown fences or short prose.
        Extract the JSON object instead of falling back to empty requirements.
        """

        if not response:
            return self._empty_result()

        text = response.strip()

        if text.startswith("```"):
            text = re.sub(
                r"^```\s*(?:json)?\s*|\s*```\s*$",
                "",
                text,
                flags=re.IGNORECASE
            ).strip()

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")

            if start == -1 or end == -1 or end <= start:
                raise

            parsed = json.loads(text[start:end + 1])

        result = self._empty_result()
        result.update(parsed)

        result["required_skills"] = [
            str(skill).strip()
            for skill in result.get("required_skills", [])
            if str(skill).strip()
        ]

        result["preferred_skills"] = [
            str(skill).strip()
            for skill in result.get("preferred_skills", [])
            if str(skill).strip()
        ]

        try:
            result["min_experience"] = float(
                result.get("min_experience", 0) or 0
            )
        except (TypeError, ValueError):
            result["min_experience"] = 0

        return result


    def analyze(self, job_description):
        """
        Convert unstructured JD into structured JSON
        """

        prompt = f"""
You are an expert AI recruiter.

Analyze the job description and return ONLY a valid JSON.

Return this format:

{{
    "required_skills": [],
    "preferred_skills": [],
    "seniority": "",
    "min_experience": 0,
    "domain": "",
    "location": "",
    "work_mode": ""
}}

Job Description:
{job_description}
"""


        response = self.llm.generate(
            prompt,
            temperature=0.1
        )


        try:
            return self._parse_response(response)

        except Exception as e:

            print("JSON parsing failed")
            print(response)

            return self._empty_result()
