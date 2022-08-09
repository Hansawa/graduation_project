import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import installElementPlus from './plugins/element'
/* 在这里@并不是src的别名，而是normalize.css依赖的根目录名的第一个字符 */
/* 在main.js import的插件或依赖的根目录是node_modules */
import '@csstools/normalize.css'
import 'css/global.css'

const app = createApp(App)
installElementPlus(app)
app.use(store).use(router).mount('#app')