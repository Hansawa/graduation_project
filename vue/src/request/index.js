import axios from 'axios';

/* 返回一个配置好的axios实例 */
export function request(config) {

    const instance = axios.create({
        /* 配置请求的根路径 */
        baseURL: 'http://localhost:8080',
        timeout: 2000
    });

    instance.interceptors.request.use(config => {
        /* 将token放入headers里（创建Authorization属性），让后端进行认证 */
        config.headers.Authorization = window.sessionStorage.getItem('token');
        console.log('请求的全部信息：')
        console.log(config);
        console.log('请求的data属性：');
        console.log(config.data);
        console.log('请求的params属性：')
        console.log(config.params);
        /* 放行 */
        return config;
    }, err => {
        console.log(err);
    });

    instance.interceptors.response.use(config => {
        console.log('响应的全部信息：');
        console.log(config);
        console.log('响应的data属性：');
        console.log(config.data);
        /* 只放行data */
        return config.data;
    }, err => {
        console.log(err);
    });

    return instance(config);
}