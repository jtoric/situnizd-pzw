<script setup lang="ts">
defineProps<{ status: string }>()
</script>

<template>
  <span :class="['badge', `badge--${status}`]">{{ status }}</span>
</template>

<style scoped>
.badge {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.5rem;
  border: 1px solid currentColor;
  white-space: nowrap;
}

.badge--active { color: var(--boja-uspjeh); }
.badge--withdrawn { color: var(--boja-tekst-mute); }
</style>
