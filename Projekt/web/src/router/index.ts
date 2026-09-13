import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PrijavaView from '@/views/PrijavaView.vue'
import NepoznatoView from '@/views/NepoznatoView.vue'
import AdminPocetnaView from '@/views/admin/AdminPocetnaView.vue'
import AdminKluboviView from '@/views/admin/AdminKluboviView.vue'
import AdminNatjecanjaView from '@/views/admin/AdminNatjecanjaView.vue'
import NatjecanjaFormaView from '@/views/admin/NatjecanjaFormaView.vue'
import AdminPrijaveView from '@/views/admin/AdminPrijaveView.vue'
import KlubPocetnaView from '@/views/klub/KlubPocetnaView.vue'
import KlubNatjecateljiView from '@/views/klub/KlubNatjecateljiView.vue'
import NatjecateljFormaView from '@/views/klub/NatjecateljFormaView.vue'
import KlubPrijaveView from '@/views/klub/KlubPrijaveView.vue'
import NatjecanjaView from '@/views/klub/NatjecanjaView.vue'
import PrijavaFormaView from '@/views/klub/PrijavaFormaView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: () => {
        const auth = useAuthStore()
        if (!auth.isAuthenticated) return '/prijava'
        return auth.isAdmin ? '/admin/pocetna' : '/klub/pocetna'
      },
    },
    {
      path: '/prijava',
      component: PrijavaView,
      meta: { layout: 'gost', javno: true },
    },
    {
      path: '/admin',
      meta: { layout: 'aplikacija', uloga: 'admin' },
      children: [
        { path: 'pocetna', component: AdminPocetnaView },
        { path: 'klubovi', component: AdminKluboviView },
        { path: 'natjecanja', component: AdminNatjecanjaView },
        { path: 'natjecanja/novo', component: NatjecanjaFormaView },
        { path: 'natjecanja/:id/uredi', component: NatjecanjaFormaView },
        { path: 'natjecanja/:compId/prijave', component: AdminPrijaveView },
      ],
    },
    {
      path: '/klub',
      meta: { layout: 'aplikacija', uloga: 'klub' },
      children: [
        { path: 'pocetna', component: KlubPocetnaView },
        { path: 'natjecatelji', component: KlubNatjecateljiView },
        { path: 'natjecatelji/novi', component: NatjecateljFormaView },
        { path: 'natjecatelji/:id/uredi', component: NatjecateljFormaView },
        { path: 'natjecanja', component: NatjecanjaView },
        { path: 'natjecanja/:compId/prijava', component: PrijavaFormaView },
        { path: 'prijave', component: KlubPrijaveView },
      ],
    },
    {
      path: '/:catchAll(.*)*',
      component: NepoznatoView,
      meta: { layout: 'gost', javno: true },
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  // Prijavljeni korisnik na javnoj stranici → preusmjeri na svoju početnu
  if (to.meta.javno) {
    if (auth.isAuthenticated) return auth.isAdmin ? '/admin/pocetna' : '/klub/pocetna'
    return true
  }

  if (!auth.isAuthenticated) return '/prijava'

  // Provjera uloge za zaštićene sekcije
  if (to.meta.uloga === 'admin' && !auth.isAdmin) return '/klub/pocetna'
  if (to.meta.uloga === 'klub' && !auth.isClub) return '/admin/pocetna'

  return true
})

export default router
