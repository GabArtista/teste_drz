from abc import ABC, abstractmethod
from typing import Optional
from app.Domain.User.Entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...
