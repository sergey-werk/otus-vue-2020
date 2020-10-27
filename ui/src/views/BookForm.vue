<template>
  <div>
    <portal to="controls">
      <div class="w-100 d-flex">
        <div class="mr-auto p-1">
          <b-button type="reset" variant="danger" @click="onReset"
            ><b-icon icon="x" />Reset
          </b-button>
        </div>
        <div class="p-1">
          <b-button variant="primary" @click.prevent="onSubmit">
            <b-icon icon="check-circle" />Save
          </b-button>
        </div>
        <div class="p-1">
          <b-button @click="$router.push({ name: 'BookInfo', props: { id } })">
            Cancel
          </b-button>
        </div>
      </div>
    </portal>

    <b-form @submit="onSubmit" v-if="scratch">
      <b-form-group
        id=""
        :label="field.title + ':'"
        :label-for="field.name"
        description=""
        v-for="(field, idx) in show_fields"
        :key="idx"
      >
        <b-form-textarea
          v-if="field.type == 'textarea'"
          :id="field.name"
          v-model="scratch[field.name]"
          :type="field.type || 'text'"
          placeholder=""
          rows="3"
          max-rows="5"
        ></b-form-textarea>
        <b-form-input
          v-else
          :id="field.name"
          v-model="scratch[field.name]"
          :type="field.type || 'text'"
          placeholder=""
        ></b-form-input>
      </b-form-group>
    </b-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

function objdiff(o1, o2) {
  return Object.keys(o1).reduce((diff, key) => {
    if (o1[key] === o2[key]) return diff;
    return {
      ...diff,
      [key]: o2[key],
    };
  }, {});
}

export default {
  name: 'BookForm',
  props: {
    id: Number,
    value: Object, // Pass an object directly (for testing).
    action: {
      validator: value => ['edit', 'add'].indexOf(value) !== -1,
      required: true,
    },
  },
  data() {
    return {
      show_fields: [
        { name: 'title', title: 'Title' },
        { name: 'price', title: 'Price' },
        { name: 'subtitle', title: 'Subtitle', type: 'textarea' },
        { name: 'desc', title: 'Description', type: 'textarea' },
        { name: 'rating', title: 'Rating', type: 'number' },
        //       { name: 'language', title: 'Language' },
        //       { name: 'isbn10', title: 'ISBN-10' },
        //       { name: 'isbn13', title: 'ISBN-13' },
        { name: 'pages', title: 'Pages', type: 'number' },
      ],
      book: null,
      scratch: null,
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

      this.book = book;
      this.scratch = { ...book };
    },
    onSubmit(evt) {
      evt.preventDefault();
      const { scratch, book } = this;

      const { id } = this;
      const diff = objdiff(book, scratch);
      console.log('SUBMIT', diff);
      this.$store
        .dispatch('books/update', { id, data: diff })
        .catch(err => {
          console.warn('ERR', id, err);
        })
        .then(() => {
          this.$router
            .push('/books/')
            .catch(
              () => {}
            ); /* fix: "err: Avoided redundant navigation to current location:""
                            when closed again after history.back() */
        });
    },
    onReset() {
      this.scratch = { ...this.book };
    },
  },
  async mounted() {
    if (this.action === 'edit') {
      await this.initBook();
      document.title = `Edit: ${this.scratch.title}`;
    } else if (this.action === 'add') {
      document.title = 'Add Book';
    }
  },
};
</script>
