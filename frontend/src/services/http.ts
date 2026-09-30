import axios, { type AxiosInstance } from 'axios'

import { API_BASE_URL } from '@/constants/api'
import { useAuthStore } from '@/stores/auth.store'

export interface ApiError {
  code: string
  message: string
  details: unknown
  requestId: string | null
}

export class HttpError extends Error {
  constructor(
    public status: number,
    public apiError: ApiError,
  ) {
    super(apiError.message)
  }
}

export const http: AxiosInstance = axios.create({ baseURL: API_BASE_URL })

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

let refreshInFlight: Promise<string> | null = null

http.interceptors.response.use(
  (response) => response,
  async (error) => {
    const auth = useAuthStore()
    const original = error.config

    if (error.response?.status === 401 && auth.refreshToken && !original._retried) {
      original._retried = true
      try {
        refreshInFlight ??= auth.refreshAccessToken()
        const newToken = await refreshInFlight
        refreshInFlight = null
        original.headers.Authorization = `Bearer ${newToken}`
        return http(original)
      } catch {
        auth.logout()
      }
    }

    const body = error.response?.data?.error
    if (body) {
      throw new HttpError(error.response.status, {
        code: body.code,
        message: body.message,
        details: body.details,
        requestId: body.request_id ?? null,
      })
    }
    throw error
  },
)
