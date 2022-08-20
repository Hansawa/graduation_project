import { createApp } from 'vue'
import ElementPlus from '/plugins/element-plus'
import router from './router'
import App from './App.vue'
import 'normalize.css'
import '/assets/global.css'

const app = createApp(App)
    .use(ElementPlus)
    .use(router)
    .mount('#app')
