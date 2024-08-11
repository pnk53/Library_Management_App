<template>
    <div class="container-fluid">
        <div class="row p-5">
            <div class="col-md-8 offset-md-2 col-lg-8 offset-lg-2 col-sm-10 offset-sm-1 border p-5 rounded-pill">
                <div class="row">
                    <form @submit.prevent="onSearchSubmit" class="col-md-12 col-lg-8 col-sm-12">
                        <div class="row">
                            <div class="col-md-8 col-lg-8 col-sm-12">
                                <input type="text" id="search" class="form-control" name="search"
                                    placeholder="Search for users" v-model="searchState.search"
                                    :class="{ 'is-invalid': vSearch.search.$error }">
                                <div class="invalid-feedback" v-if="vSearch.search.$error">
                                    {{ vSearch.search.$errors[0].$message }}
                                </div>
                            </div>
                            <div class="col-md-4 col-lg-4 col-sm-12">
                                <button class="btn btn-outline-success ps-5 pe-5" type="submit"
                                    :disabled="vSearch.$invalid">Search</button>
                            </div>
                        </div>
                    </form>
                    <div class="col-md-12 col-lg-4 col-sm-12 ms-auto">
                        <button class="btn btn-outline-info ps-4 pe-4" :disabled="vSearch.$invalid"
                            @click="clearSearch">Clear
                            Results</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="row p-5">
            <div v-if="searchedUserResults.length > 0 || searchedUserFlaggedResults.length > 0">
                <h3 class="mt-5">Your search results: </h3>
                <div class="bg-info bg-gradient rounded p-3 mt-3">
                    <h5 class="text-dark">Users</h5>
                    <table class="table">
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Username</th>
                            <th>Flag</th>
                        </tr>
                        <tr v-for="user in searchedUserResults" :key="user.id">
                            <td>{{ user.firstName }} {{ user.lastName }}</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.username }}</td>
                            <td>
                                <button class="btn btn-warning pe-5 ps-5" @click="flagCurrentUser(user.id, true)">Flag</button>
                            </td>
                        </tr>
                    </table>
                </div>
                <div class="bg-warning bg-gradient rounded p-3 mt-3">
                    <h5 class="text-dark">Flagged Users</h5>
                    <table class="table">
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Username</th>
                            <th>Un-Flag</th>
                        </tr>
                        <tr v-for="user in searchedUserFlaggedResults" :key="user.id">
                            <td>{{ user.firstName }} {{ user.lastName }}</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.username }}</td>
                            <td>
                                <button class="btn btn-warning pe-5 ps-5" @click="flagCurrentUser(user.id, false)">Un-Flag</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        <div class="row p-5">
            <div
                class="col-md-5 offset-md-1 col-lg-5 offset-lg-1 col-sm-10 offset-sm-1 myCont border border-warning rounded p-3">
                <h1 class="text-white fst-italic mb-4">User Stats</h1>
                <ul class="list-group" data-bs-theme="light">
                    <li class="list-group-item bg-warning bg-gradient" aria-current="true">
                        <h3 class="text-dark">Total Users: {{ tUsers.length }}</h3>
                    </li>
                    <li class="list-group-item">
                        <h5 class="text-dark">Active Users: {{ aUsers }}</h5>
                    </li>
                    <li class="list-group-item">
                        <h5 class="text-dark">Blocked Users: {{ bUsers }}</h5>
                    </li>
                    <li class="list-group-item bg-warning bg-gradient" aria-current="true" @click="getPopular">
                        <h4 class="text-dark">Other Stats</h4>
                    </li>
                    <li class="list-group-item" v-if="popularUsers.length > 0">
                        <h5 class="text-dark">Popular Users:</h5>
                        <h6 v-for="pU in popularUsers" :key="pU">{{ pU }}</h6>
                    </li>
                </ul>
            </div>
            <div
                class="col-md-4 offset-md-1 col-lg-4 offset-lg-1 col-sm-10 offset-sm-1 myCont border border-info rounded p-3">
                <h1 class="text-white fst-italic mb-4">Section Stats</h1>
                <ul class="list-group" data-bs-theme="light">
                    <li class="list-group-item bg-info bg-gradient" aria-current="true">
                        <h3 class="text-dark">Total Sections: {{ tSections.length }}</h3>
                    </li>
                    <li class="list-group-item bg-info bg-gradient" @click="getPopularSection">
                        <h5 class="text-dark">Other Stats:
                        </h5>
                    </li>
                    <li class="list-group-item" v-if="popularSections.length > 0">
                        <h5 class="text-dark">Popular Sections:</h5>
                        <h6 v-for="pS in popularSections" :key="pS">{{ pS }}</h6>
                    </li>
                </ul>
            </div>
        </div>
        <div class="row p-5">
            <div
                class="col-md-5 offset-md-1 col-lg-5 offset-lg-1 col-sm-10 offset-sm-1 myCont border border-warning rounded p-3">
                <h1 class="text-white fst-italic mb-4">Book Stats</h1>
                <ul class="list-group" data-bs-theme="light">
                    <li class="list-group-item bg-warning bg-gradient" aria-current="true">
                        <h3 class="text-dark">Total Books: {{ tBooks.length }}</h3>
                    </li>
                    <li class="list-group-item">
                        <h5 class="text-dark">Top Book:
                            <div class="mt-2">
                                <h6>Name: {{ hBook.name }}</h6>
                                <h6>Author: {{ hBook.author }}</h6>
                                <h6>Rating: {{ hBook.rating }}</h6>
                            </div>
                        </h5>
                    </li>
                    <li class="list-group-item bg-warning bg-gradient" aria-current="true" @click="getPopular">
                        <h4 class="text-dark">Other Stats</h4>
                    </li>
                    <li class="list-group-item" v-if="popularBooks.length > 0">
                        <h5 class="text-dark">Popular Books:</h5>
                        <h6 v-for="pB in popularBooks" :key="pB">{{ pB }}</h6>
                    </li>
                </ul>
            </div>
            <div class="col-md-4 offset-md-1 col-lg-4 offset-lg-1 col-sm-10 myCont border border-info rounded p-3">
                <h1 class="text-white fst-italic mb-4">Issued Book stats</h1>
                <ul class="list-group" data-bs-theme="light">
                    <li class="list-group-item bg-info bg-gradient" aria-current="true">
                        <h3 class="text-dark">Total Issued Books: {{ tIssuedBooks.length }}</h3>
                    </li>
                    <li class="list-group-item">
                        <h5 class="text-dark">Total Ongoing Books: {{ oIssuedBooks.length }}</h5>
                    </li>
                    <li class="list-group-item">
                        <h5 class="text-dark">Total Revoked Books: {{ rIssuedBooks.length }}</h5>
                    </li>
                    <li class="list-group-item bg-info bg-gradient" aria-current="true" @click="getPopular">
                        <h4 class="text-dark">Other Stats</h4>
                    </li>
                    <li class="list-group-item" v-if="popularBooks.length > 0">
                        <h5 class="text-dark">Top Requested Book:
                            <h6>{{ popularBooks[0] }}</h6>
                        </h5>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, computed, reactive } from 'vue';
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useUserStore } from '@/stores/userStore';
import { useSectionStore } from '@/stores/sectionStore';
import { useEBookStore } from '@/stores/ebookStore';
import { useIssuedBookStore } from '@/stores/issuedBookStore';
import { useSearchStore } from '@/stores/searchStore';
import { useAlertStore } from '@/stores/alertStore';

const userStore = useUserStore();
const sectionStore = useSectionStore();
const eBookStore = useEBookStore();
const issuedBookStore = useIssuedBookStore();
const searchStore = useSearchStore();
const alertStore = useAlertStore();

const tUsers = ref([]);
const aUsers = ref(null);
const bUsers = ref(null);
const popularUsers = ref([]);

const tSections = ref([]);
const popularSections = ref([]);

const tBooks = ref([]);
const hBook = ref({});
const popularBooks = ref([]);

const tIssuedBooks = ref([]);
const rIssuedBooks = ref([]);
const oIssuedBooks = ref([]);

const getPopular = (() => {
    const userMap = new Map();
    const bookMap = new Map();
    tIssuedBooks.value.forEach(ib => {
        if (userMap.has(ib.issuerName)) {
            userMap.set(ib.issuerName, userMap.get(ib.issuerName) + 1);
        }
        else {
            userMap.set(ib.issuerName, 1);
        }

        if (bookMap.has(ib.bookName)) {
            bookMap.set(ib.bookName, bookMap.get(ib.bookName) + 1);
        }
        else {
            bookMap.set(ib.bookName, 1);
        }
    });
    const desUser = Array.from(userMap.entries()).sort((a, b) => b[1] - a[1]).slice(0, 2);
    popularUsers.value = desUser.map(entry => entry[0]);
    const desBook = Array.from(bookMap.entries()).sort((a, b) => b[1] - a[1]).slice(0, 2);
    popularBooks.value = desBook.map(entry => entry[0]);
})

const getPopularSection = (() => {
    const sectionMap = new Map();
    tBooks.value.forEach(book => {
        let sectionList = book.section.split(',');
        for (let s in sectionList) {
            if (sectionMap.has(sectionList[s])) {
                sectionMap.set(sectionList[s], sectionMap.get(sectionList[s]) + 1);
            }
            else {
                sectionMap.set(sectionList[s], 1);
            }
        }
    });
    const desSection = Array.from(sectionMap.entries()).sort((a, b) => b[1] - a[1]).slice(0, 2);
    popularSections.value = desSection.map(entry => entry[0]);
})

onMounted(async () => {
    await userStore.retrieveAllUsers();
    tUsers.value = userStore.allUsers;
    aUsers.value = userStore.allUsers.filter(u => u.flagged == false).length;
    bUsers.value = userStore.allUsers.filter(u => u.flagged == true).length;

    await sectionStore.retrieveAllSections();
    tSections.value = sectionStore.allSections;

    await eBookStore.retrieveAllEBooks();
    tBooks.value = eBookStore.allEBooks;
    const topBook = eBookStore.allEBooks.sort((a, b) => b.rating - a.rating);
    hBook.value = {
        name: topBook[0].title,
        author: topBook[0].author,
        rating: topBook[0].rating
    };

    await issuedBookStore.retrieveAllIssuedBooks();
    tIssuedBooks.value = issuedBookStore.allIssuedBooks;
    rIssuedBooks.value = issuedBookStore.allIssuedBooks.filter(rb => rb.status == "Revoked");
    oIssuedBooks.value = issuedBookStore.allIssuedBooks.filter(ob => ob.status == "Ongoing");

    console.log(popularUsers.value + " " + popularBooks.value + " " + popularSections.value)
})

const searchState = reactive({
    search: ref(null)
})

const searchRules = computed(() => {
    return {
        search: { required }
    }
})

const vSearch = useVuelidate(searchRules, searchState, {
    $autoDirty: true
})

const searchedUserResults = ref([]);
const searchedUserFlaggedResults = ref([]);

const onSearchSubmit = (async () => {
    await searchStore.getAllSearchedUsers(searchState.search.toLowerCase());
    searchedUserResults.value = searchStore.searchedUser.filter(u => u.flagged == false);
    searchedUserFlaggedResults.value = searchStore.searchedUser.filter(u => u.flagged == true);
    if (searchedUserResults.value.length == 0 && searchedUserFlaggedResults.value.length ==0) {
        let message = "No search results for: " + searchState.search
        alertStore.error(message);
    }
})

const clearSearch = (() => {
    searchedUserResults.value = [];
})

const flagCurrentUser = (async(id, status)=>{
    try {
        await userStore.flagUser(id,status);
        setTimeout(() => {
            let message = "User "
            if(status == true){
                message = message + "flagged successfully"
            }
            else{
                message = message + "unflagged successfully"
            }
            alertStore.success(message);
        }, 200)
    }
    catch (error) {
        console.log(userStore.errorMessage);
        let message = "User flag failed: " + userStore.errorMessage;
        alertStore.error(message);
    }
})

</script>

<style scoped>
.myCont {
    min-height: 50dvh;
}
table {
    width: 100%;
    border: 2px solid #000;
    border-collapse: collapse;
}

th,
td {
    padding: 12px;
    text-align: left;
    color: #212529;
    background-color: #f8f9fa;
    border-bottom: 1px solid #ddd;
}

th {
    background-color: #212529;
    color: white;
}
</style>