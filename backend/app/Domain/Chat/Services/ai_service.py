from abc import ABC, abstractmethod


class AIServiceInterface(ABC):
    @abstractmethod
    async def ask(self, question: str, knowledge_text: str) -> str: ...
