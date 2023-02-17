import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Index',
      component: () => import('../components/homepageHeader.vue'),
      children: [
        {
          path: '/',
          name: 'Homepage',
          component: () => import('../components/Homepage/homepage.vue'),
        },
        {
          path: '/BI',
          name: 'BIanalysis',
          component: () => import('../components/BI/bianalysis.vue')
        }

      ]
    }
  ],
})

export default router
