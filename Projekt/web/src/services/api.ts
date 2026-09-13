import axios from 'axios'
import type { BackendGreska } from '@/types/api'

export class ApiGreska extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
  ) {
    super(message)
    this.name = 'ApiGreska'
  }
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.set('Authorization', `Bearer ${token}`)
  return config
})

// Singleton — sprječava paralelne refreshove (više simultanih 401 odgovora
// ne smije pokrenuti više od jednog refresh poziva)
let osvjezavanjeUTijeku: Promise<void> | null = null

api.interceptors.response.use(
  (response) => response,
  async (error: unknown) => {
    if (!axios.isAxiosError(error) || !error.response) throw error

    const status = error.response.status
    const data = error.response.data as Partial<BackendGreska>

    // Ako nije 401, ili je auth endpoint (login/refresh ne smiju triggerati retry)
    const url = error.config?.url ?? ''
    const jeAuthEndpoint = url.includes('/auth/login') || url.includes('/auth/refresh')
    if (status !== 401 || jeAuthEndpoint) {
      throw new ApiGreska(
        data.code ?? 'unknown_error',
        data.message ?? error.message,
        status,
      )
    }

    // 401 na zaštićenom endpointu — pokušaj refresh
    try {
      if (!osvjezavanjeUTijeku) {
        // Dynamic import izbjegava circular dependency s auth storeom
        const { useAuthStore } = await import('@/stores/auth')
        osvjezavanjeUTijeku = useAuthStore()
          .osvjeziToken()
          .finally(() => {
            osvjezavanjeUTijeku = null
          })
      }
      await osvjezavanjeUTijeku

      // Ponovi originalni zahtjev s novim tokenom
      return api.request(error.config!)
    } catch {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/prijava'
      throw new ApiGreska('session_expired', 'Sesija je istekla.', 401)
    }
  },
)
