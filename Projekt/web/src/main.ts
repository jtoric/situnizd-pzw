import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/globalno.css'
import { useObavijestiStore } from './stores/obavijesti'
import { useAuthStore } from './stores/auth'

const pinia = createPinia()
const aplikacija = createApp(App)
aplikacija.use(pinia)

// Boot: dohvati korisnika PRIJE instalacije routera da guard vidi ispravno stanje
if (localStorage.getItem('access_token')) {
  try {
    await useAuthStore(pinia).dohvatiMene()
  } catch {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
}

aplikacija.use(router)

aplikacija.config.errorHandler = (err) => {
  const poruka = err instanceof Error ? err.message : 'Neočekivana greška.'
  useObavijestiStore(pinia).greska(poruka)
}

aplikacija.mount('#app')
