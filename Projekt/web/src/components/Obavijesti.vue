<script setup lang="ts">
import { useObavijestiStore } from '@/stores/obavijesti'
import Obavijest from './Obavijest.vue'

const store = useObavijestiStore()
</script>

<template>
  <Teleport to="body">
    <div class="obavijesti-kontejner">
      <TransitionGroup name="obavijest">
        <Obavijest
          v-for="o in store.stavke"
          :key="o.id"
          :obavijest="o"
        />
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.obavijesti-kontejner {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 1000;
}

.obavijest-enter-active,
.obavijest-leave-active {
  transition: all var(--tranzicija);
}

.obavijest-enter-from,
.obavijest-leave-to {
  opacity: 0;
  transform: translateX(1rem);
}
</style>
