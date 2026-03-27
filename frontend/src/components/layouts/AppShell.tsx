import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'

export function AppShell() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <header style={{
        borderBottom: '1px solid var(--border)',
        padding: '0 1.5rem',
        height: '52px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'var(--surface)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
          <strong style={{ fontSize: '0.9rem', letterSpacing: '0.05em' }}>DRZ CHAT</strong>
          <nav style={{ display: 'flex', gap: '0.25rem' }}>
            <NavLink
              to="/upload"
              style={({ isActive }) => ({
                padding: '0.25rem 0.75rem',
                borderRadius: '4px',
                fontSize: '0.85rem',
                color: isActive ? 'var(--text)' : 'var(--text-muted)',
                background: isActive ? 'var(--surface-muted)' : 'transparent',
                textDecoration: 'none',
              })}
            >
              Texto Base
            </NavLink>
            <NavLink
              to="/chat"
              style={({ isActive }) => ({
                padding: '0.25rem 0.75rem',
                borderRadius: '4px',
                fontSize: '0.85rem',
                color: isActive ? 'var(--text)' : 'var(--text-muted)',
                background: isActive ? 'var(--surface-muted)' : 'transparent',
                textDecoration: 'none',
              })}
            >
              Perguntas
            </NavLink>
          </nav>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {user && (
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{user.name}</span>
          )}
          <button className="button button-secondary" onClick={handleLogout} style={{ fontSize: '0.8rem', padding: '0.25rem 0.75rem' }}>
            Sair
          </button>
        </div>
      </header>
      <main style={{ flex: 1, padding: '2rem', maxWidth: '900px', margin: '0 auto', width: '100%' }}>
        <Outlet />
      </main>
    </div>
  )
}
