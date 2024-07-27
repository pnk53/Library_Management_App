import { createApp } from 'vue'
import App from './App.vue'
import "@popperjs/core"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import router from './router/router'
import { createPinia } from 'pinia'

const pinia = createPinia();

createApp(App).use(router).use(pinia).mount('#app')
