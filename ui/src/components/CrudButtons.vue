<template>
  <div>
    <router-link
      class="btn btn-warning"
      :class="{ 'btn-sm': compact }"
      :to="{ name: 'BookEdit', params: { id } }"
    >
      <b-icon icon="pencil" />
      Edit
    </router-link>
    &nbsp;
    <b-button variant="danger" :class="{ 'btn-sm': compact }" @click.prevent="onDelete">
      <b-spinner small type="grow" v-show="loading" :disabled="!loading" />
      Delete
    </b-button>
  </div>
</template>

<script>
export default {
  props: {
    module: {
      type: String,
      // required: true
    },
    id: {
      type: [Number, Array],
      required: true,
    },
    deleteConfirmation: {
      type: [String, Function],
      // eslint-disable-next-line object-shorthand
      default: function(n) {
        return n > 1 ? `Delete ${n} items?` : 'Delete the item?';
      },
    },
    routeSuccess: {
      type: [String, Object],
    },
    compact: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      loading: null,
    };
  },
  methods: {
    onDelete() {
      const { id: ids, deleteConfirmation: message } = this;
      const number = Array.isArray(ids) ? ids.length : 1;
      const text = typeof message === 'function' ? message(number, ids) : message;
      this.loading = true;

      this.$bvModal
        .msgBoxConfirm(text, {
          title: 'Please Confirm',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'danger',
          okTitle: 'Yes',
          cancelTitle: 'No',
          footerClass: 'p-2',
          hideHeaderClose: false,
          centered: true,
        })
        .then(value => {
          if (value) {
            // Yes
            this.$store
              .dispatch('books/delete', ids)
              .catch(err => {
                console.log('ERR', ids, err);
              })
              .then(() => {
                this.$router
                  .push('/books/')
                  .catch(
                    () => {}
                  ); /* fix: "err: Avoided redundant navigation to current location:""
                            when closed again after history.back() */
              });
          } else {
            // No
            this.loading = false;
          }
          //
        });
    },
  },
};
</script>

<style scoped></style>
