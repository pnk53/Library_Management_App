<template>
    <div class="container-fluid">
        <div class="row">
            <div
                class="col-md-6 offset-md-3 col-lg-6 offset-lg-3 col-sm-10 offset-sm-1 border border-light rounded-pill mt-4 ps-5">
                <div class="row g-3 mt-2 mb-4">
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
                                <button class="btn btn-outline-success ps-5 pe-5" type="submit"
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
        <div class="row p-5">
            <div v-if="searchedSectionResults.length > 0 || searchedEBookResults.length > 0">
                <h3 class="mt-5">Your search results: </h3>
                <div class="bg-info bg-gradient rounded p-3 mt-3">
                    <h5 class="text-dark">Sections</h5>
                    <table class="table" v-if="searchedSectionResults.length > 0">
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
                    <h6 class="text-black" v-else>No Section matching your search: {{ searchState.search }}</h6>
                </div>
                <div class="bg-light bg-gradient rounded p-3 mt-3">
                    <h5 class="text-dark">E-Books</h5>
                    <table class="table" v-if="searchedEBookResults.length > 0">
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
                    <h6 class="text-black" v-else>No EBook matching your search: {{ searchState.search }}</h6>
                </div>
            </div>
        </div>
        <div class="border border-3 border-info rounded m-5 p-3 mySectionCont d-flex flex-column">
            <div class="d-flex mb-2">
                <h2 class="text-info">Sections</h2>
                <button class="btn btn-outline-info ms-auto" :hidden="!isAdmin" @click="loadSectionComponent">Add
                    Section</button>
                <component :is="sectionModal" v-if="isSectionModalLoaded" @close="unloadSectionComponent">
                </component>
            </div>
            <div class="d-flex justify-content-center" v-if="loading">
                <div class="spinner-border text-info m-5" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <transition name="fade" mode="out-in" v-else>
                <div class="row" :key="currentSectionPage">
                    <div class="col-lg-3 col-lg-0 col-md-3 offset-md-0 col-sm-10 offset-sm-1"
                        v-for="section in sectionPagination" :key="section.name">
                        <div class="card bg-info bg-gradient mt-2 mb-2 mySectionCard">
                            <div class="card-header">
                                <h5 class="text-black fst-italic">{{ section.name }}</h5>
                            </div>
                            <div class="card-body">
                                <p class="card-title text-black">Description: {{ section.description }}</p>
                                <p class="card-title text-black">Published: {{ section.dateCreated }}</p>
                            </div>
                            <div class="card-footer">
                                <div class="d-flex justify-content-between">
                                    <button class="btn btn-dark" @click="viewSection(section.id)">View</button>
                                    <button class="btn btn-danger" v-if="isAdmin"
                                        @click="deleteCurrentSection(section.id)">Delete</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="sectionPagination.length == 0">
                        <h5 class="text-secondary">No Sections added yet. Please add section(s).</h5>
                    </div>
                </div>
            </transition>
            <nav class="mt-5 mt-auto">
                <ul class="pagination justify-content-center">
                    <li class="page-item" :class="{ disabled: currentSectionPage === 1 }">
                        <a class="page-link" href="#" @click.prevent="previousSectionPage">&lt;&lt;</a>
                    </li>
                    <li v-for="page in totalSectionPages" :key="page" class="page-item"
                        :class="{ active: page === currentSectionPage }">
                        <a class="page-link" href="#" @click.prevent="goToSectionPage(page)">{{ page }}</a>
                    </li>
                    <li class="page-item" :class="{ disabled: currentSectionPage === totalSectionPages }">
                        <a class="page-link" href="#" @click.prevent="nextSectionPage">&gt;&gt;</a>
                    </li>
                </ul>
            </nav>
        </div>
        <div class="border border-3 border-light rounded m-5 p-3 mySectionCont d-flex flex-column">
            <div class="d-flex mb-2">
                <h2 class="text-light">E-Books</h2>
                <button class="btn btn-outline-light ms-auto" :hidden="!isAdmin" @click="loadEBookComponent">Add
                    EBook</button>
                <component :is="ebookModal" v-if="isEBookModalLoaded" @close="unloadEBookComponent">
                </component>
            </div>
            <div class="d-flex justify-content-center" v-if="loading">
                <div class="spinner-border text-light m-5" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <transition name="fade" mode="out-in" v-else>
                <div class="row" :key="currentEBookPage">
                    <div class="col-lg-3 offset-lg-0 col-md-3 offset-md-0 col-sm-10 offset-sm-1"
                        v-for="ebook in eBookPagination" :key="ebook.id">
                        <div class="card bg-light bg-gradient mt-2 mb-2 myCard">
                            <div class="card-header">
                                <h5 class="text-black fst-italic">{{ ebook.title }}</h5>
                            </div>
                            <div class="card-body">
                                <p class="card-title text-dark mb-3">Author: {{ ebook.author }}</p>
                                <p class="card-title text-dark mb-3">Language: {{ ebook.language }}</p>
                                <p class="card-title text-dark mb-3">Published: {{ ebook.releaseDate }}</p>
                                <p class="card-title text-dark mb-3">Section(s): {{ ebook.section }}</p>
                                <p class="text-secondary">Status: {{ ebook.status }}</p>
                                <p class="text-secondary">Rating: {{ ebook.rating }}</p>
                            </div>
                            <div class="card-footer">
                                <div class="d-flex justify-content-between">
                                    <button class="btn btn-dark" @click="viewEBook(ebook.id)">View</button>
                                    <button class="btn btn-danger" v-if="isAdmin"
                                        @click="deleteCurrentEBook(ebook.id)">Delete</button>
                                    <button class="btn btn-success" v-if="!isAdmin && ebook.status ==='Available'" @click="onBookRequest(ebook)">Request</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="eBookPagination.length == 0">
                        <h5 class="text-secondary">No EBooks added yet. Please add ebook(s).</h5>
                    </div>
                </div>
            </transition>
            <nav class="mt-5 mt-auto">
                <ul class="pagination justify-content-center">
                    <li class="page-item" :class="{ disabled: currentEBookPage === 1 }">
                        <a class="page-link" href="#" @click.prevent="previousEBookPage">&lt;&lt;</a>
                    </li>
                    <li v-for="page in totalSectionPages" :key="page" class="page-item"
                        :class="{ active: page === currentEBookPage }">
                        <a class="page-link" href="#" @click.prevent="goToEBookPage(page)">{{ page }}</a>
                    </li>
                    <li class="page-item" :class="{ disabled: currentEBookPage === totalEBookPages }">
                        <a class="page-link" href="#" @click.prevent="nextEBookPage">&gt;&gt;</a>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
</template>

<script setup>
import { useAlertStore } from '@/stores/alertStore';
import { useSectionStore } from '@/stores/sectionStore';
import { useEBookStore } from '@/stores/ebookStore';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { computed, reactive, ref, onMounted, shallowRef, defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';
import { useSearchStore } from '@/stores/searchStore';
import { useIssuedBookStore } from '@/stores/issuedBookStore';

const loading = ref(false)
const sectionStore = useSectionStore();
const eBookStore = useEBookStore();
const alertStore = useAlertStore();
const router = useRouter();

const isAdmin = computed(() => {
    if (localStorage.getItem('userType') == 'Librarian') {
        return true;
    }
    else {
        return false;
    }
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
    if(searchedSectionResults.value.length == 0 && searchedEBookResults.value.length == 0){
        let message = "No search results for: " + searchState.search
        alertStore.error(message);
    }
})

const clearSearch = (() => {
    searchedSectionResults.value = [];
    searchedEBookResults.value = [];
})

const sectionModal = shallowRef(null)
const isSectionModalLoaded = shallowRef(false)

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
})

const sections = ref([]);

const cardsPerPage = 8;
const currentSectionPage = ref(1);

const getAllSections = (async () => {
    try {
        loading.value = true;
        await sectionStore.retrieveAllSections();
        loading.value = false;
        sections.value = sectionStore.allSections;
    }
    catch (error) {
        console.log(error);
    }
})

const totalSectionPages = computed(() => Math.ceil(sections.value.length / cardsPerPage));

const sectionPagination = computed(() => {
    const start = (currentSectionPage.value - 1) * cardsPerPage;
    const end = start + cardsPerPage;
    return sections.value.slice(start, end);
});

const previousSectionPage = () => {
    if (currentSectionPage.value > 1) {
        currentSectionPage.value--;
    }
};

const nextSectionPage = () => {
    if (currentSectionPage.value < totalSectionPages.value) {
        currentSectionPage.value++;
    }
};

const goToSectionPage = (page) => {
    currentSectionPage.value = page;
};

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

const ebooks = ref([]);

const getAllEbooks = (async () => {
    try {
        loading.value = true;
        await eBookStore.retrieveAllEBooks();
        loading.value = false;
        ebooks.value = eBookStore.allEBooks;
    }
    catch (error) {
        console.log(error);
    }
})

const currentEBookPage = ref(1);

const totalEBookPages = computed(() => Math.ceil(ebooks.value.length / cardsPerPage));

const eBookPagination = computed(() => {
    const start = (currentEBookPage.value - 1) * cardsPerPage;
    const end = start + cardsPerPage;
    return ebooks.value.slice(start, end);
});

const previousEBookPage = () => {
    if (currentEBookPage.value > 1) {
        currentEBookPage.value--;
    }
};

const nextEBookPage = () => {
    if (currentEBookPage.value < totalEBookPages.value) {
        currentEBookPage.value++;
    }
};

const goToEBookPage = (page) => {
    currentEBookPage.value = page;
};

function viewEBook(id) {
    router.push({ name: 'ViewEBook', params: { eBookId: id } });
}

const issuedBookStore = useIssuedBookStore();

const onBookRequest = (async (selectedEbook) => {
    try{

        if(selectedEbook.status == "Issued"){
            throw new Error("The book you are trying to request isn't available. Try again in few day !!")
        }
        const requesterDetails = {
            userId: localStorage.getItem('user_id'),
            username: localStorage.getItem('name')
        }
        const allRequested = ref([]);
        const alreadyRequested = ref([]);
        await issuedBookStore.retrieveAllIssuedBooks();
        
        alreadyRequested.value = issuedBookStore.allIssuedBooks.filter(ib => ib.status == "Requested" && ib.bookId == selectedEbook.id && ib.userId == requesterDetails.userId)

        if(alreadyRequested.value.length > 0){
            throw new Error("Already requested. Please wait for the book requested to be accepted !!")
        }

        allRequested.value = issuedBookStore.allIssuedBooks.filter(ib => ib.status == "Requested" && ib.userId == requesterDetails.userId);

        if(allRequested.value.length > 5){
            throw new Error("You cannot request more than 5 books at a time !!")
        }

        await issuedBookStore.requestBookDetails(selectedEbook.id, selectedEbook.title, requesterDetails);

        await getAllEbooks();

        setTimeout(() => {
            alertStore.success("E-Book requested successfully") 
        }, 200)
    }
    catch (error) {
        console.log(issuedBookStore.errorMessage);
        console.log(error.message);
        let message = "Book Request failed: ";
        if(issuedBookStore.errorMessage){
            message = message + issuedBookStore.errorMessage;
        }
        else{
            message = message + error.message;
        }
        alertStore.error(message);
    }
})

const deleteCurrentEBook = (async (id) => {
    try {
        await eBookStore.deleteEBook(id);
        await getAllEbooks();
        setTimeout(() => {
            alertStore.success("E-Book deleted successfully")
        }, 200)
    } catch (error) {
        console.log(eBookStore.errorMessage);
        let message = "E-Book Delete failed: " + eBookStore.errorMessage;
        alertStore.error(message);
    }
})

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}

.mySectionCont {
    min-height: 80dvh;
}

.myCard {
    min-height: 55dvh;
    max-height: 55dvh;
}

.mySectionCard {
    min-height: 35dvh;
    max-height: 35dvh;
}

table {
    width: 100%;
    border: 2px solid #000;
    border-collapse: collapse;
}

th, td {
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