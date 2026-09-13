import { api } from '@/services/api'
import type { Klub } from '@/types/klub'

export async function dohvatiKlubove(): Promise<Klub[]> {
  const { data } = await api.get<Klub[]>('/clubs')
  return data
}
