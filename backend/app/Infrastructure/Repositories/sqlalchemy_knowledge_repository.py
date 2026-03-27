from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.Domain.Knowledge.Entities.knowledge_base import KnowledgeBase
from app.Domain.Knowledge.Repositories.knowledge_repository import KnowledgeRepositoryInterface
from app.Models.knowledge_base_model import KnowledgeBaseModel


class SQLAlchemyKnowledgeRepository(KnowledgeRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_active_by_user(self, user_id: str) -> Optional[KnowledgeBase]:
        result = await self.db.execute(
            select(KnowledgeBaseModel)
            .where(KnowledgeBaseModel.user_id == user_id)
            .where(KnowledgeBaseModel.is_active == True)  # noqa: E712
            .order_by(KnowledgeBaseModel.created_at.desc())
            .limit(1)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def deactivate_all_by_user(self, user_id: str) -> None:
        await self.db.execute(
            update(KnowledgeBaseModel)
            .where(KnowledgeBaseModel.user_id == user_id)
            .values(is_active=False)
        )
        await self.db.commit()

    async def create(self, kb: KnowledgeBase) -> KnowledgeBase:
        model = KnowledgeBaseModel(
            id=kb.id,
            user_id=kb.user_id,
            text=kb.text,
            char_count=kb.char_count,
            is_active=kb.is_active,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: KnowledgeBaseModel) -> KnowledgeBase:
        return KnowledgeBase(
            id=model.id,
            user_id=model.user_id,
            text=model.text,
            char_count=model.char_count,
            is_active=model.is_active,
            created_at=model.created_at,
        )
