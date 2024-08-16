// Vuex 때 처럼 create* 함수를 제공한다.
import { createWebHashHistory, createRouter } from 'vue-router';

import NotFound from './views/NotFound';

// function publicPath () {
//   if (process.env.CI_PAGES_URL) {
//     return new URL(process.env.CI_PAGES_URL).pathname
//   } else {
//     return '/'
//   }
// }

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home'), // 동적 import
  },
  // {
  //   // For test
  //   path: '/login',
  //   name: 'Login',
  //   component: () => import('@/views/Login'),
  // },
  {
    path: '/first',
    name: 'First',
    component: () => import('@/components/SingleFile'),
  },
  {
    path: '/last',
    name: 'Last',
    component: () => import('@/components/LastEnd'),
  },
  {
    path: '/result',
    name: 'GMap',
    component: () => import('@/components/GMap'),
  },
  {
    path: "/404",
    name: "notFound",
    component: NotFound, // 정적 import
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/404",
  },
];

// 이렇게 해도 된다.
// const router = createRouter({
//   history: createWebHistory(),
//   routes,
// });
// export default router;

export const router = createRouter({
  history: createWebHashHistory("/capstone-design/02/vue-router/"),
  base: "/capstone-design/02/vue-router/",
  routes,
});