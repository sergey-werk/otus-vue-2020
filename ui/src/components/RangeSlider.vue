<!-- A wrapper for the vue-slider-component -->
<template>
  <div v-if="data.length">
    <span>
      <slot />
      <strong>
        {{ low === null ? '' : low }}
        <span v-show="high && low != high"> – {{ high }}</span>
        &nbsp;
        <b-icon
          icon="x-circle"
          style="cursor: pointer;"
          aria-hidden
          v-show="low != null || high != null"
          @click="inputValue = [null, null]"
        />
      </strong>
    </span>
    <vue-slider
      v-bind="$attrs"
      v-on="$listeners"
      :value="valueFiltered"
      @change="v => (inputValue = v)"
      :data="dataFiltered"
      :marks="marksFiltered"
      :enable-cross="false"
      lazy
      adsorb
      :tooltipPlacement="['left', 'right']"
    />
  </div>
</template>

<script>
import VueSlider from 'vue-slider-component';
import 'vue-slider-component/theme/default.css';

export default {
  inheritAttrs: false, // Important!
  props: {
    value: {
      type: [Array],
      required: true,
    },
    data: {
      type: Array,
      required: true,
    },
    marks: {
      type: Array,
    },
  },
  computed: {
    inputValue: {
      get() {
        const [low, high] = this.value;
        return [low, high];
      },
      set(val) {
        this.$emit('input', val);
      },
    },
    low() {
      return this.inputValue[0];
    },
    high() {
      return this.inputValue[1];
    },
    dataFirstLast() {
      const { dataFiltered: data } = this;
      return [data[0], data[data.length - 1]];
    },
    dataFiltered() {
      return this.data.filter(v => !Number.isNaN(v));
    },
    marksFiltered() {
      const { dataFiltered: data } = this;
      if (this.marks) {
        // bugfix: VueSlider 'feature': marks misalign if not in data
        return this.marks.filter(_ => data.includes(_));
      }
      // if no marks given, show first and last elements
      return this.dataFirstLast;
    },
    valueFiltered() {
      const [vmin, vmax] = this.value;
      const [dmin, dmax] = this.dataFirstLast;
      return [vmin || dmin, vmax || dmax];
    },
  },
  components: {
    VueSlider,
  },
};
</script>
