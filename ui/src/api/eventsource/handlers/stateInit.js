import store from '@/store';

const stateInit = {
  eventType: 'init',
  handle(event) {
    const parsed = JSON.parse(event.data);
    store.commit('STATE_SET', parsed);
  },
};

export default stateInit;
