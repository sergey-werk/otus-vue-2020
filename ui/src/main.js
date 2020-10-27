import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import PortalVue from 'portal-vue';
import configureEventSource from '@/api/eventsource';
import App from './App.vue';
import router from './router';
import store from './store';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(PortalVue);

configureEventSource();

const env = ['VUE_APP_EVENTS_ENDPOINT', 'VUE_APP_API_ENDPOINT'];
env.forEach(v => {
  // eslint-disable-next-line no-console
  (process.env[v] ? console.info : console.warn)(`Environment variable ${v} is `, process.env[v]);
});

Vue.config.productionTip = false;

Vue.filter('base_url', value => {
  /** add BASE_URL before path.
   * Useful for files in 'public' directory.
   */
  let url = process.env.BASE_URL + value;
  url = url
    .split('/')
    .filter(x => x)
    .join('/'); // '//' -> '/'
  return `/${url}`;
});

/* A little hack */
// DELME:
Vue.mixin({
  computed: {
    console: () => console,
  },
});

// FIXME: a better way?
const delay = 3000;
let prevTimestamp = 0;

function checkAlive() {
  const { online, timestamp } = store.state;
  if (online && prevTimestamp === timestamp) {
    store.commit('SET_OFFLINE');
  } else if (!online && prevTimestamp !== timestamp) {
    store.commit('SET_ONLINE');
  }
  prevTimestamp = timestamp;
}

new Vue({
  router,
  store,
  render(h) {
    return h(App);
  },
}).$mount('#app');

setInterval(checkAlive, delay);
