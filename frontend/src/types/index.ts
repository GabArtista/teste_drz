export interface User {
  id: string
  name: string
  email: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface KnowledgeResponse {
  id: string | null
  preview: string | null
  char_count: number
  has_text: boolean
}

export interface Message {
  role: 'user' | 'assistant'
  content: string
  created_at?: string
}

export interface AskResponse {
  answer: string
  session_id: string
  sources_found: boolean
}

export interface HistoryResponse {
  session_id: string
  messages: Message[]
}
