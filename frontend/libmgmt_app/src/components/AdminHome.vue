<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-6 offset-md-0 col-lg-6 offset-lg-0 col-sm-10 offset-sm-1">
                <h1 class="text-warning mt-3 mb-3">
                    Welcome {{ admin.name }} !!!
                </h1>
                <p class="text-secondary mb-5">This is the admin homepage where in he can manage book requests, section,
                    e-books, user, etc.</p>
            </div>
            <div class="col-md-5 offset-md-1 col-lg-5 offset-lg-1 col-sm-10 offset-sm-1">
                <div class="row g-3 mt-3 mb-3">
                    <form @submit.prevent="onSearchSubmit" class="col-md-8 col-lg-8">
                        <div class="row">
                            <div class="col-md-8 col-lg-8">
                                <input type="text" id="search" class="form-control" name="search"
                                    placeholder="Search for sections, e-books" v-model="searchState.search"
                                    :class="{ 'is-invalid': vSearch.search.$error }">
                                <div class="invalid-feedback" v-if="vSearch.search.$error">
                                    {{ vSearch.search.$errors[0].$message }}
                                </div>
                            </div>
                            <div class="col-md-4 col-lg-4">
                                <button class="btn btn-outline-success ps-4 pe-4" type="submit"
                                    :disabled="vSearch.$invalid">Search</button>
                            </div>
                        </div>
                    </form>
                    <div class="col-md-4 col-lg-4">
                        <button class="btn btn-outline-info" :disabled="vSearch.$invalid" @click="clearSearch">Clear
                            Results</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-3 offset-md-0 col-lg-3 offset-lg-0 col-sm-10 offset-sm-1">
                <div class="bg-warning bg-gradient rounded mb-2 myRequestCont">
                    <h3 class="text-dark text-center p-2 mt-2 mb-2">Book Requests</h3>
                    <nav class="navbar navbar-expand-lg navbar-expand-md navbar-expand-sm border-bottom border-dark">
                        <ul class="navbar-nav mx-auto mb-2">
                            <li class="nav-item" @click="toggleList"><a
                                    class="nav-link text-dark myLink fw-bold">Pending
                                    Requests</a></li>
                            <li class="nav-item"><a class="nav-link text-dark myLink fw-bold">Pending Revokes</a></li>
                        </ul>
                    </nav>
                    <div v-if="showList">
                        <div class="d-flex justify-content-center" v-if="loading">
                            <div class="spinner-border text-danger m-5" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        <div v-else>
                            <div class="card-group">
                                <div class="col-md-12 col-lg-12 col-sm-12">
                                    <div class="card m-3 p-2">
                                        <div class="card-header">
                                            <h5 class="text-info">Shiva's Trilogy: First part</h5>
                                        </div>
                                        <div class="card-body">
                                            <p class="card-title mb-3">Alex Merchant</p>
                                            <div class="d-flex justify-content-between">
                                                <button class="btn btn-success">Grant</button>
                                                <button class="btn btn-danger">Deny</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-9 offset-md-0 col-lg-9 offset-lg-0 col-sm-10 offset-sm-1">
                <div class="bg-primary bg-gradient p-4 rounded mb-2">
                    <h2 class="text-dark">Quick Links: </h2>
                    <h5>Create new Section <button class="btn btn-dark">Add Section</button></h5>
                    <h5>Add new E-book <button class="btn btn-dark">Upload E-book</button></h5>
                </div>
                <div v-if="searchResults">
                    <h2>Your search result: {{ searchResults }}</h2>
                </div>
                <div v-else>
                    <div class="border border-info p-4 rounded mb-2">
                        <h2 class="text-info">Sections</h2>
                        <div class="row">
                            <div class="col-md-3 col-lg-3 col-sm-5">
                                <div class="card bg-info bg-gradient mt-2">
                                    <div class="card-header">
                                        <h5 class="text-dark">Science Friction</h5>
                                    </div>
                                    <div class="card-body">
                                        <p class="card-title text-dark mb-3">07/07/2024</p>
                                        <p class="text-dark">This is the random description for the section.</p>
                                        <div class="d-flex justify-content-between">
                                            <button class="btn btn-dark">View</button>
                                            <button class="btn btn-danger">Delete</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <h5 class="mt-3 d-flex"><router-link to="/explorer" class="text-decoration-none text-info ms-auto">View all</router-link></h5>
                    </div>
                    <div class="border border-light p-4 rounded mb-2">
                        <h2 class="text-light">E-books</h2>
                        <div class="row">
                            <div class="col-md-3 col-lg-3 col-sm-5">
                                <div class="card bg-light bg-gradient mt-2">
                                    <div class="card-header">
                                        <h5 class="text-dark">Shiva's trilogy: First part</h5>
                                    </div>
                                    <div class="card-body">
                                        <p class="card-title text-dark mb-3">07/07/2024</p>
                                        <p class="text-dark">This is the random description for the section.</p>
                                        <div class="d-flex justify-content-between">
                                            <button class="btn btn-dark">View</button>
                                            <button class="btn btn-danger">Delete</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <h5 class="mt-3 d-flex"><router-link to="/explorer" class="text-decoration-none text-light ms-auto">View all</router-link></h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import useVuelidate from '@vuelidate/core';
import { required, alphaNum } from '@vuelidate/validators';
import { computed, reactive, ref } from 'vue';

const admin = {
    "name": localStorage.getItem('name'),
    "user_id": localStorage.getItem('user_id')
}

const searchState = reactive({
    search: ref(null)
})

const searchRules = computed(() => {
    return {
        search: { required, alphaNum }
    }
})

const vSearch = useVuelidate(searchRules, searchState, {
    $autoDirty: true
})

const searchResults = ref(null)

const onSearchSubmit = (() => {
    return searchResults.value = searchState.search
})

const clearSearch = (() => {
    searchResults.value = null;
})

const loading = ref(false);

const showList = ref(false);

const toggleList = (() => {
    showList.value = !showList.value;
});

</script>

<style scoped>
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(33, 37, 41, 1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background-color: #212529;
    -webkit-box-shadow: inset 0 0 6px rgba(90, 90, 90, 0.7);
}

.myRequestCont {
    min-height: 100dvh;
    max-height: 100dvh;
    overflow-y: scroll;
}

.myLink {
    cursor: pointer;
}
</style>