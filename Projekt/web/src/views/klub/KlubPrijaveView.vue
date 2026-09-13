<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiNatjecanja } from '@/services/natjecanja'
import { dohvatiPrijave, azurirajPrijavu, odjaviPrijavu, reakivirajPrijavu } from '@/services/prijave'
import { izracunajFazu, dozvoljeno } from '@/utils/faza'
import { KATEGORIJE_M, KATEGORIJE_F } from '@/types/prijava'
import StatusBadge from '@/components/StatusBadge.vue'
import type { Natjecanje } from '@/types/natjecanje'
import type { Prijava } from '@/types/prijava'

interface GrupaPrijava {
  natjecanje: Natjecanje
  prijave: Prijava[]
}

const auth = useAuthStore()
const obavijesti = useObavijestiStore()
const grupe = ref<GrupaPrijava[]>([])
const ucitava = ref(true)

onMounted(async () => {
  const clubId = auth.user?.club_id
  if (!clubId) return
  try {
    const natjecanja = await dohvatiNatjecanja()
    const rezultati = await Promise.all(
      natjecanja.map(async (n) => {
        const sve = await dohvatiPrijave(n.id)
        return { natjecanje: n, prijave: sve }
      }),
    )
    grupe.value = rezultati.filter((g) => g.prijave.length > 0)
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri dohvatu prijava.')
  } finally {
    ucitava.value = false
  }
})

const uredivanjeId = ref<number | null>(null)
const novaKategorija = ref('')

function pocniUredi(prijava: Prijava): void {
  uredivanjeId.value = prijava.id
  novaKategorija.value = prijava.category
}

async function spremiKategoriju(compId: number, prijava: Prijava): Promise<void> {
  try {
    await azurirajPrijavu(compId, prijava.id, { category: novaKategorija.value })
    prijava.category = novaKategorija.value
    obavijesti.uspjeh('Kategorija ažurirana.')
    uredivanjeId.value = null
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri ažuriranju.')
  }
}

async function odjavi(compId: number, prijava: Prijava): Promise<void> {
  const ime = `${prijava.lifter.first_name} ${prijava.lifter.last_name}`
  if (!confirm(`Odjaviti natjecatelja ${ime}?`)) return
  try {
    const azurirano = await odjaviPrijavu(compId, prijava.id)
    prijava.status = azurirano.status
    obavijesti.uspjeh(`${ime} odjavljen.`)
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri odjavi.')
  }
}

async function reakiviraj(compId: number, prijava: Prijava): Promise<void> {
  const ime = `${prijava.lifter.first_name} ${prijava.lifter.last_name}`
  try {
    const azurirano = await reakivirajPrijavu(compId, prijava.id)
    prijava.status = azurirano.status
    obavijesti.uspjeh(`${ime} ponovo prijavljen.`)
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri ponovnoj prijavi.')
  }
}

function kategorijeZaPrijavu(prijava: Prijava): readonly string[] {
  return (KATEGORIJE_M as readonly string[]).includes(prijava.category) ? KATEGORIJE_M : KATEGORIJE_F
}
</script>

<template>
  <div class="pogled">
    <h1>Moje prijave</h1>

    <div v-if="ucitava" class="muted">Učitavanje...</div>
    <div v-else-if="grupe.length === 0" class="stanje-poruka muted">
      Nema aktivnih prijava.
    </div>

    <template v-else>
      <section v-for="g in grupe" :key="g.natjecanje.id" class="sekcija">
        <div class="sekcija-zaglavlje">
          <h2>{{ g.natjecanje.name }}</h2>
          <span class="datum muted">{{ new Date(g.natjecanje.date).toLocaleDateString('hr-HR') }}</span>
        </div>

        <table class="tablica">
          <thead>
            <tr>
              <th>Natjecatelj</th>
              <th>Kategorija</th>
              <th>Total</th>
              <th>Status</th>
              <th>Prijavljeno</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in g.prijave" :key="p.id">
              <td>{{ p.lifter.first_name }} {{ p.lifter.last_name }}</td>
              <td>
                <template v-if="uredivanjeId === p.id">
                  <select v-model="novaKategorija" class="select-inline">
                    <option v-for="k in kategorijeZaPrijavu(p)" :key="k" :value="k">
                      {{ k }} kg
                    </option>
                  </select>
                </template>
                <template v-else>{{ p.category }} kg</template>
              </td>
              <td>{{ p.total }} kg</td>
              <td><StatusBadge :status="p.status" /></td>
              <td class="muted">
                {{ p.registered_at ? new Date(p.registered_at).toLocaleDateString('hr-HR') : '—' }}
              </td>
              <td class="akcije-celija">
                <template v-if="p.status === 'active'">
                  <template v-if="uredivanjeId === p.id">
                    <button class="akcija" @click="spremiKategoriju(g.natjecanje.id, p)">Spremi</button>
                    <button class="akcija" @click="uredivanjeId = null">Odustani</button>
                  </template>
                  <template v-else>
                    <button
                      class="akcija"
                      :disabled="!dozvoljeno(izracunajFazu(g.natjecanje), 'promijeni-kategoriju').ok"
                      :title="dozvoljeno(izracunajFazu(g.natjecanje), 'promijeni-kategoriju').razlog"
                      @click="pocniUredi(p)"
                    >
                      Promijeni kategoriju
                    </button>
                    <button
                      class="akcija akcija--brisanje"
                      :disabled="!dozvoljeno(izracunajFazu(g.natjecanje), 'odjavi').ok"
                      :title="dozvoljeno(izracunajFazu(g.natjecanje), 'odjavi').razlog"
                      @click="odjavi(g.natjecanje.id, p)"
                    >
                      Odjavi
                    </button>
                  </template>
                </template>
                <template v-else>
                  <button
                    class="akcija"
                    :disabled="!dozvoljeno(izracunajFazu(g.natjecanje), 'ponovo-prijavi').ok"
                    :title="dozvoljeno(izracunajFazu(g.natjecanje), 'ponovo-prijavi').razlog"
                    @click="reakiviraj(g.natjecanje.id, p)"
                  >
                    Ponovo prijavi
                  </button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </template>
  </div>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
}

.sekcija {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.sekcija-zaglavlje {
  display: flex;
  align-items: baseline;
  gap: 1rem;
}

.sekcija-zaglavlje h2 {
  font-size: 1.25rem;
}

.datum { font-size: 0.8rem; }

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

.select-inline {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

.akcije-celija {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.akcija {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  transition: color var(--tranzicija);
}

.akcija:hover:not(:disabled) { color: var(--boja-tekst); }
.akcija--brisanje:hover:not(:disabled) { color: var(--boja-akcent); }
.akcija:disabled { opacity: 0.35; cursor: not-allowed; }
</style>
