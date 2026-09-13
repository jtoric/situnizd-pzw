<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { dohvatiNatjecanja } from '@/services/natjecanja'
import { izracunajFazu, dozvoljeno } from '@/utils/faza'
import type { Natjecanje } from '@/types/natjecanje'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const natjecanja = ref<Natjecanje[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')

onMounted(async () => {
  try {
    const podaci = await dohvatiNatjecanja()
    natjecanja.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu.'
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

function oznakeFaze(n: Natjecanje): string {
  return NAZIV_FAZE[izracunajFazu(n)] ?? izracunajFazu(n)
}
</script>

<template>
  <div class="pogled">
    <h1>Natjecanja</h1>

    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">{{ porukaGreske }}</div>
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
              {{ oznakeFaze(n) }}
            </span>
          </td>
          <td>
            <RouterLink
              v-if="dozvoljeno(izracunajFazu(n), 'kreiraj').ok"
              :to="`/klub/natjecanja/${n.id}/prijava`"
              class="akcija"
            >
              Prijavi se
            </RouterLink>
            <span v-else class="akcija akcija--onemoguceno" :title="dozvoljeno(izracunajFazu(n), 'kreiraj').razlog">
              Prijavi se
            </span>
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

.tablica tbody tr:hover td {
  background: var(--boja-povrsina);
}

.faza-badge {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.5rem;
  border: 1px solid currentColor;
}

.faza-badge--open { color: var(--boja-uspjeh); }
.faza-badge--prelim_passed { color: var(--boja-tekst-mute); }
.faza-badge--closed { color: var(--boja-akcent); }

.akcija {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-akcent);
  transition: opacity var(--tranzicija);
}

.akcija:hover {
  opacity: 0.75;
}

.akcija--onemoguceno {
  color: var(--boja-tekst-mute);
  cursor: not-allowed;
}
</style>
