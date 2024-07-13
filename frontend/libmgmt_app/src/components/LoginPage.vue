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
          <form @submit.prevent="login" class="form" ref="loginForm">
            <div class="mb-3">
              <label for="username" class="form-label text-warning">Username</label>
              <input type="text" id="username" class="form-control" name="username" placeholder="bookworm123"
                v-model="state.username" :class="{
                  'is-invalid': v$.username.$error,
                  'is-valid': !v$.username.$invalid,
                }" />
              <div class="invalid-feedback" v-if="v$.username.$error">
                {{ v$.username.$errors[0].$message }}
              </div>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label text-warning">Password</label>
              <input type="password" name="password" id="password" class="form-control" v-model="state.password" :class="{
                'is-invalid': v$.password.$error,
                'is-valid': !v$.password.$invalid,
              }" />
              <div class="invalid-feedback" v-if="v$.password.$error">
                {{ v$.password.$errors[0].$message }}
              </div>
            </div>
            <div class="d-grid gap-2 mt-4">
              <button class="btn btn-outline-warning" type="submit" :disabled="v$.$invalid">
                Login
              </button>
            </div>
          </form>
          <p class="text-secondary mt-5">
            New to Library Management ?
            <router-link to="/signUp" class="text-warning text-decoration-none">SignUp</router-link>
          </p>
          <p class="text-secondary">
            Forgot Passowrd ?
            <ForgotPassword />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, reactive, ref } from "vue";
import { required, alpha, minLength } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import ForgotPassword from "../components/ForgotPassword.vue";

export default {
  name: "LoginPage",
  components: {
    ForgotPassword,
  },
  setup() {
    const state = reactive({
      username: ref(null),
      password: ref(null),
    });
    const rules = computed(() => {
      return {
        username: { required, alpha },
        password: { required, minLength: minLength(6) },
      };
    });
    const v$ = useVuelidate(rules, state, {
      $autoDirty: true,
    });

    return {
      state,
      v$,
    };
  },
  methods: {
    login() {
      this.v$.$validate();
      if (!this.v$.$error) {
        this.$refs.loginForm.reset();
      } else {
        alert("Failed");
      }
    },
  },
};
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
