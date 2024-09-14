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
                <div class="row g-3 mt-3 mb-3 d-flex">
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
                    <div class="col-md-4 col-lg-4 ms-auto">
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
                            <li class="nav-item" @click="toggleList">
                                <a class="nav-link myLink fw-bold" :class="showList ? 'text-black' : 'text-white'">Pending Requests</a>
                            </li>
                            <li class="nav-item" @click="toggleList">
                                <a class="nav-link text-dark myLink fw-bold" :class="{'text-white': showList}">Pending Revokes</a>
                            </li>
                        </ul>
                    </nav>
                    <div v-if="showList">
                        <div class="d-flex justify-content-center" v-if="loading">
                            <div class="spinner-border text-danger m-5" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        <div v-else>
                            <div v-if="allOngoingBooks.length == 0" class="mt-3 p-2">
                                <p class="text-white text-center">You have no requests to be revoked.</p>
                            </div>
                            <div class="card-group">
                                <div class="col-md-12 col-lg-12 col-sm-12" v-for="Obook in allOngoingBooks"
                                    :key="Obook.id">
                                    <div class="card m-3 p-2">
                                        <div class="card-header">
                                            <h5 class="text-warning">{{ Obook.bookName }}</h5>
                                        </div>
                                        <div class="card-body">
                                            <p class="card-title mb-3">Current Issuer: {{ Obook.issuerName }}</p>
                                            <p class="text-secondary">Returned Date: {{ Obook.returnedDate }}</p>
                                        </div>
                                        <div class="card-footer">
                                            <div class="d-flex justify-content-between">
                                                <button class="btn btn-danger" @click="revokeBookRequest(Obook)">Revoke</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else>
                        <div class="d-flex justify-content-center" v-if="reqLoading">
                            <div class="spinner-border text-danger m-5" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        <div v-else>
                            <div v-if="allRequestedBooks.length == 0" class="mt-3 p-2">
                                <p class="text-white text-center">You have no pending book requests.</p>
                            </div>
                            <div class="card-group">
                                <div class="col-md-12 col-lg-12 col-sm-12" v-for="Rbook in allRequestedBooks" :key="Rbook.id">
                                    <div class="card m-3 p-2">
                                        <div class="card-header">
                                            <h5 class="text-warning">{{ Rbook.bookName }}</h5>
                                        </div>
                                        <div class="card-body">
                                            <p class="card-title mb-3">Requested by: {{ Rbook.issuerName }}</p>
                                        </div>
                                        <div class="card-footer">
                                            <div class="d-flex justify-content-between">
                                                <button class="btn btn-success" @click="grantBookRequest(Rbook)">Grant</button>
                                                <button class="btn btn-danger" @click="revokeBookRequest(Rbook)">Deny</button>
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
                    <h5>Create new Section
                        <button class="btn btn-dark" @click="loadSectionComponent">Add Section</button>
                        <component :is="sectionModal" v-if="isSectionModalLoaded" @close="unloadSectionComponent">
                        </component>
                    </h5>
                    <h5>Add new E-book <button class="btn btn-dark" @click="loadEBookComponent">Upload E-book</button>
                        <component :is="ebookModal" v-if="isEBookModalLoaded" @close="unloadEBookComponent"></component>
                    </h5>
                </div>
                <div v-if="searchedSectionResults.length > 0 || searchedEBookResults.length > 0">
                    <h3 class="mt-5">Your search results: </h3>
                    <div class="bg-info bg-gradient rounded p-3 mt-3">
                        <h5 class="text-dark">Sections</h5>
                        <table class="table">
                            <tr>
                                <th>Name</th>
                                <th>Published</th>
                                <th>View</th>
                            </tr>
                            <tr v-for="section in searchedSectionResults" :key="section.id">
                                <td>{{ section.name }}</td>
                                <td>{{ section.dateCreated }}</td>
                                <td><button class="btn" @click="viewSection(section.id)">View</button></td>
                            </tr>
                        </table>
                    </div>
                    <div class="bg-light bg-gradient rounded p-3 mt-3">
                        <h5 class="text-dark">E-Books</h5>
                        <table class="table">
                            <tr>
                                <th>Title</th>
                                <th>Author</th>
                                <th>Status</th>
                                <th>View</th>
                            </tr>
                            <tr v-for="book in searchedEBookResults" :key="book.id">
                                <td>{{ book.title }}</td>
                                <td>{{ book.author }}</td>
                                <td>{{ book.status }}</td>
                                <td><button class="btn" @click="viewEBook(book.id)">View</button></td>
                            </tr>
                        </table>
                    </div>
                </div>
                <div v-else>
                    <div class="border border-info p-4 rounded mb-2">
                        <h2 class="text-info">Sections</h2>
                        <div class="d-flex justify-content-center" v-if="loading">
                            <div class="spinner-border text-info m-5" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        <div class="row" v-else>
                            <div v-if="topSections.length > 0">
                                <div class="col-md-4 col-lg-3 col-sm-5" v-for="section in topSections" :key="section.id">
                                    <div class="card bg-info bg-gradient mt-2 mySectionCard">
                                        <div class="card-header">
                                            <h5 class="text-dark fst-italic">{{ section.name }}</h5>
                                        </div>
                                        <div class="card-body">
                                            <p class="card-title text-dark">Description: {{ section.description }}</p>
                                            <p class="text-secondary">Published: {{ section.dateCreated }}</p>
                                        </div>
                                        <div class="card-footer">
                                            <div class="d-flex justify-content-between">
                                                <button class="btn btn-dark" @click="viewSection(section.id)">View</button>
                                                <button class="btn btn-danger"
                                                    @click="deleteCurrentSection(section.id)">Delete</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else>
                                <h6 class="text-secondary">No Sections added yet. Please add section(s).</h6>
                            </div>
                        </div>
                        <h5 class="mt-3 d-flex"><router-link to="/explorer"
                                class="text-decoration-none text-info ms-auto">View all</router-link>
                        </h5>
                    </div>
                    <div class="border border-light p-4 rounded mb-2">
                        <h2 class="text-light">E-books</h2>
                        <div class="d-flex justify-content-center" v-if="loading">
                            <div class="spinner-border text-light m-5" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        <div class="row" v-else>
                            <div v-if="topEbooks.length > 0">
                                <div class="col-md-4 col-lg-3 col-sm-5" v-for="book in topEbooks" :key="book.id">
                                    <div class="card bg-light bg-gradient mt-2 myCard">
                                        <div class="card-header">
                                            <h5 class="text-dark fst-italic">{{ book.title }}</h5>
                                        </div>
                                        <div class="card-body">
                                            <p class="card-title text-dark mb-3">Author: {{ book.author }}</p>
                                            <p class="card-title text-dark mb-3">Language: {{ book.language }}</p>
                                            <p class="card-title text-dark mb-3">Published: {{ book.releaseDate }}</p>
                                            <p class="text-secondary">Status: {{ book.status }}</p>
                                            <p class="text-secondary">Rating: {{ book.rating }}</p>
                                        </div>
                                        <div class="card-footer">
                                            <div class="d-flex justify-content-between">
                                                <button class="btn btn-dark" @click="viewEBook(book.id)">View</button>
                                                <button class="btn btn-danger"
                                                    @click="deleteCurrentEBook(book.id)">Delete</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else>
                                <h6 class="text-secondary">No EBooks added yet. Please add ebook(s).</h6>
                            </div>
                        </div>
                        <h5 class="mt-3 d-flex"><router-link to="/explorer"
                                class="text-decoration-none text-light ms-auto">View all</router-link>
                        </h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useVuelidate } from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { computed, defineAsyncComponent, reactive, ref, shallowRef, onMounted } from 'vue';
import { useSectionStore } from '@/stores/sectionStore';
import { useRouter } from 'vue-router';
import { useAlertStore } from '@/stores/alertStore';
import { useEBookStore } from '@/stores/ebookStore';
import { useSearchStore } from '@/stores/searchStore';
import { useIssuedBookStore } from '@/stores/issuedBookStore';

const admin = {
    "name": localStorage.getItem('name'),
    "user_id": localStorage.getItem('user_id')
}
const router = useRouter();
const alertStore = useAlertStore();

const sectionModal = shallowRef(null);
const isSectionModalLoaded = shallowRef(false);

function loadSectionComponent() {
    isSectionModalLoaded.value = true;
    sectionModal.value = defineAsyncComponent(() => import("../components/AddSection.vue"))
}

async function unloadSectionComponent() {
    isSectionModalLoaded.value = false;
    sectionModal.value = null;
    await getAllSections();
}

const ebookModal = shallowRef(null)
const isEBookModalLoaded = shallowRef(false)

function loadEBookComponent() {
    isEBookModalLoaded.value = true;
    ebookModal.value = defineAsyncComponent(() => import("../components/AddEBook.vue"))
}

async function unloadEBookComponent() {
    isEBookModalLoaded.value = false;
    ebookModal.value = null;
    await getAllEbooks();
}

onMounted(async () => {
    await getAllSections();
    await getAllEbooks();
    await getAllIssuedBook();
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

const searchStore = useSearchStore();
const searchedSectionResults = ref([]);
const searchedEBookResults = ref([]);

const onSearchSubmit = (async () => {
    await searchStore.getAllSearchedSectionsAndEBooks(searchState.search.toLowerCase());
    searchedSectionResults.value = searchStore.searchedSections;
    searchedEBookResults.value = searchStore.searchedEBooks;
    if (searchedSectionResults.value.length == 0 && searchedEBookResults.value.length == 0) {
        let message = "No search results for: " + searchState.search
        alertStore.error(message);
    }
})

const clearSearch = (() => {
    searchedSectionResults.value = [];
    searchedEBookResults.value = [];
})

const loading = ref(false);

const issuedBookStore = useIssuedBookStore();
const reqLoading = ref(false);
const showList = ref(false);
const allRequestedBooks = ref([]);
const allOngoingBooks = ref([]);
const toggleList = (() => {
    showList.value = !showList.value;
});

const getAllIssuedBook = (async () => {
    try {
        reqLoading.value = true;
        await issuedBookStore.retrieveAllIssuedBooks();
        reqLoading.value = false;
        allOngoingBooks.value = issuedBookStore.allIssuedBooks.filter(ob => ob.status == "Ongoing");
        allRequestedBooks.value = issuedBookStore.allIssuedBooks.filter(rb => rb.status == "Requested");
    }
    catch (error) {
        console.log(error);
    }
})

const revokeBookRequest = (async (revokeBookData) => {
    try {
        await issuedBookStore.revokeBookRequest(revokeBookData.id);
        await eBookStore.updateRevokedBookInfo(revokeBookData.bookId);
        await getAllIssuedBook();
        await getAllEbooks();
        setTimeout(() => {
            alertStore.success("E-Book revoked successfully")
        }, 200)
    }
    catch (error) {
        console.log(issuedBookStore.errorMessage);
        let message = "E-Book revoked failed: " + issuedBookStore.errorMessage;
        alertStore.error(message);
    }
})

const grantBookRequest = (async (requestedbookData) => {
    try{
        await issuedBookStore.acceptBookRequest(requestedbookData.id);
        await eBookStore.updateAssignedBookInfo(requestedbookData.bookId, requestedbookData);
        await getAllIssuedBook();
        await getAllEbooks();
        setTimeout(() => {
            alertStore.success("E-Book granted successfully")
        }, 200)
    }
    catch (error) {
        console.log(issuedBookStore.errorMessage);
        let message = "Granting E-Book failed: " + issuedBookStore.errorMessage;
        alertStore.error(message);
    }
})

const sectionStore = useSectionStore();
const topSections = ref([]);

const getAllSections = (async () => {
    try {
        loading.value = true;
        await sectionStore.retrieveAllSections();
        loading.value = false;
        topSections.value = sectionStore.allSections.sort(()=>0.5 - Math.random()).slice(0,5);
    }
    catch (error) {
        console.log(error);
    }
})

function viewSection(id) {
    router.push({ name: 'ViewSection', params: { sectionId: id } });
}

const deleteCurrentSection = (async (id) => {
    try {
        await sectionStore.deleteSection(id);
        await getAllSections();
        setTimeout(() => {
            alertStore.success("Section deleted successfully")
        }, 200)
    } catch (error) {
        console.log(sectionStore.errorMessage);
        let message = "Section Delete failed: " + sectionStore.errorMessage;
        alertStore.error(message);
    }
})

const eBookStore = useEBookStore();
const topEbooks = ref([]);

const getAllEbooks = (async () => {
    try {
        loading.value = true;
        await eBookStore.retrieveAllEBooks();
        loading.value = false;
        topEbooks.value = eBookStore.allEBooks.sort((a,b)=>b.rating - a.rating).slice(0,5);
    }
    catch (error) {
        console.log(error);
    }
})

function viewEBook(id) {
    router.push({ name: 'ViewEBook', params: { eBookId: id } });
}

const deleteCurrentEBook = (async (id) => {
    try {
        await eBookStore.deleteEBook(id);
        await getAllEbooks();
        setTimeout(() => {
            alertStore.success("EBook deleted successfully")
        }, 200)
    } catch (error) {
        console.log(eBookStore.errorMessage);
        let message = "E-Book Delete failed: " + eBookStore.errorMessage;
        alertStore.error(message);
    }
})

</script>

<style scoped>
.myRequestCont {
    min-height: 100dvh;
    max-height: 100dvh;
    overflow-y: scroll;
}

.myLink {
    cursor: pointer;
}

.myCard {
    min-height: 50dvh;
    max-height: 50dvh;
}

.mySectionCard {
    min-height: 40dvh;
    max-height: 40dvh;
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