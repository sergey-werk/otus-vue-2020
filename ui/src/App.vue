<template>
  <div>
    <!-- Back and Forward buttons (to debug routing) -->
    <div id="toptools" class="d-flex">
      <b-button-group size="sm" class="my-2 ml-auto" style="z-index:1050">
        <b-button variant="outline-primary" @click="historyBack">
          <b-icon icon="arrow-left-circle" aria-hidden />&nbsp;Back
        </b-button>
        <b-button variant="outline-secondary" @click="historyForward">
          Forward&nbsp;<b-icon icon="arrow-right-circle" aria-hidden />
        </b-button>
      </b-button-group>
      <b-nav-form class="ml-auto" style="z-index:1050">
        <b-form-select
          size="sm"
          right
          ref="layoutSelect"
          :value="this.$store.state.layout"
          @change="v => this.$store.commit('SET_LAYOUT', v)"
          :options="layoutSelectOptions"
        />
      </b-nav-form>
    </div>
    <div class="app-layout" :class="{ offline: !isOnline }">
      <TheNavbar></TheNavbar>

      <span v-if="isOnline"> <b-badge pill variant="success">ONLINE</b-badge></span>
      <span v-else> <b-badge pill variant="danger">OFFLINE</b-badge></span>

      <component :is="layout">
        <router-view />
      </component>
    </div>
  </div>
</template>

<script>
import TheNavbar from '@/components/TheNavbar.vue';

// Register layouts here
import ModalLayout from '@/layouts/ModalLayout.vue';
import SimpleLayout from '@/layouts/SimpleLayout.vue';

export default {
  data() {
    return {
      layoutSelectOptions: [
        { value: '', text: 'Choose layout...', disabled: true },
        { value: 'modal-layout', text: 'Modal layout' },
        { value: 'simple-layout', text: 'Simple layout' },
      ],
    };
  },
  computed: {
    layout() {
      return this.$route.meta.layout || this.$store.state.layout || 'modal-layout';
    },
    isOnline() {
      return this.$store.getters.isOnline;
    },
  },
  components: {
    TheNavbar,
    SimpleLayout,
    ModalLayout,
  },
  methods: {
    historyBack() {
      // eslint-disable-next-line no-restricted-globals
      this.$router.go(-1);
    },
    historyForward() {
      // eslint-disable-next-line no-restricted-globals
      history.forward();
    },
  },
  mounted() {
    /* When page is navigated via history Back/Forward,
       vuex store is empty (if not cached in LocalStorage).
       But the values of an actual html form intpus are preserved by the browser.
       So, here we are using $refs to get the preserved value
       to initialize our layout state. Just for fun =)
    */
    try {
      /* this.$nextTick() not working in this case :(
       ... so making a little trick:
      */
      setTimeout(() => {
        const historicValue = this.$refs.layoutSelect.$refs.input.value;
        this.$store.commit('SET_LAYOUT', historicValue);
      }, 0);
    } catch (err) {
      console.log('TheNavbar', err);
    }
  },
};
</script>
