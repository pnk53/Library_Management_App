<template>
    <h1>Welcome to Vue 3</h1>
    <h1>{{ msg }}</h1>
    <h1 class="text-capitalize text-success">This is the page to check router. This in upon entering the World</h1>
</template>

<script>
import axios from 'axios';
export default {
    name: 'IntoWorld',
    data(){
        return{
            msg: '',
        };
    },
    methods: {
        getHealthcheck(){
            const path = 'http://localhost:5000/api/healthcheck';
            axios.get(path)
            .then(
                (res)=>{
                this.msg = res.data;
            }
            )
            .catch(
                (error)=>{
                    console.error(error)
                }
            );
        },
    },
    created(){
        this.getHealthcheck();
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>