<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import {
  dohvatiNatjecatelja,
  kreirajNatjecatelja,
  azurirajNatjecatelja,
} from '@/services/natjecatelji'
import { neprazno, validnaDuljina, validanDatumProslost } from '@/utils/validacija'
import FormaPolje from '@/components/FormaPolje.vue'
import Gumb from '@/components/Gumb.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const obavijesti = useObavijestiStore()

const id = computed(() => {
  const p = route.params['id']
  return p ? Number(p) : null
})
const jeUredi = computed(() => id.value !== null)

const ime = ref('')
const prezime = ref('')
const datumRodenja = ref('')
const spol = ref<'M' | 'F'>('M')
const ucitava = ref(false)

const greske = ref({ ime: '', prezime: '', datumRodenja: '' })

onMounted(async () => {
  if (!jeUredi.value || !id.value) return
  const clubId = auth.user?.club_id
  if (!clubId) return
  try {
    const n = await dohvatiNatjecatelja(clubId, id.value)
    ime.value = n.first_name
    prezime.value = n.last_name
    datumRodenja.value = n.birth_date
    spol.value = n.gender
  } catch {
    obavijesti.greska('Greška pri dohvatu natjecatelja.')
    router.push('/klub/natjecatelji')
  }
})

function validiraj(): boolean {
  greske.value.ime = neprazno(ime.value) ?? validnaDuljina(ime.value, 1, 80) ?? ''
  greske.value.prezime = neprazno(prezime.value) ?? validnaDuljina(prezime.value, 1, 80) ?? ''
  greske.value.datumRodenja = validanDatumProslost(datumRodenja.value) ?? ''
  return !greske.value.ime && !greske.value.prezime && !greske.value.datumRodenja
}

async function spremi(): Promise<void> {
  if (!validiraj()) return
  const clubId = auth.user?.club_id
  if (!clubId) return

  ucitava.value = true
  try {
    if (jeUredi.value && id.value) {
      await azurirajNatjecatelja(clubId, id.value, {
        first_name: ime.value,
        last_name: prezime.value,
        birth_date: datumRodenja.value,
        gender: spol.value,
      })
      obavijesti.uspjeh('Natjecatelj ažuriran.')
    } else {
      await kreirajNatjecatelja(clubId, {
        first_name: ime.value,
        last_name: prezime.value,
        birth_date: datumRodenja.value,
        gender: spol.value,
      })
      obavijesti.uspjeh('Natjecatelj dodan.')
    }
    await router.push('/klub/natjecatelji')
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri spremanju.')
  } finally {
    ucitava.value = false
  }
}
</script>

<template>
  <div class="pogled">
    <h1>{{ jeUredi ? 'Uredi natjecatelja' : 'Novi natjecatelj' }}</h1>

    <form class="forma" @submit.prevent="spremi">
      <FormaPolje oznaka="Ime" v-model="ime" :greska="greske.ime" :obavezno="true" />
      <FormaPolje oznaka="Prezime" v-model="prezime" :greska="greske.prezime" :obavezno="true" />
      <FormaPolje oznaka="Datum rođenja" v-model="datumRodenja" vrsta="date" :greska="greske.datumRodenja" :obavezno="true" />

      <div class="polje">
        <label>Spol</label>
        <div class="radio-grupa">
          <label class="radio"><input v-model="spol" type="radio" value="M" /> Muški</label>
          <label class="radio"><input v-model="spol" type="radio" value="F" /> Ženski</label>
        </div>
      </div>

      <div class="akcije">
        <RouterLink to="/klub/natjecatelji">
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
  max-width: 480px;
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

input[type='text'],
input[type='date'] {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.625rem 0.875rem;
  transition: border-color var(--tranzicija);
}

input:focus {
  outline: none;
  border-color: var(--boja-akcent);
}

.greska-tekst {
  font-size: 0.75rem;
  color: var(--boja-akcent);
}

.radio-grupa {
  display: flex;
  gap: 1.5rem;
}

.radio {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  text-transform: none;
  letter-spacing: 0;
  color: var(--boja-tekst);
  cursor: pointer;
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

.gumb-primarni:hover:not(:disabled) {
  background: var(--boja-tekst);
  color: var(--boja-pozadina);
}

.gumb-primarni:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
