import { createApp } from 'vue'
import ElementPlus from './plugins/element-plus'
import router from './router/index'
import vuex from './store/index'
import App from './App.vue'
import axios from 'axios'
import 'normalize.css'
import './assets/global.css'

const app = createApp(App)
                .use(ElementPlus)
                .use(router)
                .use(vuex)
app.config.globalProperties.axios = axios
app.mount('#app')
