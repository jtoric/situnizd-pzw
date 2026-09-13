export interface Natjecanje {
  id: number
  name: string
  date: string
  location: string
  prelim_deadline: string
  final_deadline: string
}

export interface NatjecanjeKreiranje {
  name: string
  date: string
  location: string
  prelim_deadline: string
  final_deadline: string
}

export interface NatjecanjeAzuriranje {
  name?: string
  date?: string
  location?: string
  prelim_deadline?: string
  final_deadline?: string
}
