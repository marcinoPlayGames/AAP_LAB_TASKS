class AIService:

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