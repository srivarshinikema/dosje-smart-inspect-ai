import api from './api'

export const authService = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password })
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
    }
    return response.data
  },

  logout: () => {
    localStorage.removeItem('access_token')
  },

  getCurrentUser: async () => {
    const response = await api.get('/users/me')
    return response.data
  },

  register: async (email: string, username: string, password: string, fullName?: string, role?: string) => {
    const response = await api.post('/auth/register', {
      email,
      username,
      password,
      full_name: fullName,
      role: role || 'INSPECTOR',
    })
    return response.data
  },
}
