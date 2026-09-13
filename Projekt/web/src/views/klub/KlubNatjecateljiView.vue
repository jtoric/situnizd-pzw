<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiNatjecatelje, obrisiNatjecatelja } from '@/services/natjecatelji'
import Tablica from '@/components/Tablica.vue'
import Gumb from '@/components/Gumb.vue'
import type { Natjecatelj } from '@/types/natjecatelj'

type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'

const auth = useAuthStore()
const obavijesti = useObavijestiStore()
const natjecatelji = ref<Natjecatelj[]>([])
const stanje = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')

const stupci = [
  { kljuc: 'first_name', oznaka: 'Ime' },
  { kljuc: 'last_name', oznaka: 'Prezime' },
  { kljuc: 'birth_date', oznaka: 'Datum rođenja' },
  { kljuc: 'gender', oznaka: 'Spol' },
]

async function ucitaj(): Promise<void> {
  const clubId = auth.user?.club_id
  if (!clubId) return
  stanje.value = 'ucitavanje'
  try {
    const podaci = await dohvatiNatjecatelje(clubId)
    natjecatelji.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu.'
  }
}

async function obrisi(id: number): Promise<void> {
  if (!confirm('Obrisati natjecatelja?')) return
  const clubId = auth.user?.club_id
  if (!clubId) return
  try {
    await obrisiNatjecatelja(clubId, id)
    obavijesti.uspjeh('Natjecatelj obrisan.')
    await ucitaj()
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri brisanju.')
  }
}

onMounted(ucitaj)
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <h1>Natjecatelji</h1>
      <RouterLink to="/klub/natjecatelji/novi">
        <Gumb>+ Dodaj</Gumb>
      </RouterLink>
    </div>

    <Tablica
      :stupci="stupci"
      :redovi="(natjecatelji as Record<string, unknown>[])"
      :stanje="stanje"
      :poruka-prazno="'Nema natjecatelja. Dodajte prvog natjecatelja.'"
      :poruka-greske="porukaGreske"
    >
      <template #akcije="{ red }">
        <RouterLink :to="`/klub/natjecatelji/${red['id']}/uredi`" class="akcija">Uredi</RouterLink>
        <Gumb vrsta="opasnost" velicina="mali" @click="obrisi(Number(red['id']))">Obriši</Gumb>
      </template>
    </Tablica>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 1.5rem; }

.zaglavlje {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.akcija {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  transition: color var(--tranzicija);
  align-self: center;
}

.akcija:hover { color: var(--boja-tekst); }
</style>
