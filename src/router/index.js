import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'main',
    component: () => import('@/views/main/BaseView.vue'),
    redirect: { name: 'home' },
    children: [
      {
        path: 'home',
        name: 'home',
        component: () => import('@/views/main/HomeView.vue'),
        meta: {
          isWeb: true,
        },
      },
      {
        path: 'database',
        name: 'database',
        component: () => import('@/views/main/DatabaseView.vue'),
        meta: {
          isWeb: true,
        },
      },
      {
        path: 'forum',
        name: 'forum',
        component: () => import('@/views/main/ForumView.vue'),
        meta: {
          isWeb: true,
        },
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: {
      layout: 'auth',
    },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/auth/RegisterView.vue'),
    meta: {
      layout: 'auth',
    },
  },
  {
    path: '/forgot',
    name: 'forgot',
    component: () => import('@/views/auth/ForgotView.vue'),
    meta: {
      layout: 'auth',
    },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: { name: 'home' },
  },
];

const router = createRouter({
  // history: createWebHistory(process.env.BASE_URL),
  history: createWebHashHistory(),
  routes,
});

export default router;
