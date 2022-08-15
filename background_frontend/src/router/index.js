import {createRouter, createWebHistory} from "vue-router"
import Login from '/views/Login.vue'

/* 配置路由表。在之后的开发中，会在这里编写组件的路由 */
const routes = [
    {
        path: '/',
        redirect: '/admin/login'
    },
    {
        path: '/admin/login',
        name: 'adminLogin',
        component: Login
    },
    {
        path: '/admin',
        name: 'admin',
        component: () => import('/layouts/index.vue'),
        redirect: '/admin/welcome',
        children: [
            {
                path: 'welcome',
                name: 'welcome',
                component: () => import('/views/Welcome.vue')
            },
            {
                path: 'crawler',
                name: 'crawler',
                component: () => import('/views/crawler/index.vue'),
                redirect: 'crawler/settings',
                children: [
                    {
                        path: 'settings',
                        name: 'settings',
                        component: () => import('/views/crawler/Settings.vue')
                    },
                    {
                        path: 'configs',
                        name: 'configs',
                        component: () => import('/views/crawler/Configs.vue')
                    }
                ]
            },
            {
                path: 'news',
                name: 'news',
                component: () => import('/views/news/Manage.vue')
            }
        ]
    }
]

/* 创建并配置 router 实例 */
const router = createRouter({
    /* 路由模式使用历史模式 */
    history: createWebHistory(),
    routes
})

import {get} from '/api'
import {ElMessage} from 'element-plus'

/* 挂载全局路由导航守卫 */
router.beforeEach(async (to, from) => {
    if (to.path === '/admin/login') return true

    /* 先从当地存储中查找 adminId（即是否自动登录），如果没有（即不是自动登录），再从会话存储中查找（即会话保持） */
    let adminId = window.localStorage.getItem('adminId')
    if (!adminId) adminId = window.sessionStorage.getItem('adminId')

    /* 自动登录或会话保持 */
    if (adminId) {
        const resp = await get('/admin/check_logged', {adminId})
        if (resp.status !== 200) {
            ElMessage.error(resp.msg)
            return '/admin/login'
        }
        /* 既不是自动登录，又不是会话保持，即第一次登录，返回登录页面 */
    } else if (!adminId) {
        ElMessage.error('Please login')
        return '/admin/login'
    }
})

/* 暴露 router 实例 */
export default router