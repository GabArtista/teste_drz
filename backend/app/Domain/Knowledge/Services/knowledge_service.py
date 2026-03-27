import uuid
from typing import Optional
from app.Domain.Knowledge.Entities.knowledge_base import KnowledgeBase
from app.Domain.Knowledge.Repositories.knowledge_repository import KnowledgeRepositoryInterface
from app.Exceptions.domain_exceptions import NoKnowledgeBaseException


class KnowledgeService:
    def __init__(self, repo: KnowledgeRepositoryInterface):
        self.repo = repo

    async def upload(self, user_id: str, text: str) -> KnowledgeBase:
        await self.repo.deactivate_all_by_user(user_id)
        kb = KnowledgeBase(
            id=str(uuid.uuid4()),
            user_id=user_id,
            text=text.strip(),
            char_count=len(text.strip()),
        )
        return await self.repo.create(kb)

    async def get_active(self, user_id: str) -> KnowledgeBase:
        kb = await self.repo.find_active_by_user(user_id)
        if not kb:
            raise NoKnowledgeBaseException()
        return kb

    async def get_active_optional(self, user_id: str) -> Optional[KnowledgeBase]:
        return await self.repo.find_active_by_user(user_id)
