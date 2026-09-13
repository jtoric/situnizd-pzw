export type Faza = 'OPEN' | 'PRELIM_PASSED' | 'CLOSED'

export const KATEGORIJE_M = ['59', '66', '74', '83', '93', '105', '120', '120+'] as const
export const KATEGORIJE_F = ['47', '52', '57', '63', '69', '76', '84', '84+'] as const

export type KategorijaM = (typeof KATEGORIJE_M)[number]
export type KategorijaF = (typeof KATEGORIJE_F)[number]
export type Kategorija = KategorijaM | KategorijaF

export interface Prijava {
  id: number
  lifter_id: number
  competition_id: number
  category: string
  total: number
  status: 'active' | 'withdrawn'
  registered_at: string | null
  lifter: { first_name: string; last_name: string }
}

export interface PrijavaKreiranje {
  lifter_id: number
  category: string
  total: number
}

export interface PrijavaAzuriranje {
  category?: string
  total?: number
}
