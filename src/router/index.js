import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'main',
    redirect: { name: 'home' },
    component: () => import('@/views/main/BaseView.vue'),
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
        path: 'about',
        name: 'about',
        component: () => import('@/views/main/AboutView.vue'),
        meta: {
          isWeb: true,
        },
      },
      {
        path: 'dopo',
        name: 'dopo',
        component: () => import('@/views/main/DopoView.vue'),
        meta: {
          isWeb: true,
        },
      },
    ],
  },
  {
    path: '/settings',
    name: 'user-settings',
    redirect: { name: 'user-settings-general' },
    component: () => import('@/views/main/BaseView.vue'),
    children: [
      {
        path: 'password',
        name: 'user-settings-general',
        component: () => import('@/views/main/settings/GeneralSettingsView.vue'),
      },
      {
        path: 'payment',
        name: 'user-settings-payment',
        component: () => import('@/views/main/settings/PaymentSettingsView.vue'),
        meta: {
          isWeb: true,
        },
      },
      {
        path: 'payment-old',
        name: 'user-settings-payment-old',
        component: () => import('@/views/main/settings/PaymentSettingsView.vue'),
      },
      {
        path: 'promocode',
        name: 'user-settings-promocode',
        component: () => import('@/views/main/settings/PromocodeSettingsView.vue'),
      },
    ],
  },
  {
    path: '/support',
    name: 'support',
    redirect: { name: 'support-list' },
    component: () => import('@/views/main/BaseView.vue'),
    children: [
      {
        path: 'list',
        name: 'support-list',
        component: () => import('@/views/main/support/SupportListView.vue'),
      },
      {
        path: 'create',
        name: 'support-create',
        component: () => import('@/views/main/support/SupportActionView.vue'),
      },
      {
        path: 'info/:id',
        name: 'support-info',
        component: () => import('@/views/main/support/SupportInfoView.vue'),
      },
    ],
  },
  {
    path: '/loader',
    name: 'loader',
    component: () => import('@/views/main/LoaderView.vue'),
    meta: {
      layout: 'loader',
    },
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
];

const router = createRouter({
  // history: createWebHistory(process.env.BASE_URL),
  history: createWebHashHistory(),
  routes,
});

export default router;
