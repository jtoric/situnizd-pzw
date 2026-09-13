<script setup lang="ts">
import type { Obavijest } from '@/stores/obavijesti'
import { useObavijestiStore } from '@/stores/obavijesti'

const props = defineProps<{ obavijest: Obavijest }>()
const store = useObavijestiStore()
</script>

<template>
  <div
    :class="['obavijest', `obavijest--${props.obavijest.vrsta}`]"
    :data-testid="`obavijest-${props.obavijest.vrsta}`"
    @click="store.ukloni(props.obavijest.id)"
  >
    <span class="poruka">{{ props.obavijest.poruka }}</span>
    <button class="zatvori" aria-label="Zatvori">×</button>
  </div>
</template>

<style scoped>
.obavijest {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border: 1px solid var(--boja-rub);
  background: var(--boja-povrsina);
  cursor: pointer;
  min-width: 280px;
  max-width: 420px;
}

.obavijest--uspjeh {
  border-color: var(--boja-uspjeh);
  color: var(--boja-uspjeh);
}

.obavijest--greska {
  border-color: var(--boja-akcent);
  color: var(--boja-akcent);
}

.obavijest--info {
  border-color: var(--boja-tekst-mute);
  color: var(--boja-tekst);
}

.poruka {
  font-size: 0.8rem;
  line-height: 1.4;
}

.zatvori {
  font-size: 1.25rem;
  color: inherit;
  opacity: 0.6;
  flex-shrink: 0;
}
</style>
