from abc import ABC, abstractmethod


class ModerationService(ABC):

    @abstractmethod
    async def mute(self, user_id: int):
        pass