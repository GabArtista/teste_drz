from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.Infrastructure.Database.connection import get_db
from app.Infrastructure.Repositories.sqlalchemy_knowledge_repository import SQLAlchemyKnowledgeRepository
from app.Domain.Knowledge.Services.knowledge_service import KnowledgeService
from app.Domain.User.Entities.user import User
from app.Http.Middleware.auth_middleware import get_current_user
from app.Http.Requests.knowledge_requests import UploadTextRequest

router = APIRouter()


def _kb_response(kb) -> dict:
    return {
        "id": kb.id,
        "preview": kb.text[:120] + "..." if len(kb.text) > 120 else kb.text,
        "char_count": kb.char_count,
        "has_text": True,
    }


@router.post("/upload-text")
async def upload_text(
    body: UploadTextRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SQLAlchemyKnowledgeRepository(db)
    service = KnowledgeService(repo)
    kb = await service.upload(current_user.id, body.text)
    return _kb_response(kb)


@router.get("/current")
async def get_current(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SQLAlchemyKnowledgeRepository(db)
    service = KnowledgeService(repo)
    kb = await service.get_active_optional(current_user.id)
    if not kb:
        return {"id": None, "preview": None, "char_count": 0, "has_text": False}
    return _kb_response(kb)
