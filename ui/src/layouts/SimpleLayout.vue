<template>
  <div>
    <p style="text-align: center;">
      <b-badge pill variant="info">Simple layout</b-badge>
    </p>
    <main>
      <nav>
        <portal-target name="controls" />
      </nav>
      <router-view :key="$route.fullPath" />
      <transition>
        <keep-alive>
          <router-view name="page" v-if="!showDefault" />
        </keep-alive>
      </transition>
    </main>
  </div>
</template>

<script>
export default {
  computed: {
    showDefault() {
      // Check if component in default router-view is present
      if (this.$route.matched[0] === undefined) return false;
      const { components } = this.$route.matched[0];
      return 'default' in components || false;
    },
  },
};
</script>
