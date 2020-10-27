import store from '@/store';

const pingEvent = {
  eventType: 'ping',
  handle(event) {
    store.state.timestamp = event.timeStamp; // Access directly
  },
};

export default pingEvent;
