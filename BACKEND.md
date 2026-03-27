# Backend – Especificação Técnica

## Stack
- Python 3.11+
- FastAPI 0.111+
- SQLAlchemy 2.0 (async)
- Pydantic v2
- python-jose (JWT)
- bcrypt / passlib
- aiosqlite (dev) / asyncpg (prod)
- Alembic (migrations)
- Anthropic SDK
- httpx (async HTTP)

## Estrutura de Pastas

```
backend/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── auth_controller.py
│   │   │   ├── knowledge_controller.py
│   │   │   └── chat_controller.py
│   │   ├── Middleware/
│   │   │   └── auth_middleware.py
│   │   └── Requests/
│   │       ├── auth_requests.py
│   │       ├── knowledge_requests.py
│   │       └── chat_requests.py
│   ├── Domain/
│   │   ├── User/
│   │   │   ├── Entities/
│   │   │   │   └── user.py
│   │   │   ├── Repositories/
│   │   │   │   └── user_repository.py      ← Abstract
│   │   │   └── Services/
│   │   │       └── auth_service.py
│   │   ├── Knowledge/
│   │   │   ├── Entities/
│   │   │   │   └── knowledge_base.py
│   │   │   ├── Repositories/
│   │   │   │   └── knowledge_repository.py ← Abstract
│   │   │   └── Services/
│   │   │       └── knowledge_service.py
│   │   └── Chat/
│   │       ├── Entities/
│   │       │   ├── chat_session.py
│   │       │   └── message.py
│   │       ├── Repositories/
│   │       │   └── chat_repository.py      ← Abstract
│   │       └── Services/
│   │           ├── chat_service.py
│   │           └── ai_service.py           ← Interface para IA
│   ├── Models/
│   │   ├── user_model.py
│   │   ├── knowledge_base_model.py
│   │   ├── chat_session_model.py
│   │   └── message_model.py
│   ├── Infrastructure/
│   │   ├── Repositories/
│   │   │   ├── sqlalchemy_user_repository.py
│   │   │   ├── sqlalchemy_knowledge_repository.py
│   │   │   └── sqlalchemy_chat_repository.py
│   │   ├── AI/
│   │   │   └── anthropic_ai_service.py
│   │   └── Database/
│   │       ├── connection.py
│   │       └── session.py
│   ├── Providers/
│   │   └── app_provider.py                 ← DI wiring (FastAPI Depends)
│   └── Exceptions/
│       ├── domain_exceptions.py
│       └── handlers.py
├── config/
│   └── settings.py                         ← Pydantic BaseSettings
├── database/
│   └── migrations/                         ← Alembic
├── resources/
│   └── prompts/
│       └── knowledge_qa.txt                ← System prompt template
├── tests/
│   ├── unit/
│   └── integration/
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── main.py
```

## API Contract

### Auth

#### POST /auth/register
```json
Request:
{
  "name": "string",
  "email": "user@example.com",
  "password": "string (min 8)"
}

Response 201:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { "id": "uuid", "name": "string", "email": "string" }
}

Errors:
- 409: Email já cadastrado
- 422: Validação falhou
```

#### POST /auth/login
```json
Request:
{
  "email": "user@example.com",
  "password": "string"
}

Response 200:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { "id": "uuid", "name": "string", "email": "string" }
}

Errors:
- 401: Credenciais inválidas
```

#### GET /auth/me
```
Headers: Authorization: Bearer <token>

Response 200:
{ "id": "uuid", "name": "string", "email": "string" }
```

### Knowledge Base

#### POST /knowledge/upload-text
```json
Headers: Authorization: Bearer <token>

Request:
{
  "text": "string (texto base completo)"
}

Response 200:
{
  "id": "uuid",
  "preview": "primeiros 100 chars...",
  "char_count": 1234,
  "created_at": "ISO datetime"
}
```

#### GET /knowledge/current
```
Headers: Authorization: Bearer <token>

Response 200:
{
  "id": "uuid",
  "preview": "...",
  "char_count": 1234,
  "has_text": true
}
```

### Chat

#### POST /chat/ask
```json
Headers: Authorization: Bearer <token>

Request:
{
  "question": "string",
  "session_id": "uuid (opcional)"
}

Response 200:
{
  "answer": "string",
  "session_id": "uuid",
  "sources_found": true
}
```

#### GET /chat/history/{session_id}
```
Headers: Authorization: Bearer <token>

Response 200:
{
  "session_id": "uuid",
  "messages": [
    { "role": "user|assistant", "content": "string", "created_at": "ISO" }
  ]
}
```

## Domain Entities

### User
```python
@dataclass
class User:
    id: UUID
    name: str
    email: str
    password_hash: str
    created_at: datetime
```

### KnowledgeBase
```python
@dataclass
class KnowledgeBase:
    id: UUID
    user_id: UUID
    text: str
    char_count: int
    created_at: datetime
    is_active: bool
```

### ChatSession
```python
@dataclass
class ChatSession:
    id: UUID
    user_id: UUID
    knowledge_base_id: UUID
    created_at: datetime
```

### Message
```python
@dataclass
class Message:
    id: UUID
    session_id: UUID
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime
```

## Prompt Engineering (resources/prompts/knowledge_qa.txt)

```
Você é um assistente especializado que responde perguntas exclusivamente
com base no texto fornecido abaixo.

REGRAS ABSOLUTAS:
1. Responda SOMENTE com informações presentes no texto abaixo
2. Se a informação não estiver no texto, responda EXATAMENTE:
   "Não sei com base nas informações fornecidas."
3. Não use conhecimento externo ou inferências
4. Seja preciso e direto

TEXTO BASE:
---
{knowledge_text}
---

PERGUNTA DO USUÁRIO: {question}

RESPOSTA:
```

## AI Service Interface

```python
# app/Domain/Chat/Services/ai_service.py
from abc import ABC, abstractmethod

class AIServiceInterface(ABC):
    @abstractmethod
    async def ask(
        self,
        question: str,
        knowledge_text: str
    ) -> str: ...
```

```python
# app/Infrastructure/AI/anthropic_ai_service.py
class AnthropicAIService(AIServiceInterface):
    async def ask(self, question: str, knowledge_text: str) -> str:
        prompt = self._build_prompt(knowledge_text, question)
        response = await self.client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
```

## Dependency Injection (Providers)

```python
# app/Providers/app_provider.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.Infrastructure.Database.session import get_db
from app.Infrastructure.Repositories import *
from app.Infrastructure.AI.anthropic_ai_service import AnthropicAIService

def get_user_repository(db: AsyncSession = Depends(get_db)):
    return SQLAlchemyUserRepository(db)

def get_auth_service(
    repo = Depends(get_user_repository)
):
    return AuthService(repo)

def get_ai_service() -> AIServiceInterface:
    return AnthropicAIService()

def get_chat_service(
    ai = Depends(get_ai_service),
    knowledge_repo = Depends(get_knowledge_repository),
    chat_repo = Depends(get_chat_repository)
):
    return ChatService(ai, knowledge_repo, chat_repo)
```

## Auth Middleware (JWT)

```python
# app/Http/Middleware/auth_middleware.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo = Depends(get_user_repository)
) -> User:
    payload = decode_jwt(token)  # raises 401 on invalid
    user = await user_repo.find_by_id(payload["sub"])
    if not user:
        raise HTTPException(401)
    return user
```

## Models SQLAlchemy

```python
# app/Models/user_model.py
class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    knowledge_bases = relationship("KnowledgeBaseModel", back_populates="user")
    chat_sessions = relationship("ChatSessionModel", back_populates="user")
```

## Configuração (config/settings.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    ANTHROPIC_API_KEY: str
    AI_MODEL: str = "claude-haiku-4-5-20251001"
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"

settings = Settings()
```

## main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Http.Controllers import auth_controller, knowledge_controller, chat_controller
from app.Exceptions.handlers import register_exception_handlers
from config.settings import settings

app = FastAPI(title="DRZ Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])
app.include_router(knowledge_controller.router, prefix="/knowledge", tags=["Knowledge"])
app.include_router(chat_controller.router, prefix="/chat", tags=["Chat"])

register_exception_handlers(app)
```

## Testes

### Unit (tests/unit/)
- `test_auth_service.py` — register, login, hash validation
- `test_knowledge_service.py` — upload, retrieve active
- `test_chat_service.py` — prompt building, fallback message

### Integration (tests/integration/)
- `test_auth_flow.py` — register → login → me
- `test_knowledge_flow.py` — upload → current
- `test_chat_flow.py` — upload → ask → history

## Como rodar

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # preencher ANTHROPIC_API_KEY e SECRET_KEY
alembic upgrade head
uvicorn main:app --reload --port 8000
```
