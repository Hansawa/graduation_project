import axios from 'axios'

/* 创建 axios 实例并配置基础url与超时时间 */
const instance = axios.create({
    /* 不使用反向代理解决跨域问题 */
    // baseURL: 'http://localhost:8080',
    /* 使用反向代理解决跨域问题 */
    baseURL: '/api',
    timeout: 2000
});

/* 为 axios 实例配置请求拦截器（可以实现携带token给后端验证等操作） */
instance.interceptors.request.use(req => {
    console.log(req);
    return req;
}, err => {
    console.log(err);
});

/* 为 axios 实例配置响应拦截器（对相应的数据进行简单处理，比如只返回data对象） */
instance.interceptors.response.use(resp => {
    console.log(resp);
    return resp.data;
}, err => {
    console.log(err);
});

/* 对 axios 实例进行简单的封装，选择这种封装形式的原因是参数比较整齐 */
function post(url, data) {
    return instance({
        method: 'POST',
        url,
        data
    });
}

/* 给parms赋予默认值 */
function get(url, params={}) {
    return instance({
        method: 'GET',
        url,
        params
    });
}

function del(url, params={}) {
    return instance({
        method: 'DELETE',
        url,
        params
    });
}

function put(url, data) {
    return instance({
        method: 'PUT',
        url,
        data
    });
}

/* 单文件上传 */
function uploadFile(url, file) {
    let data = new FormData();
    data.append('file', file);

    return instance({
        method: 'POST',
        url,
        data,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}

/* 多文件上传 */
function uploadFiles(url, files) {
    let data = new FormData();
    for (let file of files)
        data.append('files', file);

    return instance({
        method: 'POST',
        url,
        data,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}

/* 暴露封装后的方法 */
export { get, post, del, put, uploadFile, uploadFiles }