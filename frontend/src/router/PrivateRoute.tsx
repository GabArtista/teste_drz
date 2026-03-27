import { type ReactNode, useEffect } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'

export function PrivateRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, hydrate } = useAuthStore()

  useEffect(() => {
    hydrate()
  }, [hydrate])

  const token = localStorage.getItem('drz_token')
  if (!token) return <Navigate to="/login" replace />

  return <>{children}</>
}
