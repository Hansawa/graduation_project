import {createRouter, createWebHistory} from "vue-router"

/* 配置路由表。在之后的开发中，会在这里编写组件的路由 */
const routes = [
    {
        path: '/',
        redirect: {name: 'adminLogin'}
    },
    {
        path: '/admin/login',
        name: 'adminLogin',
        component: () => import('/views/Login.vue'),
        meta: {
            title: '管理员登录'
        }
    },
    {
        path: '/admin',
        name: 'admin',
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
                path: 'crawler',
                name: 'crawler',
                component: () => import('/views/crawler/index.vue'),
                redirect: {name: 'crawlerSetting'},
                meta: {
                    title: '爬虫管理'
                },
                children: [
                    {
                        path: 'setting',
                        name: 'crawlerSetting',
                        component: () => import('/views/crawler/Setting.vue'),
                        meta: {
                            title: '爬虫设置'
                        }
                    },
                    {
                        path: 'config',
                        name: 'crawlerConfig',
                        component: () => import('/views/crawler/config/index.vue'),
                        redirect: {name: 'crawlerTestConfig'},
                        meta: {
                            title: '爬虫配置'
                        },
                        children: [
                            {
                                path: 'test',
                                name: 'crawlerTest',
                                component: () => import('/views/crawler/config/test/index.vue'),
                                redirect: {name: 'crawlerTestConfig'},
                                children: [
                                    {
                                        path: 'config',
                                        name: 'crawlerTestConfig',
                                        component: () => import('/views/crawler/config/test/Test.vue'),
                                        meta: {
                                            title: '测试配置表'
                                        }
                                    },
                                    {
                                        path: 'edit_test/:_id',
                                        name: 'crawlerEditTest',
                                        component: () => import('/views/crawler/config/test/EditTest.vue'),
                                        meta: {
                                            title: '编辑与测试'
                                        }
                                    }
                                ]
                            },
                            {
                                path: 'final',
                                name: 'crawlerFinal',
                                component: () => import('/views/crawler/config/final/index.vue'),
                                redirect: {name: 'crawlerFinalConfig'},
                                children: [
                                    {
                                        path: 'config',
                                        name: 'crawlerFinalConfig',
                                        component: () => import('/views/crawler/config/final/Final.vue'),
                                        meta: {
                                            title: '最终配置表'
                                        }
                                    },
                                    {
                                        path: 'inspect/:_id',
                                        name: 'crawlerInspect',
                                        component: () => import('/views/crawler/config/final/Inspect.vue'),
                                        meta: {
                                            title: '配置查看'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                path: 'news',
                name: 'news',
                component: () => import('/views/news/index.vue'),
                redirect: {name: 'newsWebsite'},
                meta: {
                    title: '新闻管理'
                },
                children: [
                    {
                        path: 'website',
                        name: 'newsWebsite',
                        component: () => import('/views/news/Website.vue'),
                        meta: {
                            title: '新闻网站列表'
                        }
                    },
                    {
                        path: ':websiteName',
                        name: 'newsWebsiteNews',
                        component: () => import('/views/news/News.vue'),
                        props: true,
                        meta: {
                            title: '新闻列表'
                        }
                    },
                    {
                        path: ':websiteName/:_id',
                        name: 'newsWebsiteNewsDetail',
                        component: () => import('/views/news/NewsDetail.vue'),
                        props: true,
                        meta: {
                            title: '新闻内容'
                        }
                    }
                ]
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
    if (to.path === '/admin/login') {
        /* 获取当前路由元信息 */
        window.document.title = to.meta.title
        return true
    }

    /* 先从当地存储中查找 adminId（即是否自动登录），如果没有（即不是自动登录），再从会话存储中查找（即会话保持） */
    let adminId = window.localStorage.getItem('adminId')
    if (!adminId) adminId = window.sessionStorage.getItem('adminId')

    /* 自动登录或会话保持 */
    if (adminId) {
        const resp = await get('/admin/check_logged', {adminId})
        if (resp === undefined) return '/admin/login'
        /* 既不是自动登录，又不是会话保持，即第一次登录，返回登录页面 */
    } else if (!adminId) {
        ElMessage.error('Please login')
        return '/admin/login'
    }

    /* !!!! */
    let title = []
    const matched = to.matched
    for (let i = 1; i < matched.length; i++) {
        title.push(matched[i].meta.title)
        if (i > 1) break
    }
    window.document.title = title.join(' | ')
    return true
})

/* 暴露 router 实例 */
export default router