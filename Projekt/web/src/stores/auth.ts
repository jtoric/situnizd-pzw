import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/services/api'
import type { KorisnikPodaci } from '@/types/korisnik'
import type { TokenOdgovor } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const trenutniKorisnik = ref<KorisnikPodaci | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))

  const user = computed(() => trenutniKorisnik.value)
  const isAuthenticated = computed(() => !!accessToken.value && !!trenutniKorisnik.value)
  const isAdmin = computed(() => trenutniKorisnik.value?.role === 'admin')
  const isClub = computed(() => trenutniKorisnik.value?.role === 'club')

  async function login(korisnickoIme: string, lozinka: string): Promise<void> {
    const { data } = await api.post<TokenOdgovor>('/auth/login', {
      username: korisnickoIme,
      password: lozinka,
    })
    accessToken.value = data.access_token
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    await dohvatiMene()
  }

  async function dohvatiMene(): Promise<void> {
    const { data } = await api.get<KorisnikPodaci>('/auth/me')
    trenutniKorisnik.value = data
  }

  async function osvjeziToken(): Promise<void> {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) throw new Error('Nema refresh tokena')
    const { data } = await api.post<TokenOdgovor>(
      '/auth/refresh',
      { refresh_token: refreshToken },
      { headers: { Authorization: '' } }, // ne šalji stari (možda istekli) access token
    )
    accessToken.value = data.access_token
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
  }

  function logout(): void {
    trenutniKorisnik.value = null
    accessToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return { user, isAuthenticated, isAdmin, isClub, login, logout, dohvatiMene, osvjeziToken }
})
