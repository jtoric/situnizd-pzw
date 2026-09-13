<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

async function odjava(): Promise<void> {
  auth.logout()
  await router.push('/prijava')
}
</script>

<template>
  <nav class="nav">
    <RouterLink to="/" class="brand">IRON PRESS</RouterLink>

    <div v-if="auth.isAdmin" class="linkovi">
      <RouterLink to="/admin/pocetna" class="link">Početna</RouterLink>
      <RouterLink to="/admin/klubovi" class="link">Klubovi</RouterLink>
      <RouterLink to="/admin/natjecanja" class="link">Natjecanja</RouterLink>
    </div>

    <div v-else-if="auth.isClub" class="linkovi">
      <RouterLink to="/klub/pocetna" class="link">Početna</RouterLink>
      <RouterLink to="/klub/natjecatelji" class="link">Natjecatelji</RouterLink>
      <RouterLink to="/klub/natjecanja" class="link">Natjecanja</RouterLink>
      <RouterLink to="/klub/prijave" class="link">Prijave</RouterLink>
    </div>

    <div v-if="auth.isAuthenticated" class="desno">
      <span class="korisnik">{{ auth.user?.username }}</span>
      <button class="gumb-odjava" @click="odjava">Odjava</button>
    </div>
  </nav>
</template>

<style scoped>
.nav {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 0 2rem;
  height: 56px;
  background: var(--boja-povrsina);
  border-bottom: 2px solid var(--boja-rub);
}

.brand {
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 1.25rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--boja-akcent);
  white-space: nowrap;
}

.linkovi {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex: 1;
}

.link {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  padding: 0.375rem 0.75rem;
  transition: color var(--tranzicija);
}

.link:hover,
.link.router-link-active {
  color: var(--boja-tekst);
}

.link.router-link-active {
  border-bottom: 2px solid var(--boja-akcent);
}

.desno {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.korisnik {
  font-size: 0.75rem;
  color: var(--boja-tekst-mute);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.gumb-odjava {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--boja-rub);
  transition: color var(--tranzicija), border-color var(--tranzicija);
}

.gumb-odjava:hover {
  color: var(--boja-akcent);
  border-color: var(--boja-akcent);
}
</style>
