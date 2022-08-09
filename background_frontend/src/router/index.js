import { createRouter, createWebHistory } from "vue-router";

/* 配置路由表。在之后的开发中，会在这里编写组件的路由 */
const routes = [
    {
        path: '/home',
        alias: '/home',
        name: '/home',
        /* 懒加载 */
        /* 为什么要这样写 */
        component: () => import('/@/views/Home.vue'),
        redirect: '/welcome',
        children: [
            {
                path: '/welcome',
                alias: '/welcome',
                name: '/welcome',
                component: () => import('/@/components/Welcome.vue')
            },
        ]
    }
];

/* 创建并配置 router 实例 */
const router = createRouter({
    /* 路由模式使用历史模式 */
    history: createWebHistory(),
    routes
});

/* 暴露 router 实例 */
export default router;