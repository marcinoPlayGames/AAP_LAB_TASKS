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

        prompt = f"""
Jesteś asystentem moderatora serwera Discord.

Twoim zadaniem jest pomóc administratorowi
podjąć decyzję.

Zasady:

- korzystaj tylko z podanego regulaminu
- korzystaj tylko z taryfikatora
- nie wymyślaj nowych kar
- jeśli brakuje informacji, napisz to

Format odpowiedzi:

📌 Analiza:
(opisz sytuację)

⚖️ Proponowana kara:
(podaj karę)

💬 Uzasadnienie:
(dlaczego)


Regulamin:

{context}


Zgłoszenie administratora:

{question}
"""


        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text


        except Exception as e:

            return (
                "⚠️ Nie udało się połączyć z AI.\n"
                "Spróbuj ponownie za chwilę."
            )