<!-- Try to implement our own Table component
... to never do this again in a life.

Inspired by vue-good-table.
-->
<template>
  <table class="table" :class="{ 'table-sm': compact }">
    <template>
      <thead>
        <th scope="col" @click="toggleSelectAll">
          <input type="checkbox" :checked="isAllSelected" />
        </th>
        <th v-for="(title, field) in columns" :key="field">
          {{ title }}
        </th>
        <th></th>
      </thead>
    </template>
    <template>
      <tbody>
        <tr
          v-for="row in sortedRows"
          :key="row[key_field]"
          @click="onCheckboxChanged(row, 'row', $event)"
          :class="{ selected: row.selected }"
        >
          <!-- Illustration of event modifiers chainging.
        NB: order is important!, .self.stop would not work. -->
          <th scope="row" @click.stop.self="onCheckboxChanged(row, 'th', $event)">
            <input
              type="checkbox"
              :checked="row.selected"
              @change="onCheckboxChanged(row, 'checkbox', $event)"
            />
          </th>
          <td v-for="(title, field) in columns" :key="field">
            {{ row[field] }}
          </td>
          <td :key="'crud'">
            <CrudButtons class="crud-buttons" :id="row.id" compact />
          </td>
        </tr>
      </tbody>
    </template>
  </table>
</template>

<script>
import CrudButtons from './CrudButtons.vue';

export default {
  name: 'crud-table',
  props: {
    columns: {
      type: [Array, Object],
      default: () => ({ title: 'Title' }),
    },
    rows: {
      type: Array,
      required: true,
    },
    key_field: {
      type: String,
      required: true,
    },
    selectable: {
      type: Boolean,
      default: true,
    },
    sortable: {
      type: Boolean,
      default: true,
    },
    compact: Boolean,
  },
  watch: {
    originalRows: {
      handler(newValue, oldValue) {
        if (oldValue.lengh > newValue.length) {
          // TODO: a better solution is to implement filter method inside CrudTable.
          this.unselectAll();
        }
      },
    },
  },
  computed: {
    /* TODO: originalRows -> [filteredRows] -> sortedRows -> paginatedRows */
    sortedRows() {
      return this.originalRows; // TODO: sort by column
    },
    originalRows() {
      // FIXME: _.deepCopy? Or `{...this.rows}` to loose reactivity?
      return this.rows;
    },
    selectedRows() {
      const selectedRows = [];
      this.sortedRows.forEach(row => {
        if (row.selected) {
          selectedRows.push(row);
        }
      });
      // Sort to not to bother observers when user sorts table by fied.
      return selectedRows.sort((r1, r2) => r1[this.key_field] - r2[this.key_field]);
    },
    isAllSelected() {
      return this.originalRows.length && this.selectedRows.length === this.originalRows.length;
    },
  },
  methods: {
    // eslint-disable-next-line no-unused-vars
    onCheckboxChanged(row, where) {
      // console.log('called from', where);
      this.$set(row, 'selected', !row.selected);
    },
    selectAll() {
      this.sortedRows.forEach(row => {
        this.$set(row, 'selected', true);
      });
    },
    unselectAll() {
      this.sortedRows.forEach(row => {
        this.$set(row, 'selected', false);
      });
    },
    toggleSelectAll() {
      if (this.isAllSelected) {
        this.unselectAll();
        return;
      }
      this.selectAll();
    },
  },
  components: {
    CrudButtons,
  },
};
</script>

<style scoped>
.crud-buttons {
  visibility: hidden;
}
tr:hover .crud-buttons,
th:hover .crud-buttons {
  visibility: visible;
}
tr th {
  width: 1em;
}
tr:hover {
  background-color: lightgray;
}
tr.selected {
  background-color: lightgray;
}
</style>
