from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from openai import APIError as OpenAIAPIError
from app.Infrastructure.Database.connection import get_db
from app.Infrastructure.Repositories.sqlalchemy_knowledge_repository import SQLAlchemyKnowledgeRepository
from app.Infrastructure.Repositories.sqlalchemy_chat_repository import SQLAlchemyChatRepository
from app.Infrastructure.AI.ollama_ai_service import OllamaAIService
from app.Domain.Knowledge.Services.knowledge_service import KnowledgeService
from app.Domain.Chat.Services.chat_service import ChatService
from app.Domain.User.Entities.user import User
from app.Http.Middleware.auth_middleware import get_current_user
from app.Http.Requests.chat_requests import AskRequest
from config.settings import settings

router = APIRouter()


def _get_ai_service():
    """Resolve o serviço de IA pelo AI_PROVIDER configurado no .env."""
    provider = settings.AI_PROVIDER

    if provider == "ollama":
        return OllamaAIService(model=settings.AI_MODEL)

    # Providers remotos (xai, groq, openai) via OpenAI-compatible SDK
    from app.Infrastructure.AI.xai_ai_service import XAIService
    return XAIService()


@router.post("/ask")
async def ask(
    body: AskRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    knowledge_repo = SQLAlchemyKnowledgeRepository(db)
    chat_repo = SQLAlchemyChatRepository(db)
    knowledge_service = KnowledgeService(knowledge_repo)
    ai_service = _get_ai_service()
    chat_service = ChatService(ai_service, knowledge_service, chat_repo)

    try:
        result = await chat_service.ask(
            user_id=current_user.id,
            question=body.question,
            session_id=body.session_id,
        )
    except OpenAIAPIError as e:
        msg = str(e)
        if "insufficient" in msg.lower() or "credit" in msg.lower() or "quota" in msg.lower() or "permission" in msg.lower():
            raise HTTPException(status_code=402, detail="Créditos insuficientes na API de IA. Configure outro provider no .env")
        raise HTTPException(status_code=503, detail=f"Erro na API de IA: {msg[:200]}")
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return result


@router.get("/history/{session_id}")
async def history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    chat_repo = SQLAlchemyChatRepository(db)
    chat_service_obj = ChatService(None, None, chat_repo)  # type: ignore
    messages = await chat_service_obj.get_history(session_id)
    return {
        "session_id": session_id,
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ],
    }
