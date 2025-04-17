import Cookies from 'js-cookie'
import { create } from 'zustand'

const ACCESS_TOKEN = import.meta.env.VITE_ACCESS_TOKEN

interface userAuth {
  email: string;
  name: string;
  userId: string;
  departmentId: string;
  roles: string[]
}

interface AuthState {
  auth: {
    user: userAuth | null
    setUser: (user: userAuth | null) => void
    accessToken: string | null
    setAccessToken: (accessToken: string) => void
    resetAccessToken: () => void
    reset: () => void
  }
}

export const useAuthStore = create<AuthState>()((set) => ({
  auth: {
    user: null,
    setUser: (user) =>
      set((state) => ({ ...state, auth: { ...state.auth, user } })),
    accessToken: Cookies.get(ACCESS_TOKEN) || null,
    setAccessToken: (accessToken) =>
      set((state) => {
        Cookies.set(ACCESS_TOKEN, accessToken, { 
          secure: true,
          sameSite: 'strict'
        })
        return { ...state, auth: { ...state.auth, accessToken } }
      }),
    resetAccessToken: () =>
      set((state) => {
        Cookies.remove(ACCESS_TOKEN)
        return { ...state, auth: { ...state.auth, accessToken: null } }
      }),
    reset: () =>
      set((state) => {
        Cookies.remove(ACCESS_TOKEN)
        return {
          ...state,
          auth: { ...state.auth, user: null, accessToken: null },
        }
      }),
  },
}))

export const useAuth = () => useAuthStore((state) => state.auth)
