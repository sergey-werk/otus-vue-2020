import Crud from '@/store/classes/crud';

/* Book item:
    {
      id: 0,
      title: 'Getting to Know Vue.js',
      subtitle: 'Learn to Build Single Page Applications in Vue from Scratch',
      authors: 'Brett Nelson',
      publisher: 'Apress',
      language: 'English',
      isbn10: '1484237803',
      isbn13: '9781484237809',
      pages: '265',
      year: '2018',
      rating: '2',
      desc: 'Learn how to render lists of items without repeating your code structure ...',
      price: '$27.96',
      image: '/bookcovers/9781484237809.png',
      url: 'https://itbook.store/books/9781484237809',
    },
  */

const crud = new Crud(`${process.env.VUE_APP_API_ENDPOINT}/state/books`);

const state = {
  ...crud.state,
};
const getters = {
  ...crud.getters,
};
const actions = {
  ...crud.actions,
};
const mutations = {
  ...crud.mutations,
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
