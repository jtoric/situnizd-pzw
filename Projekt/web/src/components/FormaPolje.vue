<script setup lang="ts">
defineProps<{
  oznaka: string
  modelValue: string | number
  vrsta?: string
  greska?: string
  obavezno?: boolean
  pomoc?: string
}>()

defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <div class="polje">
    <label :for="oznaka">
      {{ oznaka }}<span v-if="obavezno" class="obavezno">*</span>
    </label>
    <input
      :id="oznaka"
      :type="vrsta ?? 'text'"
      :value="modelValue"
      :required="obavezno"
      :class="{ 'input--greska': greska }"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <span v-if="greska" class="greska-tekst">{{ greska }}</span>
    <span v-else-if="pomoc" class="pomoc-tekst">{{ pomoc }}</span>
  </div>
</template>

<style scoped>
.polje { display: flex; flex-direction: column; gap: 0.4rem; }

label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst-mute);
}

.obavezno { color: var(--boja-akcent); margin-left: 0.2rem; }

input {
  background: var(--boja-pozadina);
  border: 1px solid var(--boja-rub);
  color: var(--boja-tekst);
  padding: 0.625rem 0.875rem;
  transition: border-color var(--tranzicija);
}

input:focus { outline: none; border-color: var(--boja-akcent); }
input.input--greska { border-color: var(--boja-akcent); }

.greska-tekst { font-size: 0.75rem; color: var(--boja-akcent); }
.pomoc-tekst  { font-size: 0.7rem; color: var(--boja-tekst-mute); }
</style>
