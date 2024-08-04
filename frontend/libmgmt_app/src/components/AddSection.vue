<template>
    <div class="myModal-bg" v-if="isModalOpen">
        <div class="myModal" ref="modal">
            <button class="btn-close d-block ms-auto p-3" @click="closeModal"></button>
            <h3 class="text-info ps-4">Add Section</h3>
            <div class="p-5 pt-2">
                <form @submit.prevent="onSectionSubmit" class="form" ref="mySectionForm">
                    <div class="mb-3">
                        <label for="name" class="form-label text-info">Name: </label>
                        <input type="text" id="name" class="form-control" name="name" placeholder="Science Fiction"
                            v-model="sectionState.name" :class="{
                                'is-invalid': vSection.name.$error,
                                'is-valid': !vSection.name.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vSection.name.$error">
                            {{ vSection.name.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="date" class="form-label text-info">Date Created: </label>
                        <input type="date" id="date" class="form-control" name="date" v-model="sectionState.dateCreated"
                            :class="{
                                'is-invalid': vSection.dateCreated.$error,
                                'is-valid': !vSection.dateCreated.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vSection.dateCreated.$error">
                            {{ vSection.dateCreated.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="description" class="form-label text-info">Description: </label>
                        <input type="text" id="description" class="form-control" name="description"
                            placeholder="Add description" v-model="sectionState.description" :class="{
                                'is-invalid': vSection.description.$error,
                                'is-valid': !vSection.description.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vSection.description.$error">
                            {{ vSection.description.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="d-grid gap-2 mt-4">
                        <button class="btn btn-outline-info" type="submit" :disabled="vSection.$invalid">
                            Add Section
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
import { computed, reactive, ref, defineEmits } from 'vue';
import { required } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import { useAlertStore } from '@/stores/alertStore';
import { useSectionStore } from '@/stores/sectionStore';

const isModalOpen = ref(true)
const modal = ref(null)
const emit = defineEmits(['close'])

onClickOutside(modal, () => {
    isModalOpen.value = false;
    emit('close')
}
)

function closeModal() {
    isModalOpen.value = !isModalOpen.value;
    emit('close');
}

const sectionState = reactive({
    name: ref(null),
    dateCreated: ref(null),
    description: ref(null)
})

const sectionRules = computed(() => {
    return {
        name: { required },
        dateCreated: { required },
        description: { required }
    }
})

const vSection = useVuelidate(sectionRules, sectionState, {
    $autoDirty: true,
})


const onSectionSubmit = async () => {
    const alertStore = useAlertStore();
    const sectionStore = useSectionStore();
    try {
        await sectionStore.sectionRegistration(sectionState);
        console.log(sectionStore.section);
        isModalOpen.value = false;
        emit('close');
        setTimeout(() => {
            alertStore.success("Section added successfully")
        }, 200)
    }
    catch (error) {
        console.log(sectionStore.errorMessage);
        let message = "Section Registration failed: " + sectionStore.errorMessage;
        alertStore.error(message);
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
}

.myLink {
    cursor: pointer;
}
</style>