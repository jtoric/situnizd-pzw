import type { Faza } from '@/types/prijava'
import type { Natjecanje } from '@/types/natjecanje'

export function izracunajFazu(natjecanje: Natjecanje, sada = new Date()): Faza {
  const prelim = new Date(natjecanje.prelim_deadline)
  const final = new Date(natjecanje.final_deadline)
  if (sada < prelim) return 'OPEN'
  if (sada < final) return 'PRELIM_PASSED'
  return 'CLOSED'
}

export function dozvoljeno(
  faza: Faza,
  akcija: 'kreiraj' | 'promijeni-kategoriju' | 'odjavi' | 'ponovo-prijavi',
): { ok: boolean; razlog?: string } {
  if (akcija === 'kreiraj') {
    return faza === 'OPEN'
      ? { ok: true }
      : { ok: false, razlog: 'Prijave su zatvorene.' }
  }
  return faza !== 'CLOSED'
    ? { ok: true }
    : { ok: false, razlog: 'Natjecanje je zaključano.' }
}
