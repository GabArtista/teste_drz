# Frontend – Especificação Técnica

## Stack
- React 18 + TypeScript
- Vite 5
- React Router v6
- Zustand (state management)
- Axios (HTTP)
- TailwindCSS
- shadcn/ui (componentes base)

## Estrutura de Pastas

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/                     ← Atoms (shadcn + customizados)
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Textarea.tsx
│   │   │   ├── Card.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── features/               ← Molecules (lógica de feature)
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── RegisterForm.tsx
│   │   │   ├── knowledge/
│   │   │   │   └── UploadPanel.tsx
│   │   │   └── chat/
│   │   │       ├── ChatBox.tsx
│   │   │       ├── MessageList.tsx
│   │   │       ├── MessageBubble.tsx
│   │   │       └── QuestionInput.tsx
│   │   └── layouts/
│   │       ├── AppShell.tsx        ← Layout autenticado (header + outlet)
│   │       └── AuthLayout.tsx      ← Layout público (centered card)
│   ├── pages/
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── UploadPage.tsx          ← Tela 1: enviar texto
│   │   └── ChatPage.tsx            ← Tela 2: perguntas e respostas
│   ├── services/
│   │   ├── api.ts                  ← Axios instance + interceptors
│   │   ├── authService.ts
│   │   ├── knowledgeService.ts
│   │   └── chatService.ts
│   ├── stores/
│   │   ├── authStore.ts            ← Zustand: user, token, isAuthenticated
│   │   └── chatStore.ts            ← Zustand: knowledgeId, messages, session
│   ├── types/
│   │   ├── auth.types.ts
│   │   ├── knowledge.types.ts
│   │   └── chat.types.ts
│   ├── lib/
│   │   └── utils.ts                ← cn(), formatDate(), etc.
│   ├── router/
│   │   ├── index.tsx               ← createBrowserRouter config
│   │   └── PrivateRoute.tsx        ← Guard de autenticação
│   └── main.tsx
├── public/
├── index.html
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── .env
└── package.json
```

## Rotas

```
/login          → LoginPage (público)
/register       → RegisterPage (público)
/upload         → UploadPage (privado) ← Tela 1 do teste
/chat           → ChatPage (privado)   ← Tela 2 do teste
/               → redirect para /upload (se autenticado) ou /login
```

## Stores (Zustand)

### authStore
```typescript
interface AuthStore {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
  hydrate: () => void   // carrega token do localStorage
}
```

### chatStore
```typescript
interface ChatStore {
  knowledgeId: string | null
  sessionId: string | null
  messages: Message[]
  isLoading: boolean
  hasKnowledge: boolean
  uploadText: (text: string) => Promise<void>
  ask: (question: string) => Promise<void>
  clearSession: () => void
}
```

## Services

### api.ts (Axios instance)
```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

// Request interceptor: injeta Bearer token
api.interceptors.request.use(config => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Response interceptor: 401 → logout + redirect
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)
```

### authService.ts
```typescript
export const authService = {
  register: (data: RegisterRequest) =>
    api.post<AuthResponse>('/auth/register', data),
  login: (data: LoginRequest) =>
    api.post<AuthResponse>('/auth/login', data),
  me: () =>
    api.get<User>('/auth/me'),
}
```

### knowledgeService.ts
```typescript
export const knowledgeService = {
  uploadText: (text: string) =>
    api.post<KnowledgeResponse>('/knowledge/upload-text', { text }),
  getCurrent: () =>
    api.get<KnowledgeResponse>('/knowledge/current'),
}
```

### chatService.ts
```typescript
export const chatService = {
  ask: (question: string, sessionId?: string) =>
    api.post<AskResponse>('/chat/ask', { question, session_id: sessionId }),
  getHistory: (sessionId: string) =>
    api.get<HistoryResponse>(`/chat/history/${sessionId}`),
}
```

## Tipos

```typescript
// types/auth.types.ts
interface User { id: string; name: string; email: string }
interface AuthResponse { access_token: string; token_type: string; user: User }
interface RegisterRequest { name: string; email: string; password: string }
interface LoginRequest { email: string; password: string }

// types/knowledge.types.ts
interface KnowledgeResponse {
  id: string; preview: string; char_count: number; has_text: boolean
}

// types/chat.types.ts
interface Message { role: 'user' | 'assistant'; content: string; created_at?: string }
interface AskResponse { answer: string; session_id: string; sources_found: boolean }
```

## Pages

### LoginPage.tsx
- Formulário: email + senha
- Botão "Entrar"
- Link "Não tem conta? Cadastre-se"
- Feedback de erro inline (sem toast)
- Ao sucesso: navigate('/upload')

### RegisterPage.tsx
- Formulário: nome + email + senha + confirmar senha
- Validação client-side (senhas coincidem, email válido)
- Botão "Criar conta"
- Link "Já tem conta? Entrar"
- Ao sucesso: navigate('/upload')

### UploadPage.tsx (Tela 1 do teste)
- Textarea grande para colar o texto-base
- Caracteres contados em tempo real
- Botão "Enviar texto para a IA"
- Status: "Texto carregado ✓" se já existe
- Após envio bem-sucedido: botão "Ir para perguntas"

### ChatPage.tsx (Tela 2 do teste)
- Header com nome do usuário + botão logout
- Área de mensagens (scroll automático para última)
- Bolhas diferenciadas: usuário (direita, azul) / IA (esquerda, cinza)
- Input + botão "Perguntar"
- Loading spinner enquanto IA responde
- Mensagem de erro se knowledge não foi carregado
- Botão "Alterar texto base" → volta para /upload

## PrivateRoute

```tsx
// router/PrivateRoute.tsx
export function PrivateRoute({ children }: { children: ReactNode }) {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  return isAuthenticated ? children : <Navigate to="/login" replace />
}
```

## router/index.tsx

```tsx
export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/upload" replace />,
  },
  {
    element: <AuthLayout />,
    children: [
      { path: '/login', element: <LoginPage /> },
      { path: '/register', element: <RegisterPage /> },
    ]
  },
  {
    element: <PrivateRoute><AppShell /></PrivateRoute>,
    children: [
      { path: '/upload', element: <UploadPage /> },
      { path: '/chat', element: <ChatPage /> },
    ]
  }
])
```

## UX / Visual

- Design minimalista, profissional
- Cores: branco, cinza-50/100, azul-600 (primary), slate para textos
- Fontes: Inter (via Google Fonts ou sistema)
- Responsivo: mobile-first
- Estados de loading claros em todos os botões
- Mensagens de erro amigáveis (sem "Error 422")

## Como rodar

```bash
cd frontend
npm install
cp .env.example .env
npm run dev          # :5173
npm run build        # produção
npm run preview      # preview do build
```

## .env.example

```
VITE_API_BASE_URL=http://localhost:8000
```
