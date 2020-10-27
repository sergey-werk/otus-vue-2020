<template>
  <b-navbar id="topnav" toggleable="sm" variant="faded" type="light">
    <b-navbar-brand tag="h1" class="mb-0">
      <span style="color:brown">Vue</span>Bookstore</b-navbar-brand
    >
    <b-navbar-toggle target="nav-text-collapse"></b-navbar-toggle>
    <b-collapse id="nav-text-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item :to="{ name: 'BooksPage' }">Books</b-nav-item>
        <b-nav-item :to="{ name: 'AboutPage' }">About</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
    <slot />
  </b-navbar>
</template>

<script>
export default {
  //
};
</script>
