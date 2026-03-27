# DRZ — Assistente de IA com Texto Base

Aplicação Full Stack com **FastAPI** (Python) + **React + Vite** (TypeScript) que permite ao usuário enviar um texto base e conversar com uma IA que responde **exclusivamente** com base nesse texto.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução Rápida](#instalação-e-execução-rápida)
- [Guia Passo a Passo — Do Zero](#guia-passo-a-passo--do-zero)
  - [1. Python 3.12](#1-python-312)
  - [2. Node.js 20](#2-nodejs-20)
  - [3. Ollama (IA local, gratuita)](#3-ollama-ia-local-gratuita)
  - [4. Backend](#4-backend)
  - [5. Frontend](#5-frontend)
- [Provedores de IA](#provedores-de-ia)
  - [Ollama (padrão — gratuito, sem internet)](#ollama-padrão--gratuito-sem-internet)
  - [xAI / Groq / OpenAI (nuvem)](#xai--groq--openai-nuvem)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Rodando os Testes](#rodando-os-testes)
- [Arquitetura](#arquitetura)
- [Fluxos da Aplicação](#fluxos-da-aplicação)

---

## Visão Geral

| Camada | Tecnologia | Porta |
|--------|-----------|-------|
| Backend API | FastAPI 0.111, Python 3.12 | `8000` |
| Frontend | React 18 + Vite 5, TypeScript | `5173` |
| IA local | Ollama (qwen2.5:1.5b) | `11434` |
| Banco de dados | SQLite (aiosqlite) | — |

**Funcionalidades:**
- Registro e login com JWT (24h de validade)
- Upload de texto base (qualquer conteúdo)
- Chat com IA que responde **somente** com base no texto enviado
- Recusa educada para perguntas fora do contexto
- Histórico de mensagens na sessão

---

## Pré-requisitos

| Ferramenta | Versão mínima | Verificar |
|-----------|--------------|-----------|
| Python | 3.10+ (recomendado 3.12) | `python3 --version` |
| pip | qualquer | `pip3 --version` |
| Node.js | 18+ (recomendado 20) | `node --version` |
| npm | 9+ | `npm --version` |
| Ollama | qualquer | `ollama --version` |
| Git | qualquer | `git --version` |

> **Sem Ollama?** Você pode usar xAI, Groq ou OpenAI. Veja [Provedores de IA](#provedores-de-ia).

---

## Instalação e Execução Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/gabrielseibel1/DRZ.git
cd DRZ

# 2. Configure o backend
cd backend
cp .env.example .env          # ajuste se quiser outro provedor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..

# 3. Configure o frontend
cd frontend
npm install
cd ..

# 4. Inicie tudo com um script
chmod +x start.sh
./start.sh
```

Abra **http://localhost:5173** no navegador.

---

## Guia Passo a Passo — Do Zero

### 1. Python 3.12

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version  # deve exibir 3.10+
```

**macOS (com Homebrew):**
```bash
brew install python@3.12
python3 --version
```

**Windows:**
Baixe em https://python.org/downloads — marque "Add Python to PATH" durante a instalação.

---

### 2. Node.js 20

**Ubuntu / Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node --version   # deve exibir v20+
npm --version
```

**macOS:**
```bash
brew install node@20
```

**Windows:**
Baixe em https://nodejs.org (LTS).

---

### 3. Ollama (IA local, gratuita)

**Linux / macOS:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &          # inicia o servidor em background
ollama pull qwen2.5:1.5b  # baixa o modelo (~986 MB, apenas 1x)
```

**Windows:**
Baixe o instalador em https://ollama.com/download

Verifique:
```bash
curl http://localhost:11434/api/tags
# deve listar o modelo qwen2.5:1.5b
```

> O primeiro uso pode demorar ~30–90 segundos para carregar o modelo na memória ("cold start"). Nas chamadas seguintes é muito mais rápido.

---

### 4. Backend

```bash
cd backend

# Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows (PowerShell)

# Instale dependências
pip install -r requirements.txt

# Configure o ambiente
cp .env.example .env
# O padrão já está configurado para Ollama local — sem precisar alterar

# Inicie o servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará disponível em **http://localhost:8000**
Documentação interativa: **http://localhost:8000/docs**

---

### 5. Frontend

Em outro terminal:

```bash
cd frontend

# Instale dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

Acesse **http://localhost:5173**

---

## Provedores de IA

### Ollama (padrão — gratuito, sem internet)

Não requer conta nem API key. Roda 100% local na sua máquina.

```ini
# backend/.env
AI_PROVIDER=ollama
AI_MODEL=qwen2.5:1.5b
```

**Limitação:** Inferência via CPU pode levar 20–90s por resposta dependendo do hardware.
**Para acelerar:** Se tiver GPU NVIDIA, o Ollama a usa automaticamente.

Outros modelos Ollama que funcionam bem:
```bash
ollama pull llama3.2:3b       # mais capaz, ~2GB
ollama pull phi3.5            # bom custo/benefício
```
Ajuste `AI_MODEL` no `.env` conforme o modelo baixado.

---

### xAI / Groq / OpenAI (nuvem)

Respostas mais rápidas e precisas. Requer conta e API key do provedor.

```ini
# backend/.env — exemplo com Groq (tem plano gratuito)
AI_PROVIDER=groq
GROQ_API_KEY=gsk_...

# exemplo com xAI
AI_PROVIDER=xai
XAI_API_KEY=xai-...

# exemplo com OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

| Provedor | Site | Plano gratuito |
|---------|------|---------------|
| Groq | https://console.groq.com | Sim (rate limits) |
| xAI | https://console.x.ai | Créditos iniciais |
| OpenAI | https://platform.openai.com | Não (pay-as-you-go) |

Com Groq a resposta é praticamente instantânea e o plano gratuito é generoso para desenvolvimento.

---

## Variáveis de Ambiente

### `backend/.env`

```ini
# Banco de dados
DATABASE_URL=sqlite+aiosqlite:///./app.db

# JWT
JWT_SECRET_KEY=troque-esta-chave-por-algo-seguro
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# CORS
CORS_ORIGINS=["http://localhost:5173"]

# IA — escolha um provedor:
AI_PROVIDER=ollama          # ollama | xai | groq | openai
AI_MODEL=qwen2.5:1.5b      # modelo a usar (vazio = padrão do provedor)

# Chaves de API (preencha apenas o provedor escolhido)
XAI_API_KEY=
GROQ_API_KEY=
OPENAI_API_KEY=
```

> **Nunca commite o arquivo `.env` com chaves reais.** O `.gitignore` já o exclui.

---

## Rodando os Testes

### Backend (pytest)

```bash
cd backend
source .venv/bin/activate
pytest -v
```

Saída esperada: **33 testes passando** (16 unit + 17 integração).

### Frontend (Vitest — testes unitários)

```bash
cd frontend
npm run test
```

Saída esperada: **3 testes passando**.

### E2E (Playwright)

Requer backend + frontend + Ollama rodando:

```bash
# Terminal 1 — backend
cd backend && source .venv/bin/activate && uvicorn main:app --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev

# Terminal 3 — testes E2E
cd frontend
npx playwright install chromium   # apenas na primeira vez
npm run test:e2e
```

Saída esperada: **17 testes E2E passando** (6 auth/upload + 11 chat).

> Os testes de IA têm timeout de 120s e 1 retry por causa da inferência local. Com Groq/xAI eles concluem em segundos.

### Todos os testes de uma vez

```bash
# Do diretório raiz
cd backend && source .venv/bin/activate && pytest -v && cd ../frontend && npm run test && npm run test:e2e
```

---

## Arquitetura

```
DRZ/
├── backend/                    # FastAPI — Clean Architecture + DDD
│   ├── main.py                 # Entry point, lifespan, CORS, rotas
│   ├── config/settings.py      # Pydantic BaseSettings
│   ├── app/
│   │   ├── Domain/             # Camada de domínio (zero dependências externas)
│   │   │   ├── User/           # Entidade, repositório (interface), serviço de auth
│   │   │   ├── KnowledgeBase/  # Entidade, repositório, serviço
│   │   │   └── Chat/           # Entidade Message/Session, serviço de chat
│   │   ├── Http/
│   │   │   ├── Controllers/    # auth, knowledge, chat
│   │   │   ├── Middleware/     # JWT auth middleware
│   │   │   └── Requests/       # Schemas Pydantic (DTOs)
│   │   ├── Models/             # SQLAlchemy ORM models
│   │   └── Infrastructure/
│   │       ├── Repositories/   # Implementações SQLAlchemy dos repositórios
│   │       └── AI/             # OllamaAIService, XAIService
│   ├── resources/prompts/      # Template de prompt (provedores de nuvem)
│   ├── tests/
│   │   ├── unit/               # Testes unitários (sem I/O)
│   │   └── integration/        # Testes de integração (SQLite in-memory)
│   └── requirements.txt
│
├── frontend/                   # React + Vite + TypeScript
│   ├── src/
│   │   ├── pages/              # Login, Register, Upload, Chat
│   │   ├── stores/             # Zustand (auth, chat, knowledge)
│   │   ├── lib/api.ts          # Axios + interceptor JWT
│   │   └── components/         # Componentes reutilizáveis
│   ├── tests/e2e/              # Playwright — testes de ponta a ponta
│   └── src/test/               # Vitest — testes unitários
│
└── start.sh                    # Script para subir todos os serviços
```

**Princípios aplicados:**
- **Clean Architecture**: Domain layer sem dependências de framework
- **DDD**: Aggregates (`User`, `KnowledgeBase`, `ChatSession`, `Message`) com repositórios abstratos
- **Dependency Inversion**: Controllers dependem de interfaces, não de implementações concretas
- **Strategy Pattern**: Troca de provedor de IA via variável de ambiente sem alterar código

---

## Fluxos da Aplicação

### Registro e Login
1. Usuário preenche nome, e-mail e senha
2. Backend cria o usuário com senha hasheada (bcrypt, 12 rounds)
3. JWT (24h) retornado e armazenado no `localStorage`
4. Axios intercepta todas as requisições e adiciona o token

### Upload de Texto
1. Usuário cola ou digita o texto base
2. Backend armazena na tabela `knowledge_bases` vinculada ao usuário
3. Redirecionamento automático para o chat

### Chat com IA
1. Usuário envia pergunta
2. Backend recupera o texto base do usuário autenticado
3. Constrói prompt com o texto + pergunta e envia ao provedor de IA
4. IA responde **somente** com base no texto (ou diz "Não sei...")
5. Histórico exibido na tela em tempo real

---

## Estrutura de Testes — Resumo

| Suite | Qtd | O que cobre |
|-------|-----|-------------|
| Backend unit | 16 | AuthService (hash/verify), ChatService (lógica pura) |
| Backend integração | 17 | Endpoints HTTP completos com DB SQLite in-memory |
| Frontend unit | 3 | Componentes React isolados |
| E2E auth/upload | 6 | Register, login, upload, fluxo completo |
| E2E chat | 11 | Empty state, redirect, input, respostas IA, histórico |
| **Total** | **53** | **Cobertura de ponta a ponta** |

---

## Problemas Comuns

**`ollama: command not found`**
Instale o Ollama: `curl -fsSL https://ollama.com/install.sh | sh`

**`Connection refused` no backend**
Verifique se o Ollama está rodando: `ollama serve`

**Testes E2E lentos / timeout**
Normal na primeira execução (cold start do modelo). O `beforeAll` aquece o modelo antes dos testes. Com Groq/xAI não há esse problema.

**`ModuleNotFoundError` no backend**
Certifique-se de estar com o ambiente virtual ativado: `source .venv/bin/activate`

**Porta já em uso**
```bash
lsof -i :8000   # backend
lsof -i :5173   # frontend
kill -9 <PID>
```
