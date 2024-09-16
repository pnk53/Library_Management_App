<template>
    <div class="container-fluid">
        <div class="row p-5">
            <div class="col-md-6 offset-md-3 col-lg-6 offset-lg-3 col-sm-12 border border-warning rounded p-5">
        <div class="d-flex">
            <h3 class="text-white">Profile Details</h3>
            <a class="text-white ms-auto myLink" @click="editUser">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor"
                    class="bi bi-pencil-square" viewBox="0 0 16 16">
                    <path
                        d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                    <path fill-rule="evenodd"
                        d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z" />
                </svg>
            </a>
        </div>
        <form @submit.prevent="onUpdateUser" class="form" ref="updateForm">
            <div class="mb-3">
                <label for="firstName" class="form-label text-warning">First Name</label>
                <input type="text" id="firstName" class="form-control" name="firstname" placeholder="Alex"
                    v-model="updateUserState.firstName" :disabled="isDisabled" :class="{ 'is-invalid': vUpdateUser.firstName.$error }">
                <div class="invalid-feedback" v-if="vUpdateUser.firstName.$error">
                    {{ vUpdateUser.firstName.$errors[0].$message }}
                </div>
            </div>
            <div class="mb-3">
                <label for="lastName" class="form-label text-warning">Last Name</label>
                <input type="text" id="lastName" class="form-control" name="lastname" placeholder="Merchant"
                    v-model="updateUserState.lastName" :disabled="isDisabled" :class="{ 'is-invalid': vUpdateUser.lastName.$error }">
                <div class="invalid-feedback" v-if="vUpdateUser.lastName.$error">
                    {{ vUpdateUser.lastName.$errors[0].$message }}
                </div>
            </div>
            <div class="mb-3">
                <label for="username" class="form-label text-warning">Username</label>
                <input type="text" id="username" class="form-control" name="username" placeholder="alexM12"
                    v-model="updateUserState.username" :disabled="isDisabled" :class="{ 'is-invalid': vUpdateUser.username.$error }">
                <div class="invalid-feedback" v-if="vUpdateUser.username.$error">
                    {{ vUpdateUser.username.$errors[0].$message }}
                </div>
            </div>
            <div class="mb-3">
                <label for="email" class="form-label text-warning">Email</label>
                <input type="email" id="email" class="form-control" name="email" placeholder="alexy@yahoo.com"
                    v-model="updateUserState.email" :disabled="isDisabled" :class="{ 'is-invalid': vUpdateUser.email.$error }">
                <div class="invalid-feedback" v-if="vUpdateUser.email.$error">
                    {{ vUpdateUser.email.$errors[0].$message }}
                </div>
            </div>
            <div class="d-grid gap-2 mt-4">
                <button class="btn btn-outline-success" type="submit" :disabled="isDisabled || vUpdateUser.$invalid">Update</button>
            </div>
        </form>
    </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watchEffect } from 'vue';
import { useAlertStore } from '@/stores/alertStore';
import { useUserStore } from '@/stores/userStore';
import useVuelidate from '@vuelidate/core';
import { required, email, alpha, alphaNum } from '@vuelidate/validators';

const userStore = useUserStore();
const alertStore = useAlertStore();
const currentUser = ref({});
const isDisabled = ref(true);

onMounted(async () => {
    await userStore.currentUser(localStorage.getItem('user_id'));
    currentUser.value = userStore.selectedUser;
})

const editUser = (()=>{
    isDisabled.value = !isDisabled.value;
})

const updateUserState = reactive({
    firstName: ref(null),
    lastName: ref(null),
    username: ref(null),
    email: ref(null),
})
const updateUserRules = computed(() => {
    return {
        firstName: { required, alpha },
        lastName: { required, alpha },
        username: { required, alphaNum },
        email: { required, email },
    }
})
watchEffect(() => {
    updateUserState.firstName = currentUser.value.firstName || null;
    updateUserState.lastName = currentUser.value.lastName || null;
    updateUserState.username = currentUser.value.username || null;
    updateUserState.email = currentUser.value.email || null;
})
const vUpdateUser = useVuelidate(updateUserRules, updateUserState, {
    $autoDirty: true,
})

const onUpdateUser = (async () => {
    try{
        await userStore.userUpdate(localStorage.getItem('user_id'), updateUserState);
        isDisabled.value = !isDisabled.value;
        setTimeout(() => {
            alertStore.success("User details updated successfully");
        }, 200);
    }
    catch (error) {
        console.log(userStore.errorMessage);
        let message = "User Update failed: " + userStore.errorMessage;
        alertStore.error(message);
    }
})

</script>

<style scoped>
.myLink{
    cursor: pointer;
}
</style>