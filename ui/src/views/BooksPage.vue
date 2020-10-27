<template>
  <div>
    <h1>Books</h1>
    <div class="books-catalog-controls d-flex flex-row flex-wrap mb-3">
      <!-- <div class="m-2">
        <b-button variant="success" @click="$router.push({ name: 'BookAdd' })">
          <b-icon icon="plus-circle" /> Add
        </b-button>
      </div> -->
      <div class="m-2 py-2">
        <b-form-checkbox name="check-button" switch v-model="isListView">
          List view
        </b-form-checkbox>
      </div>
    </div>
    <!-- Filters -->
    <div class="py-4 d-flex flex-row flex-wrap">
      <div>
        <b-input-group>
          <b-form-input
            type="search"
            placeholder="Filter by title:"
            style="max-width: 10em;"
            v-model="filterTitleData"
          />
          <b-input-group-append>
            <b-button :disabled="!filterTitleData" @click="filterTitleData = ''">Clear</b-button>
          </b-input-group-append>
        </b-input-group>
      </div>
      <div class="d-block pb-4 mx-4" style="min-width: 10em;">
        <RangeSlider
          v-model="filterYearData"
          :data="booksYears"
          :marks="booksYears.length < 5 ? booksYears : []"
        >
          by year:&nbsp;
        </RangeSlider>
      </div>
      <div class="d-block pb-4 mx-4" :style="`min-width: ${booksPricesRounded.length}em;`">
        <!-- one more option to set props -->
        <RangeSlider v-model="filterPriceData" :data="booksPricesRounded">
          by price:&nbsp;
        </RangeSlider>
      </div>
    </div>
    <!-- / Filters -->
    <!-- Content -->
    <div class="d-flex justify-content-center mb-3" v-if="isBooksLoading">
      <b-spinner label="Loading..."></b-spinner>
    </div>

    <section v-show="filteredItems.length">
      <!-- Card view -->
      <div class="row" v-if="!isListView">
        <div
          class="book-card col-xs-12 col-sm-6 col-md-4 d-flex"
          v-for="book in filteredItems"
          :key="book.id"
        >
          <BooksCard class="w-100 mb-4" :item="book" />
        </div>
      </div>
      <!-- Here we use our own CrudTable component. -->
      <div v-else-if="isListView">
        <CrudTable key_field="id" :rows="filteredItems" :columns="listColumns" />
      </div>
    </section>
    <p v-show="this.items.length && !filteredItems.length">No match found.</p>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import CrudTable from '@/components/CrudTable.vue';
import RangeSlider from '@/components/RangeSlider.vue';
import BooksCard from './BooksCard.vue';

// eslint-disable-next-line no-extend-native, func-names
Number.prototype.between = function(a, b) {
  /** Because why not =) */
  const min = Math.min.apply(Math, [a, b]);
  const max = Math.max.apply(Math, [a, b]);
  return this >= min && this <= max;
};

function forceNumber(val) {
  /** Strip non-numeric characters and convert to number. */
  if (val === undefined || val === null || Number.isNaN(val)) {
    return val;
  }
  return Number(String(val).replace(/[^0-9.-]+/g, ''));
}

export default {
  name: 'Books',
  data() {
    return {
      isListView: false, // TODO: move to state?, make it an url parameter?
      listColumns: {
        title: 'Title',
        year: 'Published in (year)',
        price: 'Price',
      },
      filterTitleData: '',
      filterYearData: [null, null],
      filterPriceData: [null, null],
    };
  },
  components: {
    RangeSlider,
    BooksCard,
    CrudTable,
  },
  computed: {
    ...mapGetters('books', {
      isBooksLoading: 'isLoading',
      getBookById: 'byId',
      booksAttrUnique: 'attrUnique',
    }),
    ...mapState('books', ['items', 'selectedItems']),
    filteredItems() {
      return this.items
        .filter(item => item.title.toLowerCase().includes(this.filterTitle))
        .filter(
          item =>
            Number(item.year).between(...this.filterYear) ||
            // accept undefined if filter not set
            (this.filterYear[0] === null && this.filterYear[1] === null)
        )
        .filter(
          item =>
            Math.floor(forceNumber(item.price)).between(...this.filterPrice) ||
            (this.filterPrice[0] === null && this.filterPrice[1] === null)
        );
    },
    filterTitle() {
      return this.filterTitleData.trim().toLowerCase();
    },
    filterYear() {
      const yr = this.filterYearData;
      return [yr[0] || null, yr[1] || null];
    },
    filterPrice() {
      const pr = this.filterPriceData;
      // pr[1] + 1 -- because prices are rounded down
      return [pr[0] || null, pr[1] ? pr[1] + 1 : null];
    },
    booksYears() {
      /** Unique years of all the books. */
      return this.booksAttrUnique('year', Number).sort((a, b) => a - b);
    },
    booksPricesRounded() {
      /** Unique prices of all the books,
         sorted and rounded down! (49.99 -> 49.)
      */
      return this.booksAttrUnique('price', x => Math.floor(forceNumber(x))).sort((a, b) => a - b);
    },
  },
  mounted() {
    if (!this.items.length) {
      // this.$store.dispatch('books/fetch');
    }
  },
};
</script>

<style scoped>
@media (min-width: 1100px) {
  .book-card {
    flex: 0 0 350px !important;
  }
}
.b-icon {
  margin-right: 0.3em;
}
</style>
