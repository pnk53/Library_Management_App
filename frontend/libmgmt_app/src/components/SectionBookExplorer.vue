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
        <div class="row">
            <div v-if="searchResults">
                <h2>Your search result: {{ searchResults }}</h2>
            </div>
        </div>
        <div class="border border-3 border-info rounded m-5 p-3 mySectionCont d-flex flex-column">
            <div class="d-flex mb-2">
                <h2 class="text-info">Sections</h2>
                <button class="btn btn-outline-info ms-auto" :hidden="!isAdmin" @click="loadSectionComponent">Add Section</button>
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
                        <div class="card bg-info bg-gradient mt-2 mb-2 myCard">
                            <div class="card-header">
                                <h5 class="text-dark">{{ section.name }}</h5>
                            </div>
                            <div class="card-body">
                                <p class="card-title text-dark mb-3">{{ section.rating }}</p>
                                <p class="text-dark">{{ section.description }}</p>
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
            <h2 class="text-light">EBooks</h2>
            <div class="d-flex justify-content-center" v-if="loading">
                <div class="spinner-border text-light m-5" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <transition name="fade" mode="out-in" v-else>
                <div class="row" :key="currentEBookPage">
                    <div class="col-lg-3 offset-lg-0 col-md-3 offset-md-0 col-sm-10 offset-sm-1"
                        v-for="ebook in eBookPagination" :key="ebook.name">
                        <div class="card bg-light bg-gradient mt-2 mb-2">
                            <div class="card-header">
                                <h5 class="text-dark">{{ ebook.name }}</h5>
                            </div>
                            <div class="card-body">
                                <p class="card-title text-dark mb-3">{{ ebook.rating }}</p>
                                <p class="text-dark">{{ ebook.description }}</p>
                                <div class="d-flex justify-content-between">
                                    <button class="btn btn-dark">View</button>
                                    <button class="btn btn-danger" v-if="isAdmin">Delete</button>
                                </div>
                            </div>
                        </div>
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
import useVuelidate from '@vuelidate/core';
import { required, alpha } from '@vuelidate/validators';
import { computed, reactive, ref, onMounted, shallowRef, defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';

const loading = ref(false)
const sectionStore = useSectionStore();
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
        search: { required, alpha }
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

onMounted(async () => {
    await getAllSections();
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

const ebooks = ref([
    { name: 'EBook 1', description: 'Description 1', rating: 4.5 },
    { name: 'EBook 2', description: 'Description 2', rating: 4.0 },
    { name: 'EBook 3', description: 'Description 3', rating: 3.5 },
    { name: 'EBook 4', description: 'Description 4', rating: 5.0 },
    { name: 'EBook 5', description: 'Description 5', rating: 4.2 },
    { name: 'EBook 6', description: 'Description 6', rating: 3.8 },
    { name: 'EBook 7', description: 'Description 7', rating: 4.7 },
    { name: 'EBook 8', description: 'Description 8', rating: 3.9 },
    { name: 'EBook 9', description: 'Description 9', rating: 4.3 },
    { name: 'EBook 10', description: 'Description 10', rating: 4.6 }
]);

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
    min-height: 40dvh;
}
</style>