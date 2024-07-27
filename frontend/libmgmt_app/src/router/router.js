import {createRouter, createWebHistory} from "vue-router";
import LoginPage from "@/components/LoginPage.vue";

const routes = [
    {
        name: 'LoginPage',
        component: LoginPage,
        path: '/'
    },
    {
        name: 'AboutUs',
        component: () => import("../components/AboutUs.vue"),
        path: '/AboutUs'
    },
    {
        name: 'ContactUs',
        component: () => import("../components/ContactUs.vue"),
        path: '/ContactUs'
    },
    {
        name: 'SignUpPage',
        component: () => import("../components/SignUpPage.vue"),
        path: '/signUp'
    },
    {
        name: 'AdminHome',
        component: () => import("../components/AdminHome.vue"),
        path: '/librarianHome'
    },
    {
        name: 'UserHome',
        component: () => import("../components/UserHome.vue"),
        path: '/userHome'
    }
];

const router = createRouter(
    {
        history: createWebHistory(),
        routes
    }
)

export default router