<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiNatjecanje } from '@/services/natjecanja'
import { dohvatiNatjecatelje } from '@/services/natjecatelji'
import { kreirajPrijavu } from '@/services/prijave'
import { izracunajFazu, dozvoljeno } from '@/utils/faza'
import { KATEGORIJE_M, KATEGORIJE_F } from '@/types/prijava'
import type { Natjecanje } from '@/types/natjecanje'
import type { Natjecatelj } from '@/types/natjecatelj'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const obavijesti = useObavijestiStore()

const compId = Number(route.params['compId'])
const natjecanje = ref<Natjecanje | null>(null)
const natjecatelji = ref<Natjecatelj[]>([])
const ucitava = ref(true)

const odabraniNatjecatelj = ref<number | ''>('')
const odabranaKategorija = ref('')
const total = ref(0)

const faza = computed(() => (natjecanje.value ? izracunajFazu(natjecanje.value) : 'CLOSED'))
const mozePrijava = computed(() => dozvoljeno(faza.value, 'kreiraj'))

const kategorije = computed(() => {
  if (!odabraniNatjecatelj.value) return []
  const n = natjecatelji.value.find((n) => n.id === odabraniNatjecatelj.value)
  return n?.gender === 'M' ? [...KATEGORIJE_M] : [...KATEGORIJE_F]
})

onMounted(async () => {
  const clubId = auth.user?.club_id
  if (!clubId) return
  try {
    const [nat, lifteri] = await Promise.all([
      dohvatiNatjecanje(compId),
      dohvatiNatjecatelje(clubId),
    ])
    natjecanje.value = nat
    natjecatelji.value = lifteri
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri učitavanju.')
    router.push('/klub/natjecanja')
  } finally {
    ucitava.value = false
  }
})

async function prijavi(): Promise<void> {
  if (!mozePrijava.value.ok) return
  if (!odabraniNatjecatelj.value || !odabranaKategorija.value) {
    obavijesti.greska('Odaberite natjecatelja i kategoriju.')
    return
  }
  try {
    await kreirajPrijavu(compId, {
      lifter_id: Number(odabraniNatjecatelj.value),
      category: odabranaKategorija.value,
      total: total.value,
    })
    obavijesti.uspjeh('Prijava uspješna.')
    router.push('/klub/prijave')
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri prijavi.')
  }
}
</script>

<template>
  <div class="pogled">
    <div v-if="ucitava" class="muted">Učitavanje...</div>

    <template v-else-if="natjecanje">
      <h1>{{ natjecanje.name }}</h1>

      <div v-if="!mozePrijava.ok" class="blokada">
        {{ mozePrijava.razlog }}
      </div>

      <form v-else class="forma" @submit.prevent="prijavi">
        <div class="polje">
          <label for="natjecatelj">Natjecatelj</label>
          <select id="natjecatelj" v-model="odabraniNatjecatelj" required>
            <option value="" disabled>— Odaberi natjecatelja —</option>
            <option v-for="n in natjecatelji" :key="n.id" :value="n.id">
              {{ n.first_name }} {{ n.last_name }} ({{ n.gender }})
            </option>
          </select>
        </div>

        <div class="polje">
          <label for="kategorija">Kategorija</label>
          <select id="kategorija" v-model="odabranaKategorija" :disabled="!odabraniNatjecatelj" required>
            <option value="" disabled>— Odaberi kategoriju —</option>
            <option v-for="k in kategorije" :key="k" :value="k">{{ k }} kg</option>
          </select>
        </div>

        <div class="polje">
          <label for="total">Total (kg)</label>
          <input id="total" v-model.number="total" type="number" min="0" />
          <span class="pomoc">Najbolji total u zadnjih 12 mj. (0 = prvo natjecanje)</span>
        </div>

        <div class="akcije">
          <RouterLink to="/klub/natjecanja" class="gumb-sekundarni">Odustani</RouterLink>
          <button type="submit" class="gumb-primarni">Prijavi</button>
        </div>
      </form>
    </template>
  </div>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 480px;
}

.blokada {
  padding: 1rem;
  border: 1px solid var(--boja-akcent);
  color: var(--boja-akcent);
  font-size: 0.875rem;
}

.forma {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 2rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
}

.polje {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
}

select,
input[type='number'] {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.625rem 0.875rem;
}

select:focus,
input:focus {
  outline: none;
  border-color: var(--boja-akcent);
}

.pomoc {
  font-size: 0.7rem;
  color: var(--boja-tekst-mute);
}

.akcije {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.gumb-primarni {
  background: var(--boja-akcent);
  color: var(--boja-tekst);
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 0.625rem 1.5rem;
}

.gumb-primarni:hover {
  background: var(--boja-tekst);
  color: var(--boja-pozadina);
}

.gumb-sekundarni {
  display: inline-flex;
  align-items: center;
  padding: 0.625rem 1.25rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
  transition: color var(--tranzicija), border-color var(--tranzicija);
}

.gumb-sekundarni:hover {
  color: var(--boja-tekst);
  border-color: var(--boja-tekst-mute);
}
</style>
