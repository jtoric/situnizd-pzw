export function neprazno(vrijednost: string): string | null {
  return vrijednost.trim().length === 0 ? 'Polje je obavezno.' : null
}

export function validnaDuljina(
  vrijednost: string,
  min: number,
  max: number,
): string | null {
  const d = vrijednost.trim().length
  if (d < min) return `Minimalno ${min} znakova.`
  if (d > max) return `Maksimalno ${max} znakova.`
  return null
}

export function validanDatumProslost(vrijednost: string): string | null {
  if (!vrijednost) return 'Polje je obavezno.'
  const datum = new Date(vrijednost)
  if (isNaN(datum.getTime())) return 'Neispravan datum.'
  if (datum >= new Date()) return 'Datum mora biti u prošlosti.'
  return null
}
