import uuid
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.Domain.User.Entities.user import User
from app.Domain.User.Repositories.user_repository import UserRepositoryInterface
from app.Exceptions.domain_exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from config.settings import settings


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


def _verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False


class AuthService:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def register(self, name: str, email: str, password: str) -> tuple[User, str]:
        existing = await self.user_repo.find_by_email(email)
        if existing:
            raise EmailAlreadyExistsException(email)

        user = User(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            password_hash=_hash_password(password),
        )
        user = await self.user_repo.create(user)
        token = self._create_token(user.id)
        return user, token

    async def login(self, email: str, password: str) -> tuple[User, str]:
        user = await self.user_repo.find_by_email(email)
        if not user or not _verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        token = self._create_token(user.id)
        return user, token

    def _create_token(self, user_id: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRE_HOURS)
        payload = {"sub": user_id, "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get("sub")
            if not user_id:
                raise InvalidCredentialsException()
            return user_id
        except JWTError:
            raise InvalidCredentialsException()
