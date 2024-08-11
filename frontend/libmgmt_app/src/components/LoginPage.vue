<template>
  <div class="container-fluid">
    <div class="row p-3">
      <div class="myCarousel">
        <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-indicators">
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0"
              class="active bg-warning" aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"
              class="bg-warning"></button>
          </div>
          <div class="carousel-inner">
            <div class="carousel-item active">
              <img src="../assets/poster1.jpg" class="d-block w-100 img-responsive rounded" alt="Poster 1" />
            </div>
            <div class="carousel-item">
              <img src="../assets/poster2.jpg" class="d-block w-100 img-responsive rounded" alt="Poster 3" />
            </div>
          </div>
          <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying"
            data-bs-slide="prev">
            <div class="myButton">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            </div>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying"
            data-bs-slide="next">
            <div class="myButton">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
            </div>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
      </div>
    </div>
    <div class="row p-5">
      <h1 class="text-warning">Welcome to Library Management System</h1>
      <h4 class="text-warning mt-2">
        LMS is a vast collection of eBooks and they can be rent for free !!!
      </h4>
      <p class="mt-4">
        Choose among various free eBooks to read them online or download for a
        small price. Any book can be rented upto 7 days for free !!!
      </p>
      <p>
        LMS primary objective is to make litrature available for everyone and
        anyone.
      </p>
      <h1 class="text-warning mt-5 mb-3">Login</h1>
      <div class="d-flex p-5 myIndexCont border">
        <div class="col-md-4 col-lg-4 col-sm-10">
          <img src="../assets/logo.png" alt="LOGO" class="img-thumbnail rounded" width="350px" height="350px" />
        </div>
        <div class="col-md-6 offset-md-2 col-lg-6 offset-lg-2 col-sm-10">
          <form @submit.prevent="onLogin" class="form" ref="loginForm">
            <div class="mb-3">
              <label for="username" class="form-label text-warning">Username</label>
              <input type="text" id="username" class="form-control" name="username" placeholder="alexM12"
                v-model="state.username"
                :class="{ 'is-invalid': vLogin.username.$error, 'is-valid': !vLogin.username.$invalid }">
              <div class="invalid-feedback" v-if="vLogin.username.$error">
                {{ vLogin.username.$errors[0].$message }}
              </div>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label text-warning">Password</label>
              <input type="password" id="password" class="form-control" name="password" v-model="state.password"
                :class="{ 'is-invalid': vLogin.password.$error, 'is-valid': !vLogin.password.$invalid }">
              <div class="invalid-feedback" v-if="vLogin.password.$error">
                {{ vLogin.password.$errors[0].$message }}
              </div>
            </div>
            <div class="d-grid gap-2 mt-4">
              <button class="btn btn-outline-warning" type="submit" :disabled="vLogin.$invalid">Login</button>
            </div>
          </form>
          <p class="text-secondary mt-5">
            New to Library Management ?
            <router-link to="/signUp" class="text-warning text-decoration-none">SignUp</router-link>
          </p>
          <p class="text-secondary">
            Forgot Password ?
            <a class="text-decoration-none text-warning myLink" @click="loadComponent" >Reset</a>
            <component :is="passwordModal" v-if="isModalLoaded"></component>
            <!-- Forgot Passowrd ?
            <ForgotPassword /> -->
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineAsyncComponent, reactive, ref } from "vue";
import { required, alphaNum, minLength } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import { useRouter } from "vue-router";
import { useAlertStore } from "@/stores/alertStore";
import { useUserStore } from "@/stores/userStore";

const router = useRouter();
const isModalLoaded = ref(false);
const passwordModal = ref(null);

function loadComponent(){
  isModalLoaded.value = true;
  passwordModal.value = defineAsyncComponent(()=> import('../components/ForgotPassword.vue'));
}

const state = reactive({
  username: ref(null),
  password: ref(null),
})

const rules = computed(() => {
  return {
    username: { required, alphaNum },
    password: { required, minLength: minLength(6) }
  }
})

const vLogin = useVuelidate(rules, state, {
  $autoDirty: true,
})

const onLogin = async () => {
  const alertStore = useAlertStore();
  const userStore = useUserStore();
  try {
    await userStore.userLogin(state);
    console.log(userStore.user);
    if(userStore.user.userType == "Librarian"){
      router.push('/librarianHome');
    }
    else{
      router.push('/userHome');
    }
    setTimeout(() => {
    alertStore.success("Login Successful");
    },300);
  }
  catch (error) {
    console.log(userStore.errorMessage);
    console.log(error.message);
    let message = "Login failed: ";
        if(userStore.errorMessage){
            message = message + userStore.errorMessage;
        }
        else{
            message = message + error.message;
        }
        alertStore.error(message);
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* colors: #dbe975 #fbb505 #fd5921 */
::placeholder {
  color: #dbe975;
  opacity: 0.5;
  /* Firefox */
}

::-ms-input-placeholder {
  /* Edge 12 -18 */
  color: #dbe975;
}

.myLink{
  cursor: pointer;
}

.myCarousel {
  min-height: 70dvh;
  border-radius: 10px;
}

.myButton {
  background-color: #ffffff;
  box-shadow: 2px 2px 5px #000;
  border-radius: 50%;
  padding: 1rem;
}

.myIndexCont {
  border-radius: 50px;
}
</style>
