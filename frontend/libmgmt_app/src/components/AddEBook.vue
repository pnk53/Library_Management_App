<template>
    <div class="myModal-bg" v-if="isModalOpen">
        <div class="myModal" ref="modal">
            <button class="btn-close d-block ms-auto p-3" @click="closeModal"></button>
            <h3 class="text-light ps-4">Add EBook</h3>
            <div class="p-5 pt-2">
                <form @submit.prevent="onEBookSubmit" class="form" ref="myForgotForm">
                    <div class="mb-3">
                        <label for="title" class="form-label text-light">Title: </label>
                        <input type="text" id="title" class="form-control" name="title" placeholder="Ikigai"
                            v-model="ebookState.title" :class="{
                                'is-invalid': vEbook.title.$error,
                                'is-valid': !vEbook.title.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.title.$error">
                            {{ vEbook.title.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="author" class="form-label text-light">Author: </label>
                        <input type="text" id="author" class="form-control" name="author" placeholder="Hector Garcia"
                            v-model="ebookState.author" :class="{
                                'is-invalid': vEbook.author.$error,
                                'is-valid': !vEbook.author.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.author.$error">
                            {{ vEbook.author.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="language" class="form-label text-light">Language: </label>
                        <input type="text" id="language" class="form-control" name="language" placeholder="English"
                            v-model="ebookState.language" :class="{
                                'is-invalid': vEbook.language.$error,
                                'is-valid': !vEbook.language.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.language.$error">
                            {{ vEbook.language.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="section" class="form-label text-light">Section: </label>
                        <Multiselect id="section" class="form-select mySelect" :searchable="false" :close-on-select="false"
                            :clear-on-select="false" placeholder="Select sections" :options="sectionsNames"
                            :multiple="true" name="section" v-model="ebookState.section" :class="{
                                'is-invalid': vEbook.section.$error,
                                'is-valid': !vEbook.section.$invalid,
                            }">
                        </Multiselect>
                        <div class="invalid-feedback" v-if="vEbook.section.$error">
                            {{ vEbook.section.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="date" class="form-label text-light">Release Date: </label>
                        <input type="date" id="date" class="form-control" name="date" v-model="ebookState.releaseDate"
                            :class="{
                                'is-invalid': vEbook.releaseDate.$error,
                                'is-valid': !vEbook.releaseDate.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vEbook.releaseDate.$error">
                            {{ vEbook.releaseDate.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="ebook" class="form-label text-light">EBook: </label>
                        <input type="file" id="ebook" class="form-control" accept=".epub" name="ebook" @change="onEBookUpload" :class="{
                            'is-invalid': vEbook.ebook.$error,
                            'is-valid': !vEbook.ebook.$invalid,
                        }" />
                        <div class="invalid-feedback" v-if="vEbook.ebook.$error">
                            {{ vEbook.ebook.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="d-grid gap-2 mt-4">
                        <button class="btn btn-outline-light" type="submit" :disabled="vEbook.$invalid">
                            Add EBook
                        </button>
                    </div>
                </form>
                <div class="d-grid gap-2 mt-2">
                    <button class="btn btn-outline-danger" @click="closeModal">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onClickOutside } from '@vueuse/core';
import { computed, reactive, ref, defineEmits, onMounted, onUnmounted } from 'vue';
import { required, alpha, helpers } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import { useAlertStore } from '@/stores/alertStore';
import { useSectionStore } from '@/stores/sectionStore';
import { useEBookStore } from '@/stores/ebookStore';
import { Multiselect } from 'vue-multiselect';

const isModalOpen = ref(true)
const modal = ref(null)
const emit = defineEmits(['close'])

onClickOutside(modal, () => {
    isModalOpen.value = false;
    emit('close');
}
)

function closeModal() {
    isModalOpen.value = !isModalOpen.value;
    emit('close');
}

const alertStore = useAlertStore();
const sectionStore = useSectionStore();
const eBookStore = useEBookStore();

const ebookState = reactive({
    title: ref(null),
    author: ref(null),
    language: ref(null),
    releaseDate: ref(null),
    section: ref([]),
    ebook: ref(null)
})

const isEPubFile = ((file)=>{
    if(!file){
        return true;
    }
    const fileType = file.name.split('.').pop().toLowerCase();
    return fileType === 'epub';
})

const ebookRules = computed(() => {
    return {
        title: { required },
        author: { required },
        language: { required, alpha },
        releaseDate: { required },
        section: { required },
        ebook: { required, isEPubFile: helpers.withMessage('Please upload .epub file', isEPubFile) },
    }
})

const onEBookUpload = ((event) => {
    ebookState.ebook = event.target.files[0];
    console.log(ebookState.ebook);
})

const vEbook = useVuelidate(ebookRules, ebookState, {
    $autoDirty: true,
})

const sectionsNames = ref([]);

onMounted(async () => {
    await sectionStore.getAllSectionNames();
    sectionsNames.value = sectionStore.allSectionNames;
})

onUnmounted(() => {
    sectionsNames.value = null
})

const onEBookSubmit = async () => {
    try {
        await eBookStore.addEBook(ebookState);
        console.log(eBookStore.eBook);
        isModalOpen.value = false;
        emit('close');
        setTimeout(() => {
            alertStore.success("EBook added successfully")
        }, 200)
    }
    catch (error) {
        console.log(eBookStore.errorMessage);
        let message = "EBook Registration failed: " + eBookStore.errorMessage;
        alertStore.error(message);
        console.log(error);
    }
}

</script>

<style scoped>
.myModal-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(225, 255, 255, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
}

.myModal {
    position: relative;
    background-color: #212529;
    border-radius: 15px;
    min-width: 80dvh;
    min-height: 10dvh;
    max-height: 90dvh;
    overflow-y: scroll;
}

.myLink {
    cursor: pointer;
}
</style>