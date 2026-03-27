# Gaps & Decisões Pendentes

## Decisões que precisam de confirmação antes de desenvolver

### 1. Chave da API de IA
- Você tem uma `ANTHROPIC_API_KEY` disponível?
- Se não: usar OpenAI? Groq? Ou mockar a IA para o teste?
- **Impacto**: muda `Infrastructure/AI/` e `.env`

### 2. Banco de Dados
- SQLite está ok para o teste (zero config, funciona de imediato)?
- **Decisão recomendada**: ✅ SQLite para simplicidade no teste
- Alembic configurado para migrar facilmente para PostgreSQL em produção

### 3. Streaming da resposta da IA
- A resposta da IA chega como texto completo ou em streaming (token a token)?
- Streaming melhora UX mas adiciona complexidade (Server-Sent Events)
- **Decisão recomendada**: Resposta completa primeiro, streaming como melhoria opcional

### 4. Sessões de Chat
- Uma única sessão por usuário ou múltiplas sessões?
- **Decisão recomendada**: Uma sessão ativa por knowledge_base, nova sessão quando trocar texto

### 5. Knowledge Base por usuário
- Um texto ativo por vez (substituível) ou histórico de uploads?
- **Decisão recomendada**: Um texto ativo, novo upload substitui o anterior

### 6. Shadcn/ui vs CSS manual
- Usar shadcn/ui (instala componentes prontos) ou escrever CSS com Tailwind puro?
- **Decisão recomendada**: Tailwind puro para evitar setup extra no teste

## Gaps Técnicos Identificados

### Backend
- [ ] Confirmar versão da Anthropic SDK (anthropic >= 0.25.0)
- [ ] Strategy de migration: auto-upgrade no startup ou manual?
- [ ] CORS: apenas localhost:5173 ou outros origins?

### Frontend
- [ ] React Router: versão 6 (stable) ou 7?
- [ ] Zustand: versão 4 ou 5?
- [ ] Confirmar se shadcn/ui ou Tailwind puro

## O que NÃO está no escopo do teste

- Refresh token / token rotation
- Rate limiting
- Email verification
- File upload (só texto puro)
- Multi-tenancy
- Docker / deploy
- Testes E2E (Playwright)

## Ordem de desenvolvimento sugerida

```
1. Backend: setup inicial (FastAPI + SQLAlchemy + Alembic)
2. Backend: auth (register/login/me)
3. Backend: knowledge upload
4. Backend: chat/ask com IA
5. Backend: testes unitários básicos
6. Frontend: setup (Vite + Router + Zustand + Axios)
7. Frontend: auth pages (Login + Register)
8. Frontend: Upload page
9. Frontend: Chat page
10. Integração e smoke test ponta-a-ponta
```

## Estimativa de Arquivos

| Lado     | Arquivos | Aproximado |
|----------|----------|------------|
| Backend  | ~35      | ~1.200 linhas |
| Frontend | ~25      | ~900 linhas   |
| Total    | ~60      | ~2.100 linhas |
