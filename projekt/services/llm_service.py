from abc import ABC, abstractmethod


class LLMService(ABC):

    @abstractmethod
    async def ask(self, prompt: str) -> str:
        pass