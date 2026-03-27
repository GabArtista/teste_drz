import { create } from 'zustand'
import type { User } from '../types'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  setAuth: (user: User, token: string) => void
  logout: () => void
  hydrate: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  setAuth: (user, token) => {
    localStorage.setItem('drz_token', token)
    set({ user, token, isAuthenticated: true })
  },

  logout: () => {
    localStorage.removeItem('drz_token')
    set({ user: null, token: null, isAuthenticated: false })
  },

  hydrate: () => {
    const token = localStorage.getItem('drz_token')
    if (token) {
      set({ token, isAuthenticated: true })
    }
  },
}))
