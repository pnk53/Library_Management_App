<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-10 offset-md-1 col-lg-10 offset-lg-1 col-sm-10 offset-sm-1">
                <h1 class="text-warning">
                    {{ user.name }}
                </h1>
                <h2 class="text-warning">
                    {{ user.user_id }}
                </h2>
            </div>
        </div>
    </div>
</template>

<script setup>

const user = {
    "name": localStorage.getItem('name'),
    "user_id": localStorage.getItem('user_id')
}

</script>

<style scoped>

</style>