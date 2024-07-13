import { createApp } from 'vue'
import App from './App.vue'
import "@popperjs/core"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import router from './router/router'

createApp(App).use(router).mount('#app')
