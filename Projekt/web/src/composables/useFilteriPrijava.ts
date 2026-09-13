import { computed, ref, watch } from 'vue'
import type { Ref } from 'vue'
import type { Prijava } from '@/types/prijava'
import { KATEGORIJE_M, KATEGORIJE_F } from '@/types/prijava'

export interface PrijavaProsirena extends Prijava {
  klub_id: number
  klub_naziv: string
}

export const SVE_KATEGORIJE = [...KATEGORIJE_M, ...KATEGORIJE_F] as const

const VELICINA_STRANICE = 20

export function useFilteriPrijava(prijave: Ref<PrijavaProsirena[]>) {
  const filterStatus = ref<'sve' | 'active' | 'withdrawn'>('sve')
  const filterKlubId = ref<number | 'sve'>('sve')
  const filterLifter = ref('')
  const filterKategorija = ref('')
  const stranica = ref(1)

  const filtrirane = computed(() => {
    let r = prijave.value

    if (filterStatus.value !== 'sve') {
      const s = filterStatus.value
      r = r.filter((p) => p.status === s)
    }
    if (filterKlubId.value !== 'sve') {
      const kid = filterKlubId.value
      r = r.filter((p) => p.klub_id === kid)
    }
    if (filterLifter.value.trim()) {
      const upit = filterLifter.value.toLowerCase()
      r = r.filter((p) =>
        `${p.lifter.first_name} ${p.lifter.last_name}`.toLowerCase().includes(upit),
      )
    }
    if (filterKategorija.value) {
      const kat = filterKategorija.value
      r = r.filter((p) => p.category === kat)
    }
    return r
  })

  const ukupnoStranica = computed(() =>
    Math.max(1, Math.ceil(filtrirane.value.length / VELICINA_STRANICE)),
  )

  watch([filterStatus, filterKlubId, filterLifter, filterKategorija], () => {
    stranica.value = 1
  })

  const trenutnaStranica = computed(() => Math.min(stranica.value, ukupnoStranica.value))

  const prikazane = computed(() => {
    const pocetak = (trenutnaStranica.value - 1) * VELICINA_STRANICE
    return filtrirane.value.slice(pocetak, pocetak + VELICINA_STRANICE)
  })

  function prethodna(): void {
    if (stranica.value > 1) stranica.value--
  }

  function sljedeca(): void {
    if (stranica.value < ukupnoStranica.value) stranica.value++
  }

  return {
    filterStatus,
    filterKlubId,
    filterLifter,
    filterKategorija,
    trenutnaStranica,
    ukupnoStranica,
    filtrirane,
    prikazane,
    prethodna,
    sljedeca,
  }
}
