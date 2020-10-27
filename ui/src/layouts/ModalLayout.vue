<!-- The Forms pop-up in a modal window. -->
<template>
  <div>
    <p style="text-align: center;">
      <b-badge pill variant="info">Modal layout</b-badge>
    </p>
    <TheModal
      id="global-modal"
      :visible="showDefault"
      :key="$route.fullPath"
      size="lg"
      @hidden="onModalClose"
    >
      <slot />
      <template slot="dialog-controls">
        <div class="w-100">
          <portal-target name="controls" />
        </div>
      </template>
    </TheModal>

    <main>
      <keep-alive>
        <!-- The main content is not remounted when route changes. -->
        <router-view name="page" />
      </keep-alive>
    </main>
  </div>
</template>

<script>
import TheModal from '@/components/TheModal.vue';

export default {
  data() {
    return {
      routeFullPath: '',
    };
  },
  watch: {
    // eslint-disable-next-line no-unused-vars
    $route(to, from) {
      // console.log('modal watch', 'to:', to, 'from:', from);
      /* The modal visibility is controlled by a router. */
      const { components } = to.matched[0];
      const showDialog = 'default' in components || false;
      // fix: show on hystory back, but not show when manually closed
      // const notShowAgain = to.query.cancelled && !to.meta.popStateDetected;
      if (showDialog) {
        // } && !notShowAgain) {
        this.routeFullPath = to.fullPath;
        this.popModal();
        // this.$forceUpdate();  // ??? what for was this added
      } else {
        this.hideModal();
      }
    },
  },
  computed: {
    showDefault() {
      // Check if component in default router-view is present
      if (this.$route.matched[0] === undefined) return false;
      const { components } = this.$route.matched[0];
      return 'default' in components || false;
    },
  },
  methods: {
    popModal() {
      this.$bvModal.show('global-modal');
    },
    hideModal() {
      this.$bvModal.hide('global-modal');
    },
    onModalClose() {
      // eslint-disable-next-line no-unused-vars
      const { path, params, query, hash, fullPath } = this.$route;

      if (this.routeFullPath === fullPath) {
        this.$router.push('../');
        // same page (not click a link in a modal)
        // this.$router
        //   .replace({
        //     path,
        //     params,
        //     query: { ...query, cancelled: true },
        //     hash,
        //   }) /* when modal closed, need to change uri
        //   to be able to click the same router-link again,
        //   so set ?cancelled=true
        //   */
        //   .catch(
        //     () => {}
        //   ); /* fix: "err: Avoided redundant navigation to current location:""
        //   when closed again after history.back() */
      }
    },
  },
  mounted() {
    console.log('Modal layout mounted');
  },
  components: {
    TheModal,
  },
};
</script>
