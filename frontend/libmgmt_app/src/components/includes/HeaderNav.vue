<template>
    <nav class="navbar navbar-expand-lg navbar-expand-md bg-warning bg-gradient" id="myNavbar">
        <div class="container-fluid">
            <a class="navbar-brand ms-5 fs-2 fw-bold text-black" href="#">LMS</a>
            <button class="navbar-toggler bg-dark" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item" v-if="isLogged">
                        <router-link class="nav-link text-black" :to="userHome" active-class="active" exact-active-class="extract-active">Home</router-link>
                    </li>
                    <li class="nav-item" v-if="isLogged">
                        <router-link class="nav-link text-black" to="/explorer" active-class="active" exact-active-class="extract-active">Explorer</router-link>
                    </li>
                    <li class="nav-item" v-if="isAdmin && isLogged">
                        <router-link class="nav-link text-black" to="/stats" active-class="active" exact-active-class="extract-active">Stats</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link text-black" to="/AboutUs" active-class="active" exact-active-class="extract-active">About Us</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link text-black" to="/ContactUs" active-class="active" exact-active-class="extract-active">Contact Us</router-link>
                    </li>
                </ul>
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item" v-if="isSigned">
                        <router-link to="/signUp" class="nav-link text-black" active-class="active" exact-active-class="extract-active">
                            SignUp
                        </router-link>
                    </li>
                    <li class="nav-item" v-if="isLogin">
                        <router-link to="/" class="nav-link text-black" active-class="active" exact-active-class="extract-active">
                            Login
                        </router-link>
                    </li>
                    <li class="nav-item fw-bold" v-if="isLogged">
                        <router-link to="/profile" class="nav-link text-black" active-class="active" exact-active-class="extract-active">
                            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor"
                                class="bi bi-person-circle" viewBox="0 0 16 16">
                                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
                                <path fill-rule="evenodd"
                                    d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z" />
                            </svg>
                            Profile
                        </router-link>
                    </li>
                    <li class="nav-item" v-if="isLogged">
                        <a class="nav-link text-black myLink" @click="logout">
                            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="#fff"
                                class="bi bi-box-arrow-right" viewBox="0 0 16 16">
                                <path fill-rule="evenodd"
                                    d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z" />
                                <path fill-rule="evenodd"
                                    d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z" />
                            </svg>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { useAlertStore } from '@/stores/alertStore';
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();
const alertStore = useAlertStore();

const isSigned = computed(() => {
    return route.path == '/';
})
const isLogin = computed(() => {
    return route.path == '/signUp' || route.path == '/ContactUs' && !localStorage.getItem('name') || route.path == '/AboutUs' && !localStorage.getItem('name');
})
const isLogged = computed(() => {
    if ((route.path == '/' || route.path == '/signUp' || route.path == '/ContactUs' || route.path == '/AboutUs') && !localStorage.getItem('name')) {
        return false;
    }
    else {
        return true;
    }
})
const isAdmin = computed(() => {
    if (localStorage.getItem('userType') == 'Librarian'){
        return true;
    }
    else{
        return false;
    }
})

const userHome = computed(() => {
    if(localStorage.getItem('userType') == 'Librarian'){
        return "/librarianHome";
    }
    else{
        return "/userHome";
    }
})

const logout = (() => {
    localStorage.clear();
    router.push('/');
    setTimeout(()=>{
    alertStore.success("Logged out successfully");
    },300);
})

</script>

<style scoped>
#myNavbar {
    box-shadow: 2px 4px 15px #000;
    min-height: 20dvh;
    border-radius: 0px 0px 70px 70px;
    color: #000 !important;
    font-size: larger;
}
.myLink{
    cursor: pointer;
}
.active {
    color: #fff !important;
}
.extract-active{
    color: #fff !important;
}
</style>