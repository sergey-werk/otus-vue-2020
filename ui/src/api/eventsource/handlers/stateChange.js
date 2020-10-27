/* eslint-disable no-unused-vars */
import store from '@/store';

// # pub messages:
// # id: <ts>
// # event: change
// # data: { module: 'books',
// #         version: <version>,
// #         uid: <uid>,
// #         action: 'set' | 'delete' | 'update' | 'add'
// #         payload: <payload> }
// #
// # =Action= = Payload =
// # Set      { items: [ <item>, ...] }
// # Update   { <id>: {<key>: <value>, ...} }
// # Delete   [ <id>, ...]
// # Add      <item>

const stateChange = {
  eventType: 'change',
  handle(event) {
    const parsed = JSON.parse(event.data);
    const { module, action, version, uid, payload } = parsed;

    switch (action) {
      // Fixme: module
      case 'update':
        // eslint-disable-next-line no-restricted-syntax
        for (const [id, obj] of Object.entries(payload)) {
          store.commit('books/ITEM_UPDATE', { id, obj });
        }
        break;
      case 'delete':
        store.commit('books/ITEMS_DELETE', ...payload);
        break;
      default:
        console.error(`Unknown stateChange action '${action}'`);
    }
  },
};

export default stateChange;
