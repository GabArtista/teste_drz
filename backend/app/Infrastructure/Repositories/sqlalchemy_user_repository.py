from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.Domain.User.Entities.user import User
from app.Domain.User.Repositories.user_repository import UserRepositoryInterface
from app.Models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_id(self, user_id: str) -> Optional[User]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def create(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password_hash,
            created_at=model.created_at,
        )
