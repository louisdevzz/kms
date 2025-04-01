interface AuthData {
  user: {
    email: string;
    id: string;
  };
  token: string;
  expiresAt: number;
}

export const setAuth = (data: Omit<AuthData, 'expiresAt'>) => {
  const authData: AuthData = {
    ...data,
    expiresAt: new Date().getTime() + 24 * 60 * 60 * 1000, // 24 hours from now
  }
  localStorage.setItem('auth', JSON.stringify(authData))
}

export const getAuth = (): AuthData | null => {
  try {
    const authData = localStorage.getItem('auth')
    if (!authData) return null

    return JSON.parse(authData)
  } catch {
    return null
  }
}

export const checkAuth = () => {
  try {
    const authData = getAuth()
    if (!authData) return false

    const isExpired = new Date().getTime() > authData.expiresAt

    if (isExpired) {
      localStorage.removeItem('auth')
      return false
    }

    return true
  } catch (error) {
    localStorage.removeItem('auth')
    return false
  }
}

export const clearAuth = () => {
  localStorage.removeItem('auth')
} 