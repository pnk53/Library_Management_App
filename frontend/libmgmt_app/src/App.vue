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
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgb(85, 83, 85);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background-color: #ffffff;
    -webkit-box-shadow: inset 0 0 6px rgba(85, 83, 85, 0.7);
}
</style>
