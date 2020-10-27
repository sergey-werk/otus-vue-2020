/*

*/
import Handlers from './handlers';

export default function configureEventSources() {
  const eventSource = new EventSource(process.env.VUE_APP_EVENTS_ENDPOINT);
  Handlers.forEach(handler => {
    eventSource.addEventListener(handler.eventType, event => {
      handler.handle(event);
    });
  });
}
