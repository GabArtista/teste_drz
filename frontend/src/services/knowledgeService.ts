import api from '../lib/api'
import type { KnowledgeResponse } from '../types'

export const knowledgeService = {
  uploadText: (text: string) =>
    api.post<KnowledgeResponse>('/knowledge/upload-text', { text }),
  getCurrent: () =>
    api.get<KnowledgeResponse>('/knowledge/current'),
}
