import {createRouter, createWebHistory} from 'vue-router'
import Login from 'views/Login';

const routes = [
    {
        path: '/',
        alias: '/',
        name: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        alias: '/login',
        name: '/login',
        component: Login,

    },
    {
        path: '/home',
        alias: '/home',
        name: '/home',
        /* 懒加载 */
        /* 为什么要这样写 */
        component: () => import('views/Home'),
        redirect: '/welcome',
        /* 原文：注意，以 / 开头的嵌套路径将被视为根路径。这允许你利用组件嵌套，而不必使用嵌套的 URL。 */
        children: [
            {
                path: '/welcome',
                alias: '/welcome',
                name: '/welcome',
                component: () => import('components/Welcome')
            },
            {
                path: '/newsmanage',
                alias: '/newsmanage',
                name: '/newsmanage',
                component: () => import('components/NewsManage')
            },
            {
                path: '/commentmanage',
                alias: '/commentmanage',
                name: '/commentmanage',
                component: () => import('components/CommentManage')
            },
            {
                path: '/usermanage',
                alias: '/usermanage',
                name: '/usermanage',
                component: () => import('components/UserManage')
            },
            {
                path: '/selfaccount',
                alias: '/selfaccount',
                name: '/selfaccount',
                component: () => import('components/SelfAccount')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

/* 挂载全局路由导航守卫 */
router.beforeEach((to, from) => {
    from;
    /* 使用导航守卫控制访问权限 */
    /* 如果跳转到登录页，放行 */
    if (to.path === '/login') return true;
    /* 如果访问出登录页以外的页面且无token */
    if (!window.sessionStorage.getItem('token')) {
        /* push也是个异步函数，也可以加await */
        router.push('/login').then(() => {
            return false;
        });
    }
})

export default router
