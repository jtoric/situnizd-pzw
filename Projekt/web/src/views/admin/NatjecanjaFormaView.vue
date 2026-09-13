<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiNatjecanje, kreirajNatjecanje, azurirajNatjecanje } from '@/services/natjecanja'
import FormaPolje from '@/components/FormaPolje.vue'
import Gumb from '@/components/Gumb.vue'

const route = useRoute()
const router = useRouter()
const obavijesti = useObavijestiStore()

const id = computed(() => {
  const p = route.params['id']
  return p ? Number(p) : null
})
const jeUredi = computed(() => id.value !== null)

const naziv = ref('')
const datum = ref('')
const lokacija = ref('')
const prelimDeadline = ref('')
const finalDeadline = ref('')
const ucitava = ref(false)

const greske = ref({
  naziv: '',
  datum: '',
  lokacija: '',
  prelimDeadline: '',
  finalDeadline: '',
})

onMounted(async () => {
  if (!jeUredi.value || !id.value) return
  try {
    const n = await dohvatiNatjecanje(id.value)
    naziv.value = n.name
    datum.value = n.date
    lokacija.value = n.location
    prelimDeadline.value = n.prelim_deadline.slice(0, 16)
    finalDeadline.value = n.final_deadline.slice(0, 16)
  } catch {
    obavijesti.greska('Greška pri dohvatu natjecanja.')
    router.push('/admin/natjecanja')
  }
})

function validiraj(): boolean {
  greske.value.naziv = naziv.value.trim() ? '' : 'Naziv je obavezan.'
  greske.value.datum = datum.value ? '' : 'Datum je obavezan.'
  greske.value.lokacija = lokacija.value.trim() ? '' : 'Lokacija je obavezna.'
  greske.value.prelimDeadline = prelimDeadline.value ? '' : 'Preliminarni rok je obavezan.'
  greske.value.finalDeadline = finalDeadline.value ? '' : 'Finalni rok je obavezan.'

  if (!greske.value.finalDeadline && !greske.value.prelimDeadline) {
    if (new Date(finalDeadline.value) <= new Date(prelimDeadline.value)) {
      greske.value.finalDeadline = 'Finalni rok mora biti nakon preliminarnog.'
    }
  }

  return !Object.values(greske.value).some(Boolean)
}

async function spremi(): Promise<void> {
  if (!validiraj()) return
  ucitava.value = true
  try {
    const tijelo = {
      name: naziv.value.trim(),
      date: datum.value,
      location: lokacija.value.trim(),
      prelim_deadline: prelimDeadline.value,
      final_deadline: finalDeadline.value,
    }
    if (jeUredi.value && id.value) {
      await azurirajNatjecanje(id.value, tijelo)
      obavijesti.uspjeh('Natjecanje ažurirano.')
    } else {
      await kreirajNatjecanje(tijelo)
      obavijesti.uspjeh('Natjecanje kreirano.')
    }
    await router.push('/admin/natjecanja')
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri spremanju.')
  } finally {
    ucitava.value = false
  }
}
</script>

<template>
  <div class="pogled">
    <h1>{{ jeUredi ? 'Uredi natjecanje' : 'Novo natjecanje' }}</h1>

    <form class="forma" @submit.prevent="spremi">
      <FormaPolje
        oznaka="Naziv"
        v-model="naziv"
        :greska="greske.naziv"
        :obavezno="true"
      />
      <FormaPolje
        oznaka="Datum natjecanja"
        v-model="datum"
        vrsta="date"
        :greska="greske.datum"
        :obavezno="true"
      />
      <FormaPolje
        oznaka="Lokacija"
        v-model="lokacija"
        :greska="greske.lokacija"
        :obavezno="true"
      />
      <FormaPolje
        oznaka="Preliminarni rok"
        v-model="prelimDeadline"
        vrsta="datetime-local"
        :greska="greske.prelimDeadline"
        :obavezno="true"
      />
      <FormaPolje
        oznaka="Finalni rok"
        v-model="finalDeadline"
        vrsta="datetime-local"
        :greska="greske.finalDeadline"
        :obavezno="true"
        pomoc="Mora biti nakon preliminarnog roka."
      />

      <div class="akcije">
        <RouterLink to="/admin/natjecanja">
          <Gumb vrsta="sekundarni">Odustani</Gumb>
        </RouterLink>
        <Gumb tip="submit" :ucitava="ucitava">Spremi</Gumb>
      </div>
    </form>
  </div>
</template>

<style scoped>
.pogled {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 520px;
}

.forma {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 2rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
}

.akcije {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}
</style>
