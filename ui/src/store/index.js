import Vue from 'vue';
import Vuex from 'vuex';
// import createPersistedState from 'vuex-persistedstate';

import books from './modules/books';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    layout: '', // Page layout
    timstamp: 0,
    online: true,
  },
  getters: {
    isOnline: ({ online }) => online,
  },
  mutations: {
    SET_LAYOUT(state, payload) {
      state.layout = payload;
    },
    STATE_SET(state, payload) {
      this.commit('SET_ONLINE');
      Object.assign(state, payload);
    },
    SET_ONLINE(state) {
      state.online = true;
    },
    SET_OFFLINE(state) {
      state.online = false;
    },
  },
  modules: {
    books,
  },
  //  plugins: [createPersistedState()],
});
