// Oblik error odgovora koji backend vraća na non-2xx zahtjeve
export interface BackendGreska {
  code: string
  message: string
}
