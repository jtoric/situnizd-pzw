export interface Natjecatelj {
  id: number
  first_name: string
  last_name: string
  birth_date: string
  gender: 'M' | 'F'
  club_id: number
}

export interface NatjecateljKreiranje {
  first_name: string
  last_name: string
  birth_date: string
  gender: 'M' | 'F'
}

export interface NatjecateljAzuriranje {
  first_name?: string
  last_name?: string
  birth_date?: string
  gender?: 'M' | 'F'
}
