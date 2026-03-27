import { Outlet, Link, useLocation } from 'react-router-dom'

export function AuthLayout() {
  const location = useLocation()
  const isLogin = location.pathname === '/login'

  return (
    <div className="auth-layout">
      <div className="auth-layout-brand">
        <span className="eyebrow">DRZ</span>
        <strong>Chat com IA</strong>
        <p>Faça perguntas baseadas em qualquer texto que você fornecer.</p>
      </div>
      <div className="auth-layout-card">
        <Outlet />
        <p style={{ textAlign: 'center', marginTop: '1rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
          {isLogin ? (
            <>Não tem conta? <Link to="/register" style={{ color: 'var(--text)' }}>Cadastre-se</Link></>
          ) : (
            <>Já tem conta? <Link to="/login" style={{ color: 'var(--text)' }}>Entrar</Link></>
          )}
        </p>
      </div>
    </div>
  )
}
