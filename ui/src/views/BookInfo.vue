<template>
  <section class="book-info" v-if="book" :key="id">
    <portal to="controls">
      <div class="w-100 d-flex">
        <div class="ml-auto w-auto">
          <CrudButtons class="crud-buttons" :id="book.id" />
        </div>
      </div>
    </portal>
    <header>
      <h1>{{ book.title }}</h1>
      <p class="book-authors">by {{ book.authors }}</p>
    </header>
    <p class="book-subtitle">
      {{ book.subtitle }}
    </p>
    <div class="d-flex flex-sm-row flex-column">
      <div class="book-cover flex-shrink-1">
        <img :src="book.image | base_url" alt="Book cover" />
      </div>
      <div class="mr-auto mt-auto mb-auto flex-column">
        <p v-for="(field, key) in show_fields" :key="key" :class="`book-field book-${key}`">
          <label v-if="field" :for="(field_id = `book-${book.id}-${key}`)"
            >{{ field }}:&nbsp;</label
          >
          <span class="book-field-value" :id="field_id">
            {{ book[key] }}
          </span>
        </p>
      </div>
    </div>
    <div>
      <p class="book-desc">
        {{ book.desc }}
      </p>
    </div>
  </section>
  <section v-else-if="booksLoading">
    <b-spinner label="Loading..." />
  </section>
  <section v-else-if="!book">
    Book not found. :'-(
  </section>
</template>

<script>
import CrudButtons from '@/components/CrudButtons.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'BookInfo', // to prevent 'Anonymous component' in devtools.
  props: {
    id: Number,
    value: Object, // Pass an object directly (for testing).
  },
  components: {
    CrudButtons,
  },
  data() {
    return {
      book: null,
      show_fields: {
        price: 'Price',
        publisher: 'Published by',
        year: 'Year',
        language: 'Language',
        isbn10: 'ISBN-10',
        isbn13: 'ISBN-13',
        pages: 'Pages',
        // rating: 'Rating',
      },
    };
  },
  computed: {
    ...mapGetters('books', {
      booksLoading: 'isLoading',
      getBookById: 'byId',
    }),
  },
  methods: {
    initBook() {
      const { id: propId, value: propValue } = this; // Props
      let id;
      let book = propValue; // 1: passed directly via Props

      if (!book) {
        id = propId || this.$route.params.id;
        book = this.getBookById(id); // 2: get from store
      }

      this.book = book || null;
    },
  },
  async mounted() {
    await this.initBook();
    document.title = this.book.title;
    console.log('title set to ', this.book.title);
  },
};
</script>
