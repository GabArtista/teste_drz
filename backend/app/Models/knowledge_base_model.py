import uuid
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.Models.base import Base


class KnowledgeBaseModel(Base):
    __tablename__ = "knowledge_bases"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    char_count = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", back_populates="knowledge_bases")
    chat_sessions = relationship("ChatSessionModel", back_populates="knowledge_base")
