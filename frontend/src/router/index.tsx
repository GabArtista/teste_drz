import { createBrowserRouter, Navigate } from 'react-router-dom'
import { LoginPage } from '../pages/LoginPage'
import { RegisterPage } from '../pages/RegisterPage'
import { UploadPage } from '../pages/UploadPage'
import { ChatPage } from '../pages/ChatPage'
import { PrivateRoute } from './PrivateRoute'
import { AuthLayout } from '../components/layouts/AuthLayout'
import { AppShell } from '../components/layouts/AppShell'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/upload" replace />,
  },
  {
    element: <AuthLayout />,
    children: [
      { path: '/login', element: <LoginPage /> },
      { path: '/register', element: <RegisterPage /> },
    ],
  },
  {
    element: (
      <PrivateRoute>
        <AppShell />
      </PrivateRoute>
    ),
    children: [
      { path: '/upload', element: <UploadPage /> },
      { path: '/chat', element: <ChatPage /> },
    ],
  },
])
