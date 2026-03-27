from abc import ABC, abstractmethod
from typing import List, Optional
from app.Domain.Chat.Entities.chat_session import ChatSession
from app.Domain.Chat.Entities.message import Message


class ChatRepositoryInterface(ABC):
    @abstractmethod
    async def find_session_by_id(self, session_id: str) -> Optional[ChatSession]: ...

    @abstractmethod
    async def create_session(self, session: ChatSession) -> ChatSession: ...

    @abstractmethod
    async def add_message(self, message: Message) -> Message: ...

    @abstractmethod
    async def get_messages(self, session_id: str) -> List[Message]: ...
