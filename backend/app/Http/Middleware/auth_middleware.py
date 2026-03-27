from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.Infrastructure.Database.connection import get_db
from app.Infrastructure.Repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.Domain.User.Services.auth_service import AuthService
from app.Domain.User.Entities.user import User
from app.Exceptions.domain_exceptions import InvalidCredentialsException

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(repo)

    try:
        user_id = auth_service.decode_token(token)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    user = await repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")

    return user
