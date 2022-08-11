import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig(({command, mode, ssrBuild}) => {
  // dev and serve
  if (command === 'serve') {
    // console.log(process.cwd())
    return {
      root: './',
      /*
        root: project root directory, where 'index.html' is located.
        default: process.cwd(), process from node.exe.
        absolute path (if you move your 'index.html' to 'src' directory)
        root: 'D:/graduation_project/background/src', both '/' and '\\'.
        relative path (relative to current working directory)
        root: './src'
       */

      base: '/',
      /*
        部署到网站后的基址，要以 '/' 结尾
        项目启动后在浏览器开发者模式源代码中（也即部署后）所有文件（不包括在 public 目录中的静态资源）都将以它作为基址，以它为根目录
        router 也要以它为基址才能实现路由跳转
      */

      mode: 'development',
      /* 设置开发模式（development）或发布、构建模式（production） */

      define: {
        __APP_VERSION__: JSON.stringify('v0.0.1'),
      },
      /*
        定义全局变量，值必须是 JSON 对象
        如果变量的值要为字符串，不能直接写字符串，因为会被当成表达式，
        需要用 JSON.stringify() 转成字符串
      */

      plugins: [vue()],
      /* 构建工具 vite 将会使用的插件 */

      publicDir: 'public',
      /*
        存放静态资源的路径，默认为 'public'
        可以为绝对地址，也可以为基于项目根目录的相对地址
        开发模式下，在该目录的静态资源将不会做任何的处理，直接复制到网站的根路径
        发布模式下，在该目录的静态资源将不会做任何的处理，直接复制到 'outDir' 路径的根路径
      */

      cacheDir: 'node_modules/.vite',
      /* 用来存放缓存文件的目录 */

      resolve: {
        alias: {
          /* __dirname 获取当前项目的根目录 */
          '/assets': path.resolve('./src', './assets'),
          '/request': path.resolve('./src', './request'),
          '/views': path.resolve('./src', './views'),
          '/components': path.resolve('./src', './components')
        },
        /* 给路径取别名，直接使用时只适用于 js，css 块的导入，不适用于 html
        * 如果要在 html 中使用，先把路径指向的文件导入到 js 中，同时会创建一个新的响应式变量，
        * 然后在 html 模板中使用 */

        extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json']
        /* 导入时不需要写扩展名的文件 */
      },

      server: {
        host: 'localhost',
        /* 该项目启动时，服务器要监听的 ip 地址，一有对该地址发送请求便返回页面 */

        port: 8081,
        /* 服务器监听的 ip 地址的端口号 */

        strictPort: true,

        // open: true,
        /* 每次启动时是否自动打开页面 */

        /* 热部署 */
        hotOnly: false,
        liveReload: true,

        proxy: {
          '/api': {
            target: 'http://localhost:8080',
            changeOrigin: true,
            rewrite: path => path.replace(/^\/api/, '')
          }
        },
        /* 设置代理，可以用来解决跨域问题（如上） */

        cors: false
        /* 是否接受所有来源的请求，不接受就会产生跨域问题 */
      }
    }
  }
  else if (command === 'build') {
    return {

    }
  }
})