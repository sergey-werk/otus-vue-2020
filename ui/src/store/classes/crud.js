/* eslint-disable no-unused-vars */
/* eslint-disable implicit-arrow-linebreak */
/**
 * Class for some CRUD-compatible items list.
 * (Create, Read, Update, Delete)
 *
 * Each list items must have unique 'id' property.
 */
import client from '@/api/client';
import Vue from 'vue';

export default class {
  constructor(url) {
    this.state = {
      url, // API endpoint
      isLoading: false,
      items: [],
    };

    this.getters = {
      byId: ({ items }) => id => {
        const nId = Number(id);
        return items.find(o => Number(o.id) === nId);
      },
      attrUnique: ({ items }) => (attr, format = String) =>
        // for the items get all possible variants of specified attribute,
        // unsorted!
        Array.from(new Set(items.map(o => o[attr]).map(format))),
      isLoading: state => !!state.isLoading,
    };

    this.actions = {
      async add({ commit }, payload) {
        // FIXME: Not implemented.
      },

      async delete(context, _id) {
        client.deleteItem(url, _id).then(x => console.log(x));
      },

      async update(context, { id, data }) {
        client.updateItem(url, id, data).then(x => console.log(x));
      },
    };

    this.mutations = {
      LOADING_SET(state, v) {
        state.isLoading = v;
      },
      ITEMS_SET(state, arr) {
        state.items = [...arr];
      },
      ITEM_UPDATE(state, { id, obj }) {
        // eslint-disable-next-line eqeqeq
        // const itemIndex = state.items.findIndex(x => x.id == id);
        const nId = Number(id);
        const item = state.items.find(o => Number(o.id) === nId);
        if (item) {
          // eslint-disable-next-line no-restricted-syntax
          for (const [key, val] of Object.entries(obj)) {
            Vue.set(item, key, val);
          }
        }
      },
      ITEMS_ADD(state, ...arr) {
        state.items.push(...arr);
      }, // FIXME: check
      // TODO: update.
      ITEMS_DELETE(state, ...arr) {
        const strArr = arr.map(String);
        state.items = state.items.filter(({ id }) => !strArr.includes(String(id)));
      },
    };
  }
}
