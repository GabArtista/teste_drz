import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../services/authService'
import { useAuthStore } from '../stores/authStore'

export function LoginPage() {
  const navigate = useNavigate()
  const { setAuth, isAuthenticated } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (isAuthenticated) navigate('/upload', { replace: true })
  }, [isAuthenticated, navigate])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await authService.login(email, password)
      setAuth(res.data.user, res.data.access_token)
      navigate('/upload', { replace: true })
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(msg || 'Credenciais inválidas.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="stack stack-tight" onSubmit={handleSubmit}>
      <h2 style={{ marginBottom: '0.5rem' }}>Entrar</h2>
      {error && <div className="feedback-banner feedback-error">{error}</div>}
      <label className="field">
        <span className="field-label">E-mail</span>
        <input className="input" type="email" value={email} onChange={e => setEmail(e.target.value)} required autoFocus />
      </label>
      <label className="field">
        <span className="field-label">Senha</span>
        <input className="input" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
      </label>
      <button className="button" type="submit" disabled={loading}>
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  )
}
