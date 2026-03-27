from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.Infrastructure.Database.connection import get_db
from app.Infrastructure.Repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.Domain.User.Services.auth_service import AuthService
from app.Domain.User.Entities.user import User
from app.Http.Requests.auth_requests import RegisterRequest, LoginRequest
from app.Http.Middleware.auth_middleware import get_current_user

router = APIRouter()


def _user_response(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/register", status_code=201)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    service = AuthService(repo)
    user, token = await service.register(body.name, body.email, body.password)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": _user_response(user),
    }


@router.post("/login")
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    service = AuthService(repo)
    user, token = await service.login(body.email, body.password)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": _user_response(user),
    }


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return _user_response(current_user)
