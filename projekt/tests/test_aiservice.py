from services.ai_service import AIService

ai = AIService()

response = ai.generate_response(
    "spam",
    """
    Regulamin:
    §1 Zabrania się spamu.

    Taryfikator:
    Przewinienie: spam
    Kara: mute 2h
    """
)

print(response)