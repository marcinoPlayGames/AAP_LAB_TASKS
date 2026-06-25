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
        regulamin,
        taryfikator,
        kara
    ):

        prompt = f"""
Jesteś asystentem moderatora serwera Discord.

Twoim zadaniem jest pomóc administratorowi
podjąć decyzję.

Zasady:

- korzystaj wyłącznie z przekazanego regulaminu
- korzystaj wyłącznie z przekazanego taryfikatora
- nie wymyślaj nowych kar
- nie odwołuj się do wiedzy spoza przekazanego kontekstu
- jeżeli opis przewinienia w taryfikatorze jest semantycznie zgodny
  z opisem w regulaminie, traktuj je jako to samo przewinienie
- wpisy taryfikatora zostały wybrane przez system RAG jako
  najbardziej pasujące do zgłoszenia
- jeżeli w kontekście znajduje się proponowana kara,
  wykorzystaj ją jako rekomendację
- jeśli mimo tego brakuje informacji, napisz to

Interpretuj przekazane fragmenty regulaminu i taryfikatora jako wynik
wyszukiwania RAG. Nie oceniaj, czy są poprawnie dobrane — zakładaj,
że są najbardziej trafnymi fragmentami odpowiadającymi zgłoszeniu.

Format odpowiedzi:

📌 Analiza:
(opisz sytuację)

⚖️ Proponowana kara:
(podaj karę)

💬 Uzasadnienie:
(dlaczego)


Regulamin:

{regulamin}

Najbardziej pasujące wpisy taryfikatora:

{taryfikator}

Rekomendowana kara:

{kara}

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