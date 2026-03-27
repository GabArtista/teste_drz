import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.Models.base import Base


class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    knowledge_base_id = Column(String(36), ForeignKey("knowledge_bases.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", back_populates="chat_sessions")
    knowledge_base = relationship("KnowledgeBaseModel", back_populates="chat_sessions")
    messages = relationship(
        "MessageModel", back_populates="session", cascade="all, delete-orphan"
    )
