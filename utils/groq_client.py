from groq import Groq
from config.settings import Settings


class GroqClient:

    def __init__(self):
        self.client = Groq(
            api_key=Settings.GROQ_API_KEY
        )

    def generate(
        self,
        prompt,
        temperature=0.2
    ):

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