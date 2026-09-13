<script setup lang="ts" generic="T extends Record<string, unknown>">
defineProps<{
  stupci: { kljuc: string; oznaka: string }[]
  redovi: T[]
  stanje: 'ucitavanje' | 'greska' | 'prazno' | 'spremno'
  porukaPrazno?: string
  porukaGreske?: string
}>()
</script>

<template>
  <div>
    <div v-if="stanje === 'ucitavanje'" class="stanje-poruka muted">Učitavanje...</div>
    <div v-else-if="stanje === 'greska'" class="stanje-poruka greska">
      {{ porukaGreske ?? 'Greška pri dohvatu podataka.' }}
    </div>
    <div v-else-if="stanje === 'prazno'" class="stanje-poruka muted">
      {{ porukaPrazno ?? 'Nema podataka.' }}
    </div>
    <table v-else class="tablica">
      <thead>
        <tr>
          <th v-for="s in stupci" :key="s.kljuc">{{ s.oznaka }}</th>
          <th v-if="$slots['akcije']"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(red, i) in redovi" :key="i">
          <td v-for="s in stupci" :key="s.kljuc">{{ red[s.kljuc] }}</td>
          <td v-if="$slots['akcije']" class="akcije-celija">
            <slot name="akcije" :red="red" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.stanje-poruka {
  padding: 1rem;
  border: 1px solid var(--boja-rub);
  font-size: 0.875rem;
}

.stanje-poruka.greska { border-color: var(--boja-akcent); color: var(--boja-akcent); }

.tablica { width: 100%; border-collapse: collapse; font-size: 0.875rem; }

.tablica th {
  text-align: left;
  padding: 0.625rem 1rem;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
  border-bottom: 2px solid var(--boja-rub);
}

.tablica td { padding: 0.75rem 1rem; border-bottom: 1px solid var(--boja-rub); }
.tablica tbody tr:hover td { background: var(--boja-povrsina); }
.akcije-celija { display: flex; gap: 0.75rem; }
</style>
