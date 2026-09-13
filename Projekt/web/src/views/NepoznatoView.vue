<script setup lang="ts">
// 404 stranica
</script>

<template>
  <div class="nepoznato">
    <h1>404</h1>
    <p class="muted">Stranica nije pronađena.</p>
    <RouterLink to="/" class="veza">← Povratak</RouterLink>
  </div>
</template>

<style scoped>
.nepoznato {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

h1 {
  font-size: 6rem;
  color: var(--boja-akcent);
  letter-spacing: -0.02em;
}

.veza {
  color: var(--boja-tekst-mute);
  font-size: 0.875rem;
  transition: color var(--tranzicija);
}

.veza:hover {
  color: var(--boja-tekst);
}
</style>
