import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('authStore', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('starts unauthenticated', async () => {
    const { useAuthStore } = await import('../stores/authStore')
    const store = useAuthStore.getState()
    expect(store.isAuthenticated).toBe(false)
    expect(store.token).toBeNull()
  })

  it('setAuth stores token', async () => {
    const { useAuthStore } = await import('../stores/authStore')
    useAuthStore.getState().setAuth({ id: '1', name: 'Test', email: 'test@test.com' }, 'mytoken')
    expect(useAuthStore.getState().isAuthenticated).toBe(true)
    expect(useAuthStore.getState().token).toBe('mytoken')
    expect(localStorage.getItem('drz_token')).toBe('mytoken')
  })

  it('logout clears state', async () => {
    const { useAuthStore } = await import('../stores/authStore')
    useAuthStore.getState().setAuth({ id: '1', name: 'Test', email: 'test@test.com' }, 'mytoken')
    useAuthStore.getState().logout()
    expect(useAuthStore.getState().isAuthenticated).toBe(false)
    expect(useAuthStore.getState().token).toBeNull()
    expect(localStorage.getItem('drz_token')).toBeNull()
  })
})
