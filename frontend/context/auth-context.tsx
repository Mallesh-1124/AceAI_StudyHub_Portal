'use client'

import * as React from 'react'
import { useRouter } from 'next/navigation'
import { getMe, login as apiLogin, logout as apiLogout, register as apiRegister, type User } from '@/lib/api'

type LoginCredentials = {
  username: string
  password: string
}

type RegisterCredentials = {
  username: string
  email: string
  password: string
  first_name?: string
  last_name?: string
}

type AuthContextType = {
  user: User | null
  loading: boolean
  login: (credentials: LoginCredentials) => Promise<User>
  register: (credentials: RegisterCredentials) => Promise<User>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = React.createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = React.useState<User | null>(null)
  const [loading, setLoading] = React.useState(true)
  const router = useRouter()

  const refreshUser = React.useCallback(async () => {
    setLoading(true)
    try {
      const currentUser = await getMe()
      setUser(currentUser)
    } catch (error) {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  React.useEffect(() => {
    refreshUser()
  }, [refreshUser])

  const login = React.useCallback(async (credentials: LoginCredentials) => {
    const currentUser = await apiLogin(credentials)
    setUser(currentUser)
    return currentUser
  }, [])

  const register = React.useCallback(async (credentials: RegisterCredentials) => {
    const currentUser = await apiRegister(credentials)
    setUser(currentUser)
    return currentUser
  }, [])

  const logout = React.useCallback(async () => {
    await apiLogout()
    setUser(null)
    router.push('/')
  }, [router])

  const value = React.useMemo(
    () => ({ user, loading, login, register, logout, refreshUser }),
    [user, loading, login, register, logout, refreshUser]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = React.useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
