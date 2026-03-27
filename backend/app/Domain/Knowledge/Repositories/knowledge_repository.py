from abc import ABC, abstractmethod
from typing import Optional
from app.Domain.Knowledge.Entities.knowledge_base import KnowledgeBase


class KnowledgeRepositoryInterface(ABC):
    @abstractmethod
    async def find_active_by_user(self, user_id: str) -> Optional[KnowledgeBase]: ...

    @abstractmethod
    async def deactivate_all_by_user(self, user_id: str) -> None: ...

    @abstractmethod
    async def create(self, kb: KnowledgeBase) -> KnowledgeBase: ...
