import {createRouter, createWebHistory} from "vue-router";
import HelloWorld from "../components/HelloWorld.vue";

const routes = [
    {
        name: 'HelloWorld',
        component: HelloWorld,
        path: '/'
    },
    {
        name: 'IntoWorld',
        component: () => import("../components/IntoWorld.vue"),
        path: '/world'
    }
];

const router = createRouter(
    {
        history: createWebHistory(),
        routes
    }
)

export default router