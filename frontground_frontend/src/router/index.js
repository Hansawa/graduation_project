import {createRouter, createWebHistory} from "vue-router"

/* 配置路由表。在之后的开发中，会在这里编写组件的路由 */
const routes = [
    {
        path: '/',
        redirect: {name: 'welcome'}
    },
    {
        path: '/user',
        name: 'user',
        component: () => import('/layouts/index.vue'),
        redirect: {name: 'welcome'},
        children: [
            {
                path: 'welcome',
                name: 'welcome',
                component: () => import('/views/Welcome.vue'),
                meta: {
                    title: '欢迎！'
                }
            },
            {
                path: ':website',
                name: 'news',
                component: () => import('/views/News.vue')
            },
            {
                path: ':website/:newsId',
                name: 'newsDetail',
                component: () => import('/views/NewsDetail.vue')
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
    // if (to.path === '/admin/login') {
    /* 获取当前路由元信息 */
    // window.document.title = to.meta.title
    // return true
    // }
    //
    // /* 先从当地存储中查找 adminId（即是否自动登录），如果没有（即不是自动登录），再从会话存储中查找（即会话保持） */
    // let adminId = window.localStorage.getItem('adminId')
    // if (!adminId) adminId = window.sessionStorage.getItem('adminId')
    //
    // /* 自动登录或会话保持 */
    // if (adminId) {
    //     const resp = await get('/admin/check_logged', {adminId})
    //     if (resp === undefined) return '/admin/login'
    //     /* 既不是自动登录，又不是会话保持，即第一次登录，返回登录页面 */
    // } else if (!adminId) {
    //     ElMessage.error('Please login')
    //     return '/admin/login'
    // }
    //
    // /* !!!! */
    // let title = []
    // const matched = to.matched
    // for (let i = 1; i < matched.length; i++) {
    //     title.push(matched[i].meta.title)
    //     if (i > 1) break
    // }
    // window.document.title = title.join(' | ')
    return true
})

/* 暴露 router 实例 */
export default router