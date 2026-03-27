import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from app.Models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    knowledge_bases = relationship(
        "KnowledgeBaseModel", back_populates="user", cascade="all, delete-orphan"
    )
    chat_sessions = relationship(
        "ChatSessionModel", back_populates="user", cascade="all, delete-orphan"
    )
