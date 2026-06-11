# explainability/reason_generator.py


import json
import time

from utils.groq_client import GroqClient
from config.settings import Settings


class ReasonGenerator:


    def __init__(self):

        self.llm = GroqClient()


    def generate_batch(
        self,
        candidates,
        jd_data
    ):

        prompt_candidates = []


        for c in candidates:

            prompt_candidates.append({

                "candidate_id":
                    c["candidate_id"],

                "score":
                    c["score"],

                "skills":
                    c["features"]["skills"],

                "experience":
                    c["features"]["experience"],

                "reliability":
                    c["features"]["reliability"]
            })


        prompt = f"""
You are an expert technical recruiter.

For every candidate generate a short hiring reason.

Return ONLY valid JSON.

Format:

[
 {{
   "candidate_id": 123,
   "reasoning": "Strong ML engineer..."
 }}
]

Candidates:

{prompt_candidates}

Job Requirements:

{jd_data}

Maximum 40 words per candidate.
"""


        for attempt in range(
            Settings.GROQ_MAX_RETRIES
        ):

            try:

                response = self.llm.generate(
                    prompt,
                    temperature=0.2
                )


                result = json.loads(
                    response
                )


                return result


            except Exception as e:

                print(
                    f"Groq retry {attempt + 1}"
                )

                time.sleep(
                    Settings.GROQ_RETRY_DELAY
                )


        return []