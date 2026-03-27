import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../services/authService'
import { useAuthStore } from '../stores/authStore'

export function RegisterPage() {
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await authService.register(name, email, password)
      setAuth(res.data.user, res.data.access_token)
      navigate('/upload', { replace: true })
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(msg || 'Erro ao criar conta.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="stack stack-tight" onSubmit={handleSubmit}>
      <h2 style={{ marginBottom: '0.5rem' }}>Criar conta</h2>
      {error && <div className="feedback-banner feedback-error">{error}</div>}
      <label className="field">
        <span className="field-label">Nome</span>
        <input className="input" type="text" value={name} onChange={e => setName(e.target.value)} required autoFocus />
      </label>
      <label className="field">
        <span className="field-label">E-mail</span>
        <input className="input" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
      </label>
      <label className="field">
        <span className="field-label">Senha (mín. 6 caracteres)</span>
        <input className="input" type="password" value={password} onChange={e => setPassword(e.target.value)} required minLength={6} />
      </label>
      <button className="button" type="submit" disabled={loading}>
        {loading ? 'Criando conta...' : 'Criar conta'}
      </button>
    </form>
  )
}
