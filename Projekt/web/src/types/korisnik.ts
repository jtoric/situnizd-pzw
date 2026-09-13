export interface KorisnikPodaci {
  id: number
  username: string
  role: 'admin' | 'club'
  is_active: boolean
  club_id: number | null
}
