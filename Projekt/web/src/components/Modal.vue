<script setup lang="ts">
defineProps<{
  modelValue: boolean
  naslov: string
}>()

const emit = defineEmits<{
  'update:modelValue': [v: boolean]
}>()
</script>

<template>
  <Teleport to="body">
    <div v-if="modelValue" class="overlay" @click.self="emit('update:modelValue', false)">
      <div class="modal" role="dialog" :aria-label="naslov">
        <div class="modal-zaglavlje">
          <h2 class="modal-naslov">{{ naslov }}</h2>
          <button class="zatvori" @click="emit('update:modelValue', false)">✕</button>
        </div>
        <div class="modal-sadrzaj">
          <slot />
        </div>
        <div v-if="$slots['akcije']" class="modal-akcije">
          <slot name="akcije" />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  width: min(480px, 90vw);
  display: flex;
  flex-direction: column;
}

.modal-zaglavlje {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--boja-rub);
}

.modal-naslov {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.zatvori {
  font-size: 1rem;
  color: var(--boja-tekst-mute);
  background: none;
  border: none;
  cursor: pointer;
  line-height: 1;
  padding: 0.25rem;
}

.zatvori:hover { color: var(--boja-tekst); }

.modal-sadrzaj {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.modal-akcije {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--boja-rub);
}
</style>
