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
    },
    {
        name: 'SectionBookExplorer',
        component: () => import("../components/SectionBookExplorer.vue"),
        path: '/explorer'
    },
    {
        name: 'ViewSection',
        component: () => import("../components/ViewSection.vue"),
        path: '/section/:sectionId'
    }
];

const router = createRouter(
    {
        history: createWebHistory(),
        routes
    }
)

router.beforeEach((to, from, next)=>{
    const currentUserRole = localStorage.getItem('userType');
    const adminRoutes = ['/librarianHome'];
    
    if (adminRoutes.includes(to.path) && currentUserRole != 'Librarian'){
        return next('/userHome');
    }

    next();
})

export default router