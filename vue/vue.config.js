module.exports = {
    /* 配置Webpack */
    configureWebpack: {
        resolve: {
            /* 对路径取别名，@为src的别名，在style中启用别名要加~ */
            alias: {
                'assets': '@/assets',
                'css': '@/assets/css',
                'network': '@/network',
                'components': '@/components',
                'views': '@/views',
                'request': '@/request'
            }
        }
    },
    /* 部署项目后的网站前端请求根路径（http://localhost:8080/）,，当它等于./时为相对路径 */
    publicPath: '/',
    /* build后输出文件的根目录 */
    outputDir: 'dist',
    /* 相对于outputDir的静态资源build后存放的目录 */
    assetsDir: '',
    /* 开发服务器配置 */
    devServer: {
        /* 指定要使用的host */
        host: 'localhost',
        /*hot: true,*/
        /* 热部署 */
        hotOnly: false,
        liveReload: true,
        /* 不使用https */
        https: false,
        /* 设置index（首页）文件的文件名（指定单页面名称） */
        index: 'index.html',
        /* 服务器启动时是否打开页面，可以提供浏览器名 */
        open: true,
        /* 全屏显示编译错误与不在全屏显示警告 */
        overlay: {
            warnings: false,
            errors: true
        },
        /* 修改服务器端口号 */
        port: 80,
        /* 代理后端url来进行通信 */
        // proxy: {
        //     /* 可以改成''，这样请求就可以不加/api了 */
        //     '/api': {
        //         target: 'http://localhost:8080',
        //         /* 当使用/api后，target会与/api加后面的路径拼接形成请求，在这里我们把请求的'/api'字符串去掉，才能够正确找到后端接口 */
        //         pathRewrite: {'^/api': ''},
        //         /* 开放证书无效的后端服务器（当target使用了https时） */
        //         secure: false,
        //     }
        // }
    }
}
