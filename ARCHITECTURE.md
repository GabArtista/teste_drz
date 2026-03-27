# Arquitetura Geral – Teste DRZ

## Visão Geral

Dois microsserviços independentes com comunicação via HTTP REST:

```
┌─────────────────────┐         ┌──────────────────────────┐
│   frontend (React)  │ ──HTTP──▶│  backend (FastAPI/Python) │
│   :5173 (dev)       │◀──────── │  :8000                    │
└─────────────────────┘          └──────────┬───────────────┘
                                             │
                                   ┌─────────▼──────────┐
                                   │  Anthropic/OpenAI  │
                                   └────────────────────┘
```

## Stack

| Camada     | Tecnologia                              |
|------------|----------------------------------------|
| Backend    | Python 3.11+, FastAPI, Pydantic v2      |
| Auth       | JWT (python-jose), bcrypt               |
| IA         | Anthropic Claude (claude-haiku-4-5)     |
| DB         | SQLite (dev) → PostgreSQL (prod)        |
| ORM        | SQLAlchemy 2.0 async + Alembic          |
| Frontend   | React 18, Vite, TypeScript              |
| UI         | TailwindCSS + shadcn/ui                 |
| State      | Zustand                                 |
| HTTP       | Axios                                   |
| Roteamento | React Router v6                         |

## Princípios Arquiteturais

### Clean Architecture
- Regras de negócio no Domain (sem dependência de frameworks)
- Dependências apontam para dentro (domain → nunca importa infra)
- Interfaces (portas) definidas no domain, implementadas na infra

### DDD Aplicado
- Agregados: `User`, `KnowledgeBase`, `ChatSession`
- Repositórios abstratos no domain, concretos na infra
- Services de domínio para regras que envolvem múltiplas entidades

### Estrutura Laravel-like (adaptada para Python/React)
```
backend/
├── app/
│   ├── Http/            ← Controllers, Middleware, Requests (validators)
│   ├── Domain/          ← Entities, Repositories (abstract), Services
│   ├── Models/          ← SQLAlchemy ORM models
│   ├── Providers/       ← Dependency injection wiring
│   └── Exceptions/      ← Custom exceptions + handlers
├── config/              ← Settings por ambiente
├── database/
│   └── migrations/      ← Alembic migrations
├── resources/           ← Templates, prompts, assets estáticos
├── tests/               ← Unit + Integration
└── main.py              ← Entrypoint FastAPI

frontend/
├── src/
│   ├── components/
│   │   ├── ui/          ← Atoms: Button, Input, Card, Modal
│   │   ├── features/    ← Molecules: ChatBox, AuthForm, UploadPanel
│   │   └── layouts/     ← AppShell, AuthLayout
│   ├── pages/           ← Login, Register, Upload, Chat
│   ├── services/        ← API clients (authService, chatService)
│   ├── stores/          ← Zustand stores (authStore, chatStore)
│   ├── types/           ← TypeScript interfaces
│   └── lib/             ← Utils, axios instance, helpers
├── public/
└── index.html
```

## Fluxos Principais

### 1. Autenticação
```
Register → POST /auth/register → JWT token
Login    → POST /auth/login    → JWT token
Token armazenado no localStorage + Zustand store
Axios interceptor injeta Bearer token em todas requisições
Rotas protegidas via PrivateRoute component
```

### 2. Upload de Texto
```
Usuário cola texto → POST /knowledge/upload-text
Backend armazena no DB associado ao user_id
Retorna knowledge_base_id
Frontend armazena ID no chatStore
```

### 3. Chat com IA
```
Usuário digita pergunta → POST /chat/ask
Backend:
  1. Recupera knowledge_base do user
  2. Monta prompt: system + texto_base + pergunta
  3. Chama Claude API
  4. Se não encontrado no texto → "Não sei com base nas informações fornecidas."
  5. Persiste mensagem no histórico
  6. Retorna resposta
Frontend: exibe resposta em streaming ou após load
```

## Regras de Negócio (Domain Rules)

1. Cada usuário tem uma `KnowledgeBase` ativa por vez
2. O sistema **só responde com base no texto fornecido** — prompt engineering rígido
3. Se não houver resposta no contexto, retorna mensagem padrão
4. Histórico de chat é persistido por sessão
5. Autenticação obrigatória para todos os endpoints exceto `/auth/*`

## Segurança

- Senhas hasheadas com bcrypt (cost factor 12)
- JWT com expiração de 24h
- CORS configurado para permitir apenas o frontend
- Validação de entrada via Pydantic em todas as rotas
- SQL Injection impossível via ORM

## Variáveis de Ambiente

### Backend (.env)
```
DATABASE_URL=sqlite+aiosqlite:///./app.db
SECRET_KEY=<random-256-bit>
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
ANTHROPIC_API_KEY=<key>
AI_MODEL=claude-haiku-4-5-20251001
CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000
```
