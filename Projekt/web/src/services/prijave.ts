import { api } from '@/services/api'
import type { Prijava, PrijavaKreiranje, PrijavaAzuriranje } from '@/types/prijava'

export async function dohvatiPrijave(compId: number): Promise<Prijava[]> {
  const { data } = await api.get<Prijava[]>(`/competitions/${compId}/registrations`)
  return data
}

export async function dohvatiPrijavu(compId: number, id: number): Promise<Prijava> {
  const { data } = await api.get<Prijava>(`/competitions/${compId}/registrations/${id}`)
  return data
}

export async function kreirajPrijavu(compId: number, tijelo: PrijavaKreiranje): Promise<Prijava> {
  const { data } = await api.post<Prijava>(`/competitions/${compId}/registrations`, tijelo)
  return data
}

export async function azurirajPrijavu(
  compId: number,
  id: number,
  tijelo: PrijavaAzuriranje,
): Promise<Prijava> {
  const { data } = await api.patch<Prijava>(`/competitions/${compId}/registrations/${id}`, tijelo)
  return data
}

export async function odjaviPrijavu(compId: number, id: number): Promise<Prijava> {
  const { data } = await api.post<Prijava>(
    `/competitions/${compId}/registrations/${id}/withdraw`,
  )
  return data
}

export async function reakivirajPrijavu(compId: number, id: number): Promise<Prijava> {
  const { data } = await api.post<Prijava>(
    `/competitions/${compId}/registrations/${id}/reactivate`,
  )
  return data
}
