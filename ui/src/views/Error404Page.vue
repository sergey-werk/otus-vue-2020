<template>
  <div class="about">
    <h1>Page not found. ¯\_(ツ)_/¯</h1>
    <p>
      Nothing with address <em>"{{ this.$route.params.pathMatch }}"</em> was found.
    </p>
    <p>
      Navigate <a href="javascript:history.back()">back</a> or to
      <router-link :to="{ name: 'Home' }" exact>Home</router-link>.
    </p>
  </div>
</template>

<script>
export default {};
</script>
