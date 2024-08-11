<template>
    <div class="myModal-bg" v-if="isModalOpen">
        <div class="myModal" ref="modal">
            <button class="btn-close d-block ms-auto p-3" @click="closeModal"></button>
            <h3 class="text-primary ps-4">Search for User</h3>
            <div class="p-5 pt-2">
                <form @submit.prevent="onSearch" class="form" ref="mySearchForm">
                    <div class="mb-3">
                        <input type="text" id="search" class="form-control" name="search"
                            placeholder="Search for name or username" v-model="searchState.search" :class="{
                                'is-invalid': vSearch.search.$error,
                                'is-valid': !vSearch.search.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vSearch.search.$error">
                            {{ vSearch.search.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="d-grid gap-2 mt-4">
                        <button class="btn btn-outline-primary" type="submit" :disabled="vSearch.$invalid">
                            Search
                        </button>
                    </div>
                </form>
                <div class="mt-5" v-if="searchedResult && searchedResult.length > 0">
                    <h4 class="text-primary">Your search results: </h4>
                    <ol class="list-group list-group-numbered">
                        <li class="list-group-item d-flex justify-content-between align-items-start"
                            v-for="user in searchedResult" :key="user.id">
                            <div class="ms-2 me-auto">
                                <div class="fw-bold">{{ user.username }}</div>
                                {{ user.email }}
                            </div>
                            <button class="btn btn-primary btn-sm mt-2" @click="OnAssign(user)">Select</button>
                        </li>
                    </ol>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onClickOutside } from '@vueuse/core';
import { ref, defineEmits, reactive, computed } from 'vue';
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useUserStore } from '@/stores/userStore';

const isModalOpen = ref(true);
const modal = ref(null);
const emit = defineEmits(['close', 'submit']);
const userStore = useUserStore();
const searchedResult = ref([]);

onClickOutside(modal, () => {
    isModalOpen.value = false;
    emit('close')
}
)

function closeModal() {
    isModalOpen.value = !isModalOpen.value;
    emit('close');
}

const searchState = reactive({
    search: ref(null)
})

const searchRules = computed(() => {
    return {
        search: { required }
    }
})

const vSearch = useVuelidate(searchRules, searchState, {
    $autoDirty: true,
})

const onSearch = (async () => {
    await userStore.retrieveAllUsers();
    const searchtoLower = searchState.search.toLowerCase();
    searchedResult.value = userStore.allUsers.filter(u => u.username.toLowerCase().includes(searchtoLower) || u.firstName.toLowerCase().includes(searchtoLower));
    console.log(userStore.allUsers);
    console.log(searchedResult);
})

const OnAssign = ((userData)=>{
    emit('submit', userData);
})

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
    min-width: 100dvh;
    min-height: 40dvh;
    max-height: 80dvh;
    overflow-y: scroll;
}

.myLink {
    cursor: pointer;
}
</style>