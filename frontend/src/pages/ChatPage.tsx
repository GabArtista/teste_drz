import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useChatStore } from '../stores/chatStore'
import { useAuthStore } from '../stores/authStore'

export function ChatPage() {
  const navigate = useNavigate()
  const { messages, isLoading, hasKnowledge, ask, checkKnowledge, clearSession } = useChatStore()
  const { user } = useAuthStore()
  const [question, setQuestion] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    checkKnowledge()
  }, [checkKnowledge])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim() || isLoading) return
    const q = question.trim()
    setQuestion('')
    await ask(q)
  }

  if (!hasKnowledge) {
    return (
      <div className="empty-state">
        <strong>Nenhum texto carregado</strong>
        <p>Antes de fazer perguntas, envie um texto base.</p>
        <button className="button button-secondary" onClick={() => navigate('/upload')}>
          Enviar texto base
        </button>
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 120px)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 600, margin: 0 }}>Perguntas</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: 0 }}>
            A IA responde apenas com base no texto carregado
          </p>
        </div>
        <button
          className="button button-secondary"
          onClick={() => { clearSession(); navigate('/upload') }}
          style={{ fontSize: '0.8rem', padding: '0.25rem 0.75rem' }}
        >
          Alterar texto base
        </button>
      </div>

      <div style={{
        flex: 1,
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
        paddingBottom: '1rem',
      }}>
        {messages.length === 0 && (
          <div style={{
            textAlign: 'center',
            color: 'var(--text-muted)',
            padding: '3rem',
            fontSize: '0.875rem',
          }}>
            Faça sua primeira pergunta sobre o texto carregado.
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              display: 'flex',
              justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
            }}
          >
            <div
              style={{
                maxWidth: '75%',
                padding: '0.75rem 1rem',
                borderRadius: '6px',
                fontSize: '0.875rem',
                lineHeight: 1.6,
                background: msg.role === 'user'
                  ? 'rgba(255,255,255,0.1)'
                  : 'var(--surface-strong)',
                border: '1px solid var(--border)',
                color: 'var(--text)',
              }}
            >
              {msg.role === 'assistant' && (
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>
                  IA
                </div>
              )}
              {msg.role === 'user' && (
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.25rem', textAlign: 'right' }}>
                  {user?.name || 'Você'}
                </div>
              )}
              <p style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{msg.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
            <div style={{
              padding: '0.75rem 1rem',
              borderRadius: '6px',
              background: 'var(--surface-strong)',
              border: '1px solid var(--border)',
              fontSize: '0.875rem',
              color: 'var(--text-muted)',
            }}>
              <span className="spinner" style={{ width: 16, height: 16, display: 'inline-block', marginRight: '0.5rem', verticalAlign: 'middle' }} />
              Processando...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        style={{ display: 'flex', gap: '0.5rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border)' }}
      >
        <input
          className="input"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="Digite sua pergunta..."
          disabled={isLoading}
          style={{ flex: 1 }}
          autoFocus
        />
        <button className="button" type="submit" disabled={isLoading || !question.trim()}>
          Perguntar
        </button>
      </form>
    </div>
  )
}
