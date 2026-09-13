<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiNatjecanja } from '@/services/natjecanja'
import { izracunajFazu } from '@/utils/faza'
import type { Natjecanje } from '@/types/natjecanje'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const obavijesti = useObavijestiStore()
const natjecanja = ref<Natjecanje[]>([])
const stanje = ref<Stanje>('ucitavanje')

onMounted(async () => {
  try {
    const podaci = await dohvatiNatjecanja()
    natjecanja.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri dohvatu natjecanja.')
  }
})

function formatirajDatum(d: string): string {
  return new Date(d).toLocaleDateString('hr-HR')
}

const NAZIV_FAZE: Record<string, string> = {
  OPEN: 'Otvoreno',
  PRELIM_PASSED: 'Prijave zatvorene',
  CLOSED: 'Zaključano',
}
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <h1>Natjecanja</h1>
      <RouterLink to="/admin/natjecanja/novo">
        <button class="gumb-novo">+ Novo natjecanje</button>
      </RouterLink>
    </div>

    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">Greška pri dohvatu.</div>
    <div v-else-if="stanje === 'prazno'" class="stanje-poruka muted">Nema natjecanja.</div>

    <table v-else class="tablica">
      <thead>
        <tr>
          <th>Naziv</th>
          <th>Datum</th>
          <th>Lokacija</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="n in natjecanja" :key="n.id">
          <td>{{ n.name }}</td>
          <td>{{ formatirajDatum(n.date) }}</td>
          <td>{{ n.location }}</td>
          <td>
            <span :class="['faza-badge', `faza-badge--${izracunajFazu(n).toLowerCase()}`]">
              {{ NAZIV_FAZE[izracunajFazu(n)] ?? izracunajFazu(n) }}
            </span>
          </td>
          <td class="akcije-celija">
            <RouterLink :to="`/admin/natjecanja/${n.id}/uredi`" class="akcija">Uredi</RouterLink>
            <RouterLink :to="`/admin/natjecanja/${n.id}/prijave`" class="akcija">Prijave</RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.zaglavlje {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.gumb-novo {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.5rem 1.25rem;
  background: var(--boja-akcent);
  color: var(--boja-tekst);
  border: none;
  cursor: pointer;
}

.gumb-novo:hover { background: var(--boja-tekst); color: var(--boja-pozadina); }

.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
}

.stanje-poruka.greska {
  border-color: var(--boja-akcent);
  color: var(--boja-akcent);
}

.tablica {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.tablica th {
  text-align: left;
  padding: 0.625rem 1rem;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
  border-bottom: 2px solid var(--boja-rub);
}

.tablica td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--boja-rub);
}

.tablica tbody tr:hover td { background: var(--boja-povrsina); }

.faza-badge {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.5rem;
  border: 1px solid currentColor;
}

.faza-badge--open         { color: var(--boja-uspjeh); }
.faza-badge--prelim_passed { color: var(--boja-tekst-mute); }
.faza-badge--closed       { color: var(--boja-akcent); }

.akcije-celija {
  display: flex;
  gap: 1rem;
}

.akcija {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  transition: color var(--tranzicija);
}

.akcija:hover { color: var(--boja-tekst); }
</style>
