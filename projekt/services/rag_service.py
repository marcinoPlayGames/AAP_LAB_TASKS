from abc import ABC, abstractmethod


class RAGService(ABC):

    @abstractmethod
    async def retrieve(self, query: str) -> list[str]:
        pass