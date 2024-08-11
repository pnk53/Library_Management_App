<template>
    <div class="container-fluid">
        <div class="row d-flex bg-success bg-gradient rounded p-3 m-3 mt-4 pb-4" v-if="isAdmin">
            <h3 class="text-dark">Issue Book to user</h3>
            <form @submit.prevent="onAssign" class="form row col-md-9 col-lg-9 mt-3">
                <div class="mb-3 col-md-4 col-lg-4">
                    <input type="number" id="userId" class="form-control" name="userId"
                        placeholder="Use 'User Lookup' to find User" v-model="ebookAssignState.userId" disabled :class="{
                            'is-invalid': vEbookAssign.userId.$error
                        }" />
                    <div class="invalid-feedback" v-if="vEbookAssign.userId.$error">
                        {{ vEbookAssign.userId.$errors[0].$message }}
                    </div>
                </div>
                <div class="mb-3 col-md-4 col-lg-4">
                    <input type="text" id="username" class="form-control" name="username" v-model="ebookAssignState.username" disabled :class="{
                            'is-invalid': vEbookAssign.username.$error
                        }" />
                    <div class="invalid-feedback" v-if="vEbookAssign.username.$error">
                        {{ vEbookAssign.username.$errors[0].$message }}
                    </div>
                </div>
                <div class="col-md-3 col-lg-3">
                    <button class="btn btn-light ps-5 pe-5" type="submit" :hidden="!isAdmin"
                        :disabled="vEbookAssign.$invalid">
                        Assign
                    </button>
                </div>
            </form>
            <div class="col-md-3 col-lg-3 ms-auto mt-3">
                <button class="btn btn-primary ps-5 pe-5" type="button" @click="loadSearchComponent" :hidden="!isAdmin">
                    User Lookup
                </button>
                <component :is="searchModal" v-if="isSearchModalLoaded" @close="unloadSearchComponent"
                    @submit="populateUser">
                </component>
            </div>
        </div>
        <div class="row bg-light bg-gradient rounded p-3 m-3 mt-4 pb-5">
            <div class="col-md-7 col-lg-7 col-sm-12">
                <h3 class="text-dark mb-3">Read Book</h3>
                <div class="myBookCont rounded" v-if="isBookIssuedToCurrentUser">
                    <vue-reader v-if="url" :url="url" />
                </div>
                <div class="mt-5" v-else>
                    <h2 class="text-black">
                        Please request the book to read it !!
                    </h2>
                </div>
            </div>
            <div class="col-md-5 col-lg-5 col-sm-12 bg-dark rounded p-4 mt-5">
                <div class="d-flex">
                    <h2>Book Details</h2>
                    <a class="text-white ms-auto myLink" @click="editEBook" :hidden="!isAdmin">
                        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor"
                            class="bi bi-pencil-square" viewBox="0 0 16 16">
                            <path
                                d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                            <path fill-rule="evenodd"
                                d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z" />
                        </svg>
                    </a>
                    <button class="btn btn-light ms-auto ps-4 pe-4" :hidden="isAdmin" @click="editEBook">Rate</button>
                </div>
                <form @submit.prevent="handleSubmit" class="form" ref="myEBookForm">
                    <div class="mb-3">
                        <label for="title" class="form-label text-light">Title: </label>
                        <input type="text" id="title" class="form-control" name="title" placeholder="Ikigai"
                            v-model="ebookState.title" :disabled="isDisabled || !isAdmin" :class="{
                                'is-invalid': vEbook.title.$error
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.title.$error">
                            {{ vEbook.title.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="author" class="form-label text-light">Author: </label>
                        <input type="text" id="author" class="form-control" name="author" placeholder="Hector Garcia"
                            v-model="ebookState.author" :disabled="isDisabled || !isAdmin" :class="{
                                'is-invalid': vEbook.author.$error
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.author.$error">
                            {{ vEbook.author.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="language" class="form-label text-light">Language: </label>
                        <input type="text" id="language" class="form-control" name="language" placeholder="English"
                            v-model="ebookState.language" :disabled="isDisabled || !isAdmin" :class="{
                                'is-invalid': vEbook.language.$error
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.language.$error">
                            {{ vEbook.language.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="section" class="form-label text-light">Section: </label>
                        <Multiselect id="section" class="form-select mySelect" :searchable="false"
                            :close-on-select="true" :clear-on-select="false" placeholder="Select sections"
                            :disabled="isDisabled || !isAdmin" :options="sectionsNames" :multiple="true" name="section"
                            v-model="ebookState.section" :class="{
                                'is-invalid': vEbook.section.$error
                            }">
                        </Multiselect>
                        <div class="invalid-feedback" v-if="vEbook.section.$error">
                            {{ vEbook.section.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="date" class="form-label text-light">Release Date: </label>
                        <input type="date" id="date" class="form-control" name="date" v-model="ebookState.releaseDate"
                            :disabled="isDisabled || !isAdmin" :class="{
                                'is-invalid': vEbook.releaseDate.$error
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.releaseDate.$error">
                            {{ vEbook.releaseDate.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="date" class="form-label text-light">Status: </label>
                        <input type="text" id="status" class="form-control" name="status" v-model="ebookState.status"
                            :disabled="isDisabled || !isAdmin" :class="{
                                'is-invalid': vEbook.status.$error
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.status.$error">
                            {{ vEbook.status.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="date" class="form-label text-light">Rating: </label>
                        <input type="number" min="0" max="10" id="rating" class="form-control" name="rating"
                            v-model="ebookState.rating" :disabled="isDisabled || isAdmin" :class="{
                                'is-invalid': vEbook.rating.$error
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.rating.$error">
                            {{ vEbook.rating.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="d-grid gap-2 mt-4">
                        <button class="btn btn-outline-light" type="submit" :hidden="!isAdmin"
                            :disabled="isDisabled || vEbook.$invalid">
                            Update E-Book
                        </button>
                        <button class="btn btn-outline-light" type="submit" :hidden="isAdmin"
                            :disabled="isDisabled || vEbook.$invalid">
                            Rate E-Book
                        </button>
                    </div>
                </form>
                <div class="d-grid gap-2 mt-2">
                    <button class="btn btn-outline-danger" :disabled="isDisabled" @click="deleteCurrentEBook"
                        :hidden="!isAdmin">
                        Delete E-Book
                    </button>
                    <button class="btn btn-outline-warning" :disabled="selectedEbook.status !== 'Issued'" @click="revokeBook(selectedEbook.id)"
                        :hidden="!isAdmin">
                        Revoke E-Book
                    </button>
                    <button class="btn btn-outline-success" :hidden="isBookIssuedToCurrentUser" @click="onBookRequest">
                        Request E-Book
                    </button>
                    <button class="btn btn-outline-warning" v-if="isBookIssuedToCurrentUser && !isAdmin"  @click="revokeBook(selectedEbook.id)">
                        Return E-Book
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { VueReader } from 'vue-reader';
import { useEBookStore } from '@/stores/ebookStore';
import { ref, shallowRef, onMounted, reactive, computed, watchEffect, defineAsyncComponent } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { required, alpha, integer, minValue, maxValue, alphaNum } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { Multiselect } from 'vue-multiselect';
import { useSectionStore } from '@/stores/sectionStore';
import { useAlertStore } from '@/stores/alertStore';
import { useIssuedBookStore } from '@/stores/issuedBookStore';

const eBookStore = useEBookStore();
const sectionStore = useSectionStore();
const alertStore = useAlertStore();
const issuedBookStore = useIssuedBookStore();
const selectedEbook = ref({});
const route = useRoute();
const router = useRouter();
const isDisabled = ref(true);
const sectionsNames = ref([]);
const url = ref(null);
const searchModal = shallowRef(null)
const isSearchModalLoaded = shallowRef(false)

const isAdmin = computed(() => {
    if (localStorage.getItem('userType') == 'Librarian') {
        return true;
    }
    else {
        return false;
    }
})

function loadSearchComponent() {
    isSearchModalLoaded.value = true;
    searchModal.value = defineAsyncComponent(() => import("../components/AssignBook.vue"))
}

async function unloadSearchComponent() {
    isSearchModalLoaded.value = false;
    searchModal.value = null;
}

const ebookState = reactive({
    title: ref(null),
    author: ref(null),
    language: ref(null),
    releaseDate: ref(null),
    section: ref([]),
    status: ref(null),
    rating: ref(null)
})

watchEffect(() => {
    ebookState.title = selectedEbook.value.title || null;
    ebookState.author = selectedEbook.value.author || null;
    ebookState.language = selectedEbook.value.language || null;
    ebookState.releaseDate = selectedEbook.value.releaseDate || null;
    ebookState.section = selectedEbook.value.section || null;
    ebookState.status = selectedEbook.value.status || null;
    ebookState.rating = selectedEbook.value.rating || null;
})

const ebookRules = computed(() => {
    return {
        title: { required },
        author: { required },
        language: { required, alpha },
        releaseDate: { required },
        section: { required },
        status: { required },
        rating: { integer, minValue: minValue(1), maxValue: maxValue(10) }
    }
})

const vEbook = useVuelidate(ebookRules, ebookState, {
    $autoDirty: true,
})

const populateUser = ((user) => {
    ebookAssignState.userId = user.id;
    ebookAssignState.username = user.username;
    unloadSearchComponent();
})

const ebookAssignState = reactive({
    userId: ref(null),
    username: ref(null)
})

const ebookAssignRules = computed(() => {
    return {
        userId: { required, integer },
        username: { required, alphaNum }
    }
})

const vEbookAssign = useVuelidate(ebookAssignRules, ebookAssignState, {
    $autoDirty: true,
})

const onAssign = (async () => {
    try{
        if(selectedEbook.value.status == "Issued"){
            throw new Error("The book you are trying to assign isn't available !!")
        }

        await issuedBookStore.registerIssuedBook(route.params.eBookId, selectedEbook.value.title, ebookAssignState);

        await eBookStore.updateAssignedBookInfo(route.params.eBookId, ebookAssignState);

        await loadSelectedBook();
        setTimeout(() => {
            alertStore.success("Book issued successfully")
        }, 200)
    }
    catch (error) {
        console.log(issuedBookStore.errorMessage);
        console.log(error.message);
        let message = "Book Assign failed: ";
        if(issuedBookStore.errorMessage){
            message = message + issuedBookStore.errorMessage;
        }
        else{
            message = message + error.message;
        }
        alertStore.error(message);
    }
})

const loadSelectedBook = (async ()=>{
    try {
        await eBookStore.currentEBook(route.params.eBookId);
        selectedEbook.value = eBookStore.selectedEbook;

        url.value = selectedEbook.value.contentPath;

        await sectionStore.getAllSectionNames();
        sectionsNames.value = sectionStore.allSectionNames;
    }
    catch (error) {
        console.log(error);
    }
})

onMounted(async () => {
    await loadSelectedBook();
})

const isBookIssuedToCurrentUser = computed(()=>{
    if(selectedEbook.value.currentIssuer == localStorage.getItem('user_id') && selectedEbook.value.status == "Issued"){
        return true;
    }
    else if(isAdmin.value){
        return true;
    }
    else{
        return false;
    }
})

const editEBook = (() => {
    isDisabled.value = !isDisabled.value;
})

const onEBookUpdate = async () => {
    try {
        let totalRater = selectedEbook.value.totalRater
        await eBookStore.updateEBook(route.params.eBookId, ebookState, totalRater);
        isDisabled.value = true;
        await loadSelectedBook();
        setTimeout(() => {
            alertStore.success("E-Book updated successfully")
        }, 200)
    }
    catch (error) {
        console.log(eBookStore.errorMessage);
        let message = "E-Book Update failed: " + eBookStore.errorMessage;
        alertStore.error(message);
    }
}

const onEBookRate = (async() => {
    try {
        await eBookStore.currentEBook(route.params.eBookId);
        selectedEbook.value = eBookStore.selectedEbook;
        let totalRater = selectedEbook.value.totalRater + 1;
        let finalOverallRating = parseInt(Math.round(((selectedEbook.value.rating * (totalRater-1)) + ebookState.rating) / totalRater))
        console.log(finalOverallRating)
        ebookState.rating = finalOverallRating.value;
        await eBookStore.updateEBook(route.params.eBookId, ebookState, totalRater);
        isDisabled.value = true;
        setTimeout(() => {
            alertStore.success("E-Book rated successfully")
        }, 200)
    }
    catch (error) {
        console.log(eBookStore.errorMessage);
        let message = "E-Book rating failed: " + eBookStore.errorMessage;
        alertStore.error(message);
    }
})

const handleSubmit = (() => {
    if(isAdmin.value == true){
        onEBookUpdate();
    }
    else{
        onEBookRate();
    }
})

const onBookRequest = (async () => {
    try{

        if(selectedEbook.value.status == "Issued"){
            throw new Error("The book you are trying to request isn't available. Try again in few day !!")
        }
        const requesterDetails = {
            userId: localStorage.getItem('user_id'),
            username: localStorage.getItem('name')
        }
        const allRequested = ref([]);
        const alreadyRequested = ref([]);
        await issuedBookStore.retrieveAllIssuedBooks();
        
        alreadyRequested.value = issuedBookStore.allIssuedBooks.filter(ib => ib.status == "Requested" && ib.bookId == route.params.eBookId && ib.userId == requesterDetails.userId)

        if(alreadyRequested.value.length > 0){
            throw new Error("Already requested. Please wait for the book requested to be accepted !!")
        }

        allRequested.value = issuedBookStore.allIssuedBooks.filter(ib => ib.status == "Requested" && ib.userId == requesterDetails.userId);

        if(allRequested.value.length > 5){
            throw new Error("You cannot request more than 5 books at a time !!")
        }

        await issuedBookStore.requestBookDetails(route.params.eBookId, selectedEbook.value.title, requesterDetails);

        await loadSelectedBook();
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

const revokeBook = (async (id) => {
    try {
        await issuedBookStore.retrieveAllIssuedBooks();
        const selectedRevokeBook = ref([])
        selectedRevokeBook.value = issuedBookStore.allIssuedBooks.filter(ib => ib.bookId == selectedEbook.value.id && ib.status == "Ongoing");
        
        await issuedBookStore.revokeBookRequest(selectedRevokeBook.value[0].id);
        
        await eBookStore.updateRevokedBookInfo(id);
        
        await loadSelectedBook();
        setTimeout(() => {
            alertStore.success("E-Book revoked successfully")
        }, 200)
    }
    catch (error) {
        console.log(eBookStore.errorMessage);
        let message = "E-Book revoked failed: " + eBookStore.errorMessage;
        alertStore.error(message);
    }
})

const deleteCurrentEBook = (async () => {
    try {
        await eBookStore.deleteEBook(route.params.eBookId);
        router.push('/explorer');
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
.myLink {
    cursor: pointer;
}

.myBookCont {
    height: 100dvh;
    box-shadow: 10px 10px 20px #000;
}
</style>