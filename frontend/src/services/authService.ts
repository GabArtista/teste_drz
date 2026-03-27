import api from '../lib/api'
import type { AuthResponse, User } from '../types'

export const authService = {
  register: (name: string, email: string, password: string) =>
    api.post<AuthResponse>('/auth/register', { name, email, password }),
  login: (email: string, password: string) =>
    api.post<AuthResponse>('/auth/login', { email, password }),
  me: () => api.get<User>('/auth/me'),
}
