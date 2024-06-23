<template>
  <h1>Welcome to Vue 3</h1>
  <h1>{{ msg }}</h1>
  <h1 class="text-capitalize" >This is the page to check the status of healthcheck API.</h1>
  <button @click="navigateIntoWorld" class="btn btn-lg btn-dark">Click me !!!</button>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  methods: {
    navigateIntoWorld(){
      this.$router.push("/world")
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
