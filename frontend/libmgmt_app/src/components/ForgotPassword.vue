<template>
    <div class="myModal-bg" v-if="isModalOpen">
        <div class="myModal" ref="modal">
            <button class="btn-primary btn-close d-block ms-auto p-3" @click="isModalOpen = false"></button>
            <h3 class="text-warning ps-4">Reset your password</h3>
            <div class="p-5 pt-2">
                <form @submit.prevent="forgot" class="form" ref="myForgotForm">
                    <div class="mb-3">
                        <label for="email" class="form-label text-warning">Enter your email: </label>
                        <input type="email" id="email" class="form-control" name="email" placeholder="asd@gmail.com"
                            v-model="forgotState.email" :class="{
                                'is-invalid': vForgot.email.$error,
                                'is-valid': !vForgot.email.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="vForgot.email.$error">
                            {{ vForgot.email.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="d-grid gap-2 mt-4">
                        <button class="btn btn-outline-success" type="submit" :disabled="vForgot.$invalid">
                            Submit
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onClickOutside } from '@vueuse/core';
import { computed, reactive, ref } from 'vue';
import { required, email } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'

const isModalOpen = ref(true)
const modal = ref(null)
onClickOutside(modal, () => (isModalOpen.value = false))

const forgotState = reactive({
    email: ref(null)
})

const forgotRules = computed(() => {
    return {
        email: { required, email }
    }
})

const vForgot = useVuelidate(forgotRules, forgotState, {
    $autoDirty: true,
})


const forgot = () => {
    alert(forgotState.email);
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