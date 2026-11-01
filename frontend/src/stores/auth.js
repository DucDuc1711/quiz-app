import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '../api/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('access_token') || null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value && user.value.role === 'admin')

  async function login(credentials) {
    const response = await apiClient.post('/auth/login', credentials)
    token.value = response.data.access_token
    user.value = response.data.user
    localStorage.setItem('access_token', token.value)
    localStorage.setItem('user', JSON.stringify(user.value))
    return response.data
  }

  async function register(userData) {
    const response = await apiClient.post('/auth/register', userData)
    token.value = response.data.access_token
    user.value = response.data.user
    localStorage.setItem('access_token', token.value)
    localStorage.setItem('user', JSON.stringify(user.value))
    return response.data
  }

  async function fetchMe() {
    try {
      const response = await apiClient.get('/auth/me')
      user.value = response.data.user
      localStorage.setItem('user', JSON.stringify(user.value))
    } catch (e) {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    login,
    register,
    fetchMe,
    logout
  }
})
