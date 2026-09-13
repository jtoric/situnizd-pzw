import { describe, it, expect } from 'vitest'
import { neprazno, validnaDuljina, validanDatumProslost } from './validacija'

describe('neprazno', () => {
  it('vraca null za nepraznu vrijednost', () => {
    expect(neprazno('Ivan')).toBeNull()
  })

  it('vraca poruku za prazan string', () => {
    expect(neprazno('')).toBe('Polje je obavezno.')
  })

  it('vraca poruku za string od razmaka', () => {
    expect(neprazno('   ')).toBe('Polje je obavezno.')
  })
})

describe('validnaDuljina', () => {
  it('vraca null za vrijednost u granicama', () => {
    expect(validnaDuljina('Ivan', 1, 80)).toBeNull()
  })

  it('vraca poruku kad je prekratko', () => {
    expect(validnaDuljina('I', 2, 80)).toBe('Minimalno 2 znakova.')
  })

  it('vraca poruku kad je predugo', () => {
    expect(validnaDuljina('a'.repeat(81), 1, 80)).toBe('Maksimalno 80 znakova.')
  })
})

describe('validanDatumProslost', () => {
  it('vraca null za datum u proslosti', () => {
    expect(validanDatumProslost('2000-01-01')).toBeNull()
  })

  it('odbija datum u buducnosti', () => {
    expect(validanDatumProslost('2099-01-01')).toBe('Datum mora biti u prošlosti.')
  })

  it('odbija prazan string', () => {
    expect(validanDatumProslost('')).toBe('Polje je obavezno.')
  })

  it('odbija neispravan datum', () => {
    expect(validanDatumProslost('nije-datum')).toBe('Neispravan datum.')
  })
})
