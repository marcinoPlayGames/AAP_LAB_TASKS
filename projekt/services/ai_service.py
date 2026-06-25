from google import genai
from config import GEMINI_API_KEY

class AIService:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_response(
        self,
        question,
        context
    ):

        return f"""
Na podstawie znalezionego kontekstu:

{context}

Możliwa decyzja moderatora:
Sprawdź zgłoszenie dotyczące: {question}
"""