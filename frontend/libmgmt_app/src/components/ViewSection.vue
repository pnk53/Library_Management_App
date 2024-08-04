<template>
    <div class="container-fluid">
        <div class="row p-3">
            <div class="bg-info bg=gradient rounded p-3 mt-4">
                <div class="col-md-4 col-lg-4 col-sm-12 bg-dark p-5 rounded">
                    <div class="d-flex">
                        <h2>Section Details</h2>
                        <a class="text-white ms-auto myLink" @click="editSection" :hidden="!isAdmin">
                            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor"
                                class="bi bi-pencil-square" viewBox="0 0 16 16">
                                <path
                                    d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                                <path fill-rule="evenodd"
                                    d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z" />
                            </svg>
                        </a>
                    </div>
                    <form @submit.prevent="onSectionUpdate" class="form" ref="mySectionForm">
                        <div class="mb-3">
                            <label for="name" class="form-label text-info">Name: </label>
                            <input type="text" id="name" class="form-control" name="name" placeholder="Science Fiction"
                                :disabled="isDisabled" v-model="sectionState.name" :class="{
                                    'is-invalid': vSection.name.$error
                                }" />
                            <div class="invalid-feedback" v-if="vSection.name.$error">
                                {{ vSection.name.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="date" class="form-label text-info">Date Created: </label>
                            <input type="date" id="date" class="form-control" name="date"
                                v-model="sectionState.dateCreated" :disabled="isDisabled" :class="{
                                    'is-invalid': vSection.dateCreated.$error
                                }" />
                            <div class="invalid-feedback" v-if="vSection.dateCreated.$error">
                                {{ vSection.dateCreated.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label text-info">Description: </label>
                            <input type="text" id="description" class="form-control" name="description"
                                :disabled="isDisabled" placeholder="Add description" style="min-height: 10dvh;"
                                v-model="sectionState.description" :class="{
                                    'is-invalid': vSection.description.$error
                                }" />
                            <div class="invalid-feedback" v-if="vSection.description.$error">
                                {{ vSection.description.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="d-grid gap-2 mt-4">
                            <button class="btn btn-outline-info" type="submit"
                                :disabled="isDisabled || vSection.$invalid" :hidden="!isAdmin">
                                Update Section
                            </button>
                        </div>
                    </form>
                    <div class="d-grid gap-2 mt-2">
                        <button class="btn btn-outline-danger" :disabled="isDisabled" @click="deleteCurrentSection" :hidden="!isAdmin">
                            Delete Section
                        </button>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
import { useSectionStore } from '@/stores/sectionStore';
import { onMounted, ref, computed, reactive, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useAlertStore } from '@/stores/alertStore';

const selectedSec = ref({});
const sectionStore = useSectionStore();
const route = useRoute();
const isDisabled = ref(true);
const router = useRouter();
const alertStore = useAlertStore();

function editSection() {
    isDisabled.value = !isDisabled.value;
}

const isAdmin = computed(() => {
    if (localStorage.getItem('userType') == 'Librarian'){
        return true;
    }
    else{
        return false;
    }
})

onMounted(async () => {
    try {
        await sectionStore.currentSection(route.params.sectionId);
        selectedSec.value = sectionStore.selectedSection;
    }
    catch (error) {
        console.log(error);
    }
})

const sectionState = reactive({
    name: ref(null),
    dateCreated: ref(null),
    description: ref(null)
})

watchEffect(() => {
    sectionState.name = selectedSec.value.name || null;
    sectionState.dateCreated = selectedSec.value.dateCreated || null;
    sectionState.description = selectedSec.value.description || null;
})

const sectionRules = computed(() => {
    return {
        name: { required },
        dateCreated: { required },
        description: { required }
    }
})

const vSection = useVuelidate(sectionRules, sectionState)

const onSectionUpdate = async () => {
    const alertStore = useAlertStore();
    try {
        await sectionStore.updateSection(route.params.sectionId, sectionState);
        isDisabled.value = true;
        setTimeout(() => {
            alertStore.success("Section updated successfully")
        }, 200)
    }
    catch (error) {
        console.log(sectionStore.errorMessage);
        let message = "Section Update failed: " + sectionStore.errorMessage;
        alertStore.error(message);
    }
}

const deleteCurrentSection = (async () => {
    try{
        await sectionStore.deleteSection(route.params.sectionId);
        router.push('/librarianHome');
        setTimeout(() => {
            alertStore.success("Section deleted successfully")
        }, 200)
    }catch (error) {
        console.log(sectionStore.errorMessage);
        let message = "Section Delete failed: " + sectionStore.errorMessage;
        alertStore.error(message);
    }
})

</script>

<style scoped>
.myLink {
    cursor: pointer;
}
</style>