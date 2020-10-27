<template>
  <b-modal v-bind="$attrs" v-on="$listeners" scrollable ok-only centered>
    <template v-slot:modal-header> <slot name="dialog-header" /> </template>

    <slot />

    <template v-slot:modal-footer="{ ok, cancel }">
      <!-- slotProps example -->
      <slot name="dialog-controls" :modal="{ ok, cancel }">
        <b-button variant="outline-primary" @click="cancel()"> Close </b-button>
      </slot>
    </template>
  </b-modal>
</template>

<script>
export default {
  inheritAttrs: false,
};
</script>
