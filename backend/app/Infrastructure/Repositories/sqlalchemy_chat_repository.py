from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.Domain.Chat.Entities.chat_session import ChatSession
from app.Domain.Chat.Entities.message import Message
from app.Domain.Chat.Repositories.chat_repository import ChatRepositoryInterface
from app.Models.chat_session_model import ChatSessionModel
from app.Models.message_model import MessageModel


class SQLAlchemyChatRepository(ChatRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_session_by_id(self, session_id: str) -> Optional[ChatSession]:
        result = await self.db.execute(
            select(ChatSessionModel).where(ChatSessionModel.id == session_id)
        )
        model = result.scalar_one_or_none()
        return self._session_to_entity(model) if model else None

    async def create_session(self, session: ChatSession) -> ChatSession:
        model = ChatSessionModel(
            id=session.id,
            user_id=session.user_id,
            knowledge_base_id=session.knowledge_base_id,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._session_to_entity(model)

    async def add_message(self, message: Message) -> Message:
        model = MessageModel(
            id=message.id,
            session_id=message.session_id,
            role=message.role,
            content=message.content,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._message_to_entity(model)

    async def get_messages(self, session_id: str) -> List[Message]:
        result = await self.db.execute(
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.created_at.asc())
        )
        return [self._message_to_entity(m) for m in result.scalars().all()]

    def _session_to_entity(self, model: ChatSessionModel) -> ChatSession:
        return ChatSession(
            id=model.id,
            user_id=model.user_id,
            knowledge_base_id=model.knowledge_base_id,
            created_at=model.created_at,
        )

    def _message_to_entity(self, model: MessageModel) -> Message:
        return Message(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            content=model.content,
            created_at=model.created_at,
        )
