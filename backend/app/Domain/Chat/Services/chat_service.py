import uuid
from typing import List, Optional
from app.Domain.Chat.Entities.chat_session import ChatSession
from app.Domain.Chat.Entities.message import Message
from app.Domain.Chat.Repositories.chat_repository import ChatRepositoryInterface
from app.Domain.Chat.Services.ai_service import AIServiceInterface
from app.Domain.Knowledge.Services.knowledge_service import KnowledgeService


class ChatService:
    def __init__(
        self,
        ai_service: AIServiceInterface,
        knowledge_service: KnowledgeService,
        chat_repo: ChatRepositoryInterface,
    ):
        self.ai = ai_service
        self.knowledge = knowledge_service
        self.chat_repo = chat_repo

    async def ask(
        self,
        user_id: str,
        question: str,
        session_id: Optional[str] = None,
    ) -> dict:
        kb = await self.knowledge.get_active(user_id)

        session = None
        if session_id:
            session = await self.chat_repo.find_session_by_id(session_id)

        if not session:
            session = await self.chat_repo.create_session(
                ChatSession(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    knowledge_base_id=kb.id,
                )
            )

        await self.chat_repo.add_message(
            Message(
                id=str(uuid.uuid4()),
                session_id=session.id,
                role="user",
                content=question,
            )
        )

        answer = await self.ai.ask(question, kb.text)

        await self.chat_repo.add_message(
            Message(
                id=str(uuid.uuid4()),
                session_id=session.id,
                role="assistant",
                content=answer,
            )
        )

        sources_found = "Não sei com base nas informações fornecidas" not in answer

        return {
            "answer": answer,
            "session_id": session.id,
            "sources_found": sources_found,
        }

    async def get_history(self, session_id: str) -> List[Message]:
        return await self.chat_repo.get_messages(session_id)
