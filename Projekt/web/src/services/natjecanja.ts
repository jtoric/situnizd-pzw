import { api } from '@/services/api'
import type { Natjecanje, NatjecanjeKreiranje, NatjecanjeAzuriranje } from '@/types/natjecanje'

export async function dohvatiNatjecanja(): Promise<Natjecanje[]> {
  const { data } = await api.get<Natjecanje[]>('/competitions')
  return data
}

export async function dohvatiNatjecanje(id: number): Promise<Natjecanje> {
  const { data } = await api.get<Natjecanje>(`/competitions/${id}`)
  return data
}

export async function kreirajNatjecanje(tijelo: NatjecanjeKreiranje): Promise<Natjecanje> {
  const { data } = await api.post<Natjecanje>('/competitions', tijelo)
  return data
}

export async function azurirajNatjecanje(
  id: number,
  tijelo: NatjecanjeAzuriranje,
): Promise<Natjecanje> {
  const { data } = await api.patch<Natjecanje>(`/competitions/${id}`, tijelo)
  return data
}
