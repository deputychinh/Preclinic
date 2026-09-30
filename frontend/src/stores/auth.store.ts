import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { API_BASE_URL, API_ENDPOINTS } from '@/constants/api'
import type { Role } from '@/enums'
import type { CurrentUser } from '@/types/models'

const ACCESS_TOKEN_KEY = 'carepath.access'
const REFRESH_TOKEN_KEY = 'carepath.refresh'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(sessionStorage.getItem(ACCESS_TOKEN_KEY))
  const refreshToken = ref<string | null>(sessionStorage.getItem(REFRESH_TOKEN_KEY))
  const currentUser = ref<CurrentUser | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value)
  const role = computed<Role | null>(() => currentUser.value?.role ?? null)

  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    sessionStorage.setItem(ACCESS_TOKEN_KEY, access)
    sessionStorage.setItem(REFRESH_TOKEN_KEY, refresh)
  }

  async function login(email: string, password: string) {
    const response = await axios.post(`${API_BASE_URL}${API_ENDPOINTS.login}`, { email, password })
    setTokens(response.data.data.access, response.data.data.refresh)
    await loadCurrentUser()
  }

  async function loadCurrentUser() {
    const { http } = await import('@/services/http')
    const response = await http.get(API_ENDPOINTS.me)
    const data = response.data.data
    currentUser.value = { id: data.id, email: data.email, fullName: data.full_name, role: data.role }
  }

  async function refreshAccessToken(): Promise<string> {
    if (!refreshToken.value) throw new Error('No refresh token')
    const response = await axios.post(`${API_BASE_URL}${API_ENDPOINTS.refresh}`, {
      refresh: refreshToken.value,
    })
    accessToken.value = response.data.data.access
    sessionStorage.setItem(ACCESS_TOKEN_KEY, response.data.data.access)
    return response.data.data.access
  }

  function logout() {
    accessToken.value = null
    refreshToken.value = null
    currentUser.value = null
    sessionStorage.removeItem(ACCESS_TOKEN_KEY)
    sessionStorage.removeItem(REFRESH_TOKEN_KEY)
  }

  return { accessToken, refreshToken, currentUser, isAuthenticated, role, login, loadCurrentUser, refreshAccessToken, logout }
})
