from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    SECRET_KEY: str = "dev-secret-mude-em-producao"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    ANTHROPIC_API_KEY: str = ""
    XAI_API_KEY: str = ""
    AI_MODEL: str = "grok-3-mini-fast"
    AI_PROVIDER: str = "xai"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()
