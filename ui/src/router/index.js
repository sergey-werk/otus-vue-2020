import Vue from 'vue';
import VueRouter from 'vue-router';

import Error404 from '@/views/Error404Page.vue';

// before vue-router is registered with Vue.use(VueRouter)
window.popStateDetected = false;
window.addEventListener('popstate', () => {
  window.popStateDetected = true;
});

Vue.use(VueRouter);

const BooksPage = () => import(/* webpackChunkName: "books" */ '@/views/BooksPage');
const BookInfo = () => import(/* webpackChunkName: "books" */ '@/views/BookInfo');
const BookForm = () => import(/* webpackChunkName: "books" */ '@/views/BookForm');

function castRouteParams(route) {
  return Object.assign(route.params, {
    id: Number(route.params.id),
  });
}

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: { name: 'BooksPage' },
  },
  {
    path: '/books',
    name: 'BooksPage',
    components: {
      page: BooksPage,
    },
  },
  {
    path: '/books/add',
    name: 'BookAdd',
    props: {
      default: route => ({ ...castRouteParams(route), action: 'add' }),
    },
    components: {
      default: BookForm,
      page: BooksPage,
    },
  },
  {
    path: '/books/:id',
    name: 'BookInfo',
    props: {
      default: castRouteParams,
    },
    components: {
      default: BookInfo,
      page: BooksPage,
    },
  },
  {
    path: '/books/:id/edit',
    name: 'BookEdit',
    props: {
      default: route => ({ ...castRouteParams(route), action: 'edit' }),
    },
    components: {
      default: BookForm,
      page: BooksPage,
    },
  },
  {
    /* A short direct link for QR-codes.
       No background page, just a modal pup-up.
    */
    path: '/book-:id',
    name: 'BookDirect',
    props: {
      default: castRouteParams,
    },
    components: {
      default: BookInfo,
      page: BooksPage,
    },
  },
  {
    path: '/about',
    name: 'AboutPage',
    components: {
      page: () => import(/* webpackChunkName: "about" */ '../views/AboutPage.vue'),
    },
  },
  {
    path: '*',
    component: Error404,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.afterEach(to => {
  const isPopState = window.popStateDetected;
  window.popStateDetected = false;

  /* Check if navigation caused by history event (broswer Back/Forward or router.push/go)
     Just to debug awkward routing behaviour.
  */
  // eslint-disable-next-line no-param-reassign
  to.meta.popStateDetected = isPopState || false;

  if (!to.query.cancelled) {
    // fix: keep original dialog title in history if cancelled.
    document.title = to.name || 'bookstore';
  }
});

export default router;
