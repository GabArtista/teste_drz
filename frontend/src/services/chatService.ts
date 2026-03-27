import api from '../lib/api'
import type { AskResponse, HistoryResponse } from '../types'

export const chatService = {
  ask: (question: string, sessionId?: string | null) =>
    api.post<AskResponse>('/chat/ask', { question, session_id: sessionId }),
  history: (sessionId: string) =>
    api.get<HistoryResponse>(`/chat/history/${sessionId}`),
}
