<template>
    <div class="container-fluid">
        <div class="row p-5">
            <h1 class="text-warning">Welcome to Library Management System</h1>
            <h4 class="text-warning mt-2">Sign Up Today It's free !!!</h4>
            <p class="mt-4">Sign up to gain access to vast collection of eBooks. Rent upto 7 days for free.</p>
            <h1 class="text-warning mt-5 mb-3">Sign Up</h1>
            <div class="row p-5 myIndexCont border">
                <div class="col-md-4 col-lg-4 col-sm-12">
                    <img src="../assets/logo.png" alt="LOGO" class="img-thumbnail rounded" width="350px" height="350px">
                </div>
                <div class="col-md-6 offset-md-2 col-lg-6 offset-lg-2 col-sm-12">
                    <form @submit.prevent="onSignUp" class="form" ref="signUpForm">
                        <div class="mb-3">
                            <label for="firstName" class="form-label text-warning">First Name</label>
                            <input type="text" id="firstName" class="form-control" name="firstname" placeholder="Alex"
                                v-model="state.firstName"
                                :class="{ 'is-invalid': v$.firstName.$error, 'is-valid': !v$.firstName.$invalid }">
                            <div class="invalid-feedback" v-if="v$.firstName.$error">
                                {{ v$.firstName.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="lastName" class="form-label text-warning">Last Name</label>
                            <input type="text" id="lastName" class="form-control" name="lastname" placeholder="Merchant"
                                v-model="state.lastName"
                                :class="{ 'is-invalid': v$.lastName.$error, 'is-valid': !v$.lastName.$invalid }">
                            <div class="invalid-feedback" v-if="v$.lastName.$error">
                                {{ v$.lastName.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="username" class="form-label text-warning">Username</label>
                            <input type="text" id="username" class="form-control" name="username" placeholder="alexM12"
                                v-model="state.username"
                                :class="{ 'is-invalid': v$.username.$error, 'is-valid': !v$.username.$invalid }">
                            <div class="invalid-feedback" v-if="v$.username.$error">
                                {{ v$.username.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label text-warning">Email</label>
                            <input type="email" id="email" class="form-control" name="email"
                                placeholder="alexy@yahoo.com" v-model="state.email"
                                :class="{ 'is-invalid': v$.email.$error, 'is-valid': !v$.email.$invalid }">
                            <div class="invalid-feedback" v-if="v$.email.$error">
                                {{ v$.email.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label text-warning">Password</label>
                            <input type="password" id="password" class="form-control" name="password"
                                v-model="state.password.password"
                                :class="{ 'is-invalid': v$.password.password.$error, 'is-valid': !v$.password.password.$invalid }">
                            <div class="invalid-feedback" v-if="v$.password.password.$error">
                                {{ v$.password.password.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="confirmPassword" class="form-label text-warning">Confirm Password</label>
                            <input type="password" id="confirmPassword" class="form-control" name="confirmPassword"
                                v-model="state.password.confirm"
                                :class="{ 'is-invalid': v$.password.confirm.$error, 'is-valid': !v$.password.confirm.$invalid }">
                            <div class="invalid-feedback" v-if="v$.password.confirm.$error">
                                {{ v$.password.confirm.$errors[0].$message }}
                            </div>
                        </div>
                        <div class="d-grid gap-2 mt-4">
                            <button class="btn btn-outline-success" type="submit" :disabled="v$.$invalid">SignUp</button>
                        </div>
                    </form>
                    <div class="d-grid gap-2 mt-4">
                            <button class="btn btn-outline-info" type="reset" @click="clearForm">Reset</button>
                        </div>
                    <p class="text-secondary mt-5 fs-5">Back to <router-link to="/"
                            class="text-warning text-decoration-none">Login</router-link> </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAlertStore } from '@/stores/alertStore';
import { useUserStore } from '@/stores/userStore';
import useVuelidate from '@vuelidate/core';
import { required, email, alpha, alphaNum, minLength, sameAs } from '@vuelidate/validators';
import { computed, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const state = reactive({
    firstName: ref(null),
    lastName: ref(null),
    username: ref(null),
    email: ref(null),
    password: {
        password: ref(null),
        confirm: ref(null),
    },
})
const rules = computed(() => {
    return {
        firstName: { required, alpha },
        lastName: { required, alpha },
        username: { required, alphaNum },
        email: { required, email },
        password: {
            password: { required, minLenght: minLength(6) },
            confirm: { required, sameAs: sameAs(state.password.password) },
        },
    }
})
const v$ = useVuelidate(rules, state, {
    $autoDirty: true,
})

const clearForm = () => {
    state.firstName = ref(null),
    state.lastName = ref(null),
    state.username = ref(null),
    state.email = ref(null),
    state.password.password = ref(null),
    state.password.confirm = ref(null)
}

const onSignUp = async () => {
    const alertStore = useAlertStore();
    const userStore = useUserStore();
    try{
        await userStore.userRegistration(state);
        console.log(userStore.user);
        alertStore.success("User registered successfully");
        clearForm();
        setTimeout(()=>{
            router.push('/');
        }, 2500);
    }
    catch(error){
        console.log(userStore.errorMessage);
        let message = "Registration failed: " + userStore.errorMessage;
        alertStore.error(message);
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
::placeholder {
    color: #DBE975;
    opacity: 0.5;
    /* Firefox */
}

::-ms-input-placeholder {
    /* Edge 12 -18 */
    color: #DBE975;
}

.myIndexCont {
    border-radius: 50px;
}
</style>