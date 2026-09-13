<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiNatjecanje } from '@/services/natjecanja'
import { dohvatiPrijave, odjaviPrijavu } from '@/services/prijave'
import { dohvatiKlubove } from '@/services/klubovi'
import { dohvatiNatjecatelje } from '@/services/natjecatelji'
import { useFilteriPrijava, SVE_KATEGORIJE } from '@/composables/useFilteriPrijava'
import type { PrijavaProsirena } from '@/composables/useFilteriPrijava'
import type { Klub } from '@/types/klub'
import type { Natjecanje } from '@/types/natjecanje'
import { izracunajFazu, dozvoljeno } from '@/utils/faza'
import StatusBadge from '@/components/StatusBadge.vue'
import Modal from '@/components/Modal.vue'
import { uCsv, preuzmiCsv } from '@/utils/csv'

const route = useRoute()
const obavijesti = useObavijestiStore()
const compId = Number(route.params['compId'])

const natjecanje = ref<Natjecanje | null>(null)
const prijave = ref<PrijavaProsirena[]>([])
const klubovi = ref<Klub[]>([])
const ucitava = ref(true)

const {
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
} = useFilteriPrijava(prijave)

onMounted(async () => {
  try {
    const [nat, sveKlubove, svePrijave] = await Promise.all([
      dohvatiNatjecanje(compId),
      dohvatiKlubove(),
      dohvatiPrijave(compId),
    ])

    natjecanje.value = nat
    klubovi.value = sveKlubove

    // Dohvati liftera po klubu da bi saznali club_id za svaku prijavu
    const lifterMap = new Map<number, { klub_id: number; klub_naziv: string }>()
    await Promise.all(
      sveKlubove.map(async (k) => {
        const lifteri = await dohvatiNatjecatelje(k.id)
        for (const l of lifteri) {
          lifterMap.set(l.id, { klub_id: k.id, klub_naziv: k.name })
        }
      }),
    )

    prijave.value = svePrijave.map((p) => {
      const info = lifterMap.get(p.lifter_id)
      return {
        ...p,
        klub_id: info?.klub_id ?? 0,
        klub_naziv: info?.klub_naziv ?? '—',
      }
    })
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri dohvatu prijava.')
  } finally {
    ucitava.value = false
  }
})

const mozePrijava = computed(() =>
  natjecanje.value ? dozvoljeno(izracunajFazu(natjecanje.value), 'odjavi') : { ok: false, razlog: 'Učitavanje...' },
)

function formatirajDatum(d: string | null): string {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('hr-HR')
}

// --- CSV export ---
function izvezCsv(): void {
  const naziv = natjecanje.value?.name ?? 'prijave'
  const datum = new Date().toISOString().slice(0, 10)
  const redovi = filtrirane.value.map((p) => ({
    id: p.id,
    lifter: `${p.lifter.first_name} ${p.lifter.last_name}`,
    klub: p.klub_naziv,
    kategorija: p.category,
    total: p.total,
    status: p.status,
    registered_at: p.registered_at ?? '',
  }))
  const sadrzaj = uCsv(redovi, ['id', 'lifter', 'klub', 'kategorija', 'total', 'status', 'registered_at'])
  preuzmiCsv(`prijave-${naziv}-${datum}.csv`, sadrzaj)
}

// --- Odjava modal ---
const modalOtvoren = ref(false)
const modalPrijava = ref<PrijavaProsirena | null>(null)
const modalRazlog = ref('')
const odjavaUTijeku = ref(false)

function otvoriOdjavu(p: PrijavaProsirena): void {
  modalPrijava.value = p
  modalRazlog.value = ''
  modalOtvoren.value = true
}

interface AdminLogEntry {
  regId: number
  razlog: string
  ts: string
}

async function potvrdiOdjavu(): Promise<void> {
  if (!modalPrijava.value) return
  odjavaUTijeku.value = true
  try {
    const azurirano = await odjaviPrijavu(compId, modalPrijava.value.id)
    modalPrijava.value.status = azurirano.status

    // Razlog se ne šalje backendu — sprema se lokalno kao administrativni dnevnik
    const log: AdminLogEntry[] = JSON.parse(localStorage.getItem('adminLog') ?? '[]') as AdminLogEntry[]
    log.push({ regId: modalPrijava.value.id, razlog: modalRazlog.value, ts: new Date().toISOString() })
    localStorage.setItem('adminLog', JSON.stringify(log))

    obavijesti.uspjeh('Prijava odjavljena.')
    modalOtvoren.value = false
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri odjavi.')
  } finally {
    odjavaUTijeku.value = false
  }
}
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <div>
        <RouterLink to="/admin/natjecanja" class="natrag">← Natjecanja</RouterLink>
        <h1>{{ natjecanje?.name ?? 'Prijave' }}</h1>
      </div>
      <button v-if="!ucitava && filtrirane.length > 0" class="gumb-csv" @click="izvezCsv">
        Izvezi CSV
      </button>
    </div>

    <div v-if="ucitava" class="stanje-poruka muted">Učitavanje...</div>

    <template v-else>
      <!-- Filteri -->
      <div class="filteri">
        <select v-model="filterStatus" class="select-filter">
          <option value="sve">Sve prijave</option>
          <option value="active">Aktivne</option>
          <option value="withdrawn">Odjavljene</option>
        </select>

        <select v-model="filterKlubId" class="select-filter">
          <option value="sve">Svi klubovi</option>
          <option v-for="k in klubovi" :key="k.id" :value="k.id">{{ k.name }}</option>
        </select>

        <input
          v-model="filterLifter"
          class="input-filter"
          placeholder="Traži natjecatelja..."
          type="text"
        />

        <select v-model="filterKategorija" class="select-filter">
          <option value="">Sve kategorije</option>
          <option v-for="kat in SVE_KATEGORIJE" :key="kat" :value="kat">{{ kat }} kg</option>
        </select>
      </div>

      <!-- Tablica -->
      <div v-if="filtrirane.length === 0" class="stanje-poruka muted">
        Nema prijava za odabrane filtere.
      </div>

      <template v-else>
        <table class="tablica">
          <thead>
            <tr>
              <th>Natjecatelj</th>
              <th>Klub</th>
              <th>Kategorija</th>
              <th>Total</th>
              <th>Status</th>
              <th>Prijavljeno</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in prikazane" :key="p.id">
              <td>{{ p.lifter.first_name }} {{ p.lifter.last_name }}</td>
              <td>{{ p.klub_naziv }}</td>
              <td>{{ p.category }} kg</td>
              <td>{{ p.total }} kg</td>
              <td><StatusBadge :status="p.status" /></td>
              <td class="muted">{{ formatirajDatum(p.registered_at) }}</td>
              <td>
                <button
                  v-if="p.status === 'active'"
                  class="akcija akcija--opasnost"
                  :disabled="!mozePrijava.ok"
                  :title="mozePrijava.razlog"
                  @click="otvoriOdjavu(p)"
                >
                  Odjavi
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Paginacija -->
        <div class="paginacija">
          <button class="pag-gumb" :disabled="trenutnaStranica === 1" @click="prethodna">
            ← Prethodno
          </button>
          <span class="muted">Stranica {{ trenutnaStranica }} od {{ ukupnoStranica }}</span>
          <button
            class="pag-gumb"
            :disabled="trenutnaStranica === ukupnoStranica"
            @click="sljedeca"
          >
            Sljedeće →
          </button>
        </div>
      </template>
    </template>
  </div>

  <!-- Modal: odjava -->
  <Modal v-model="modalOtvoren" naslov="Odjavi prijavu">
    <template v-if="modalPrijava">
      <p class="modal-info">
        <strong>{{ modalPrijava.lifter.first_name }} {{ modalPrijava.lifter.last_name }}</strong>
        &mdash; {{ modalPrijava.category }} kg &mdash; {{ modalPrijava.klub_naziv }}
      </p>
      <div class="polje">
        <label for="razlog">Razlog odjave</label>
        <textarea id="razlog" v-model="modalRazlog" class="textarea" rows="3" placeholder="Neobavezno..." />
      </div>
    </template>

    <template #akcije>
      <button class="pag-gumb" @click="modalOtvoren = false">Odustani</button>
      <button class="gumb-opasnost" :disabled="odjavaUTijeku" @click="potvrdiOdjavu">
        {{ odjavaUTijeku ? 'Odjava...' : 'Potvrdi odjavu' }}
      </button>
    </template>
  </Modal>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.zaglavlje { display: flex; align-items: flex-start; justify-content: space-between; }

.natrag {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  display: block;
  margin-bottom: 0.5rem;
}

.natrag:hover { color: var(--boja-tekst); }

.gumb-csv {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.5rem 1.25rem;
  background: transparent;
  color: var(--boja-tekst-mute);
  border: 1px solid var(--boja-rub);
  cursor: pointer;
  align-self: flex-end;
}

.gumb-csv:hover { color: var(--boja-tekst); border-color: var(--boja-tekst-mute); }

.filteri {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.select-filter,
.input-filter {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.5rem 0.75rem;
  font-size: 0.8rem;
  font-family: var(--font-body);
}

.select-filter:focus,
.input-filter:focus {
  outline: none;
  border-color: var(--boja-akcent);
}

.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
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

.paginacija {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  font-size: 0.8rem;
}

.pag-gumb {
  font-family: var(--font-body);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  background: none;
  border: 1px solid var(--boja-rub);
  padding: 0.375rem 0.875rem;
  cursor: pointer;
}

.pag-gumb:hover:not(:disabled) { color: var(--boja-tekst); border-color: var(--boja-tekst-mute); }
.pag-gumb:disabled { opacity: 0.35; cursor: not-allowed; }

.akcija {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: none;
  border: none;
  cursor: pointer;
}

.akcija--opasnost { color: var(--boja-tekst-mute); }
.akcija--opasnost:hover { color: var(--boja-akcent); }

.modal-info {
  font-size: 0.875rem;
  padding: 0.75rem 1rem;
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
}

.polje {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.polje label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
}

.textarea {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.625rem 0.875rem;
  font-family: var(--font-body);
  font-size: 0.875rem;
  resize: vertical;
}

.textarea:focus {
  outline: none;
  border-color: var(--boja-akcent);
}

.gumb-opasnost {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.5rem 1.25rem;
  background: transparent;
  color: var(--boja-akcent);
  border: 1px solid var(--boja-akcent);
  cursor: pointer;
}

.gumb-opasnost:hover:not(:disabled) { background: var(--boja-akcent); color: var(--boja-tekst); }
.gumb-opasnost:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
