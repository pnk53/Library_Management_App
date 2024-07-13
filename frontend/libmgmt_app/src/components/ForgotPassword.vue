<template>
    <a class="text-warning text-decoration-none myLink" @click="isModalOpen = true">Reset password</a>
    <div class="myModal-bg" v-if="isModalOpen">
        <div class="myModal" ref="modal">
            <button class="btn-primary btn-close d-block ms-auto p-3" @click="isModalOpen = false"></button>
            <h3 class="text-warning ps-4">Reset your password</h3>
            <div class="p-5 pt-2">
                <form @submit.prevent="forgot" class="form" ref="myForgotForm">
                    <div class="mb-3">
                        <label for="email" class="form-label text-warning">Enter your email: </label>
                        <input type="email" id="email" class="form-control" name="email" placeholder="asd@gmail.com"
                            v-model="state.email" :class="{
                                'is-invalid': v$.email.$error,
                                'is-valid': !v$.email.$invalid,
                            }" />
                        <div class="invalid-feedback" v-if="v$.email.$error">
                            {{ v$.email.$errors[0].$message }}
                        </div>
                    </div>
                    <div class="d-grid gap-2 mt-4">
                        <button class="btn btn-outline-success" type="submit" :disabled="v$.$invalid">
                            Submit
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { onClickOutside } from '@vueuse/core';
import { computed, reactive, ref } from 'vue';
import { required, email } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'

export default {
    name: 'ForgotPassword',
    setup() {
        const isModalOpen = ref(false)
        const modal = ref(null)
        onClickOutside(modal, () => (isModalOpen.value = false))

        const state = reactive({
            email: ref(null)
        });

        const rules = computed(() => {
            return {
                email: { required, email }
            }
        });

        const v$ = useVuelidate(rules, state, {
            $autoDirty: true,
        });

        return {
            isModalOpen,
            modal,
            state,
            v$
        }
    },
    methods: {
        forgot() {
            this.v$.$validate();
            if (!this.v$.$error) {
                this.$refs.myForgotForm.reset();
            } else {
                alert("Failed");
            }
        }
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