import { create } from 'zustand'
import type { Message } from '../types'
import { knowledgeService } from '../services/knowledgeService'
import { chatService } from '../services/chatService'

interface ChatState {
  knowledgeId: string | null
  sessionId: string | null
  messages: Message[]
  isLoading: boolean
  hasKnowledge: boolean
  uploadText: (text: string) => Promise<void>
  ask: (question: string) => Promise<void>
  checkKnowledge: () => Promise<void>
  clearSession: () => void
}

export const useChatStore = create<ChatState>((set, get) => ({
  knowledgeId: null,
  sessionId: null,
  messages: [],
  isLoading: false,
  hasKnowledge: false,

  uploadText: async (text) => {
    const res = await knowledgeService.uploadText(text)
    set({ knowledgeId: res.data.id, hasKnowledge: true })
  },

  ask: async (question) => {
    set((s) => ({
      isLoading: true,
      messages: [...s.messages, { role: 'user', content: question }],
    }))

    try {
      const res = await chatService.ask(question, get().sessionId)
      const { answer, session_id } = res.data
      set((s) => ({
        sessionId: session_id,
        isLoading: false,
        messages: [...s.messages, { role: 'assistant', content: answer }],
      }))
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      const errorMsg = detail ?? 'Erro ao processar a pergunta. Tente novamente.'
      set((s) => ({
        isLoading: false,
        messages: [
          ...s.messages,
          { role: 'assistant', content: `⚠️ ${errorMsg}` },
        ],
      }))
    }
  },

  checkKnowledge: async () => {
    try {
      const res = await knowledgeService.getCurrent()
      set({ hasKnowledge: res.data.has_text, knowledgeId: res.data.id })
    } catch {
      set({ hasKnowledge: false })
    }
  },

  clearSession: () => set({ sessionId: null, messages: [] }),
}))
