import { api } from '@/services/api'
import type { Natjecatelj, NatjecateljKreiranje, NatjecateljAzuriranje } from '@/types/natjecatelj'

export async function dohvatiNatjecatelje(clubId: number): Promise<Natjecatelj[]> {
  const { data } = await api.get<Natjecatelj[]>(`/clubs/${clubId}/lifters`, {
    params: { limit: 100 },
  })
  return data
}

export async function dohvatiNatjecatelja(clubId: number, id: number): Promise<Natjecatelj> {
  const { data } = await api.get<Natjecatelj>(`/clubs/${clubId}/lifters/${id}`)
  return data
}

export async function kreirajNatjecatelja(
  clubId: number,
  tijelo: NatjecateljKreiranje,
): Promise<Natjecatelj> {
  const { data } = await api.post<Natjecatelj>(`/clubs/${clubId}/lifters`, tijelo)
  return data
}

export async function azurirajNatjecatelja(
  clubId: number,
  id: number,
  tijelo: NatjecateljAzuriranje,
): Promise<Natjecatelj> {
  const { data } = await api.patch<Natjecatelj>(`/clubs/${clubId}/lifters/${id}`, tijelo)
  return data
}

export async function obrisiNatjecatelja(clubId: number, id: number): Promise<void> {
  await api.delete(`/clubs/${clubId}/lifters/${id}`)
}
