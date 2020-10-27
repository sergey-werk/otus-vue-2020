<template>
  <b-card class="books-card" :class="{ selected: item.selected }">
    <div style="position:relative">
      <!-- an outer box for the stretched-link -->
      <b-img
        fluid
        center
        class="books-card-img"
        alt="Book cover"
        :src="item.image || '/bookcovers/placeholder.png' | base_url"
      />
      <b-card-title>
        <router-link class="stretched-link" :to="{ name: 'BookInfo', params: { id: item.id } }">
          {{ item.title }}
        </router-link>
      </b-card-title>
      <b-card-sub-title>
        {{ item.subtitle }}
      </b-card-sub-title>
      <b-card-text />
    </div>

    <template v-slot:header>
      <div class="d-flex" @click.self.prevent="onHeaderClicked(item)">
        <b-form-rating
          class="books-card-rating"
          inline
          disabled
          no-border
          :value="item.rating"
          v-if="item.rating > 0"
        />
        <b-form-checkbox class="ml-auto p-2" v-model="item.selected" />
      </div>
    </template>
    <template v-slot:footer>
      <div class="d-flex">
        <div>
          <small class="text-muted">ISBN-13: {{ item.isbn13 }}</small> <br />
          <small class="text-muted">ISBN-10: {{ item.isbn10 }}</small>
        </div>
        <div class="ml-auto align-self-center">{{ item.price }}</div>
      </div>
    </template>
  </b-card>
</template>

<script>
export default {
  name: 'BookCard',
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  methods: {
    onHeaderClicked(item) {
      this.$set(item, 'selected', !item.selected);
    },
  },
};
</script>
