<template >
  <HeaderNav />
  <router-view />
  <FooterNav />
</template>

<script>
import HeaderNav from './components/includes/HeaderNav.vue';
import FooterNav from './components/includes/FooterNav.vue';
export default {
  name: 'App',
  components: {
    HeaderNav,
    FooterNav
  }
}
</script> 
<style>

</style>
