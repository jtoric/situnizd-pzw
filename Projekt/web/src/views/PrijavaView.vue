<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { ApiGreska } from '@/services/api'

const router = useRouter()
const auth = useAuthStore()
const obavijesti = useObavijestiStore()

const korisnickoIme = ref('')
const lozinka = ref('')
const ucitava = ref(false)

async function prijava(): Promise<void> {
  ucitava.value = true
  try {
    await auth.login(korisnickoIme.value, lozinka.value)
    const odrediste = auth.isAdmin ? '/admin/pocetna' : '/klub/pocetna'
    await router.push(odrediste)
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.message : 'Greška pri prijavi.')
  } finally {
    ucitava.value = false
  }
}
</script>

<template>
  <div class="prijava">
    <h1>IRON PRESS</h1>
    <p class="podnaslov">Sustav za registraciju powerlifting natjecanja</p>

    <form class="forma" @submit.prevent="prijava">
      <div class="polje">
        <label for="korisnicko-ime">Korisničko ime</label>
        <input
          id="korisnicko-ime"
          data-testid="korisnicko-ime"
          v-model="korisnickoIme"
          type="text"
          placeholder="korisnik"
          autocomplete="username"
          required
        />
      </div>
      <div class="polje">
        <label for="lozinka">Lozinka</label>
        <input
          id="lozinka"
          data-testid="lozinka"
          v-model="lozinka"
          type="password"
          placeholder="••••••••"
          autocomplete="current-password"
          required
        />
      </div>
      <button type="submit" data-testid="submit" class="gumb-prijava" :disabled="ucitava">
        {{ ucitava ? 'PRIJAVA...' : 'PRIJAVA' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.prijava {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

h1 {
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 3.5rem;
  letter-spacing: 0.08em;
  color: var(--boja-akcent);
}

.podnaslov {
  color: var(--boja-tekst-mute);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: -1.5rem;
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
  gap: 0.5rem;
}

label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--boja-tekst-mute);
}

input {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.75rem 1rem;
  transition: border-color var(--tranzicija);
}

input:focus {
  outline: none;
  border-color: var(--boja-akcent);
}

input::placeholder {
  color: var(--boja-tekst-mute);
  opacity: 0.6;
}

.gumb-prijava {
  background: var(--boja-akcent);
  color: var(--boja-tekst);
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 0.875rem;
  margin-top: 0.5rem;
}

.gumb-prijava:hover:not(:disabled) {
  background: var(--boja-tekst);
  color: var(--boja-pozadina);
}

.gumb-prijava:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
