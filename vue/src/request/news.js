import {request} from "./index";

function getNewsList(params) {
    return request({
        url: '/getnewslist',
        method: 'get',
        params: params
    });
}

function addNews(data) {
    return request({
        url: '/addnews',
        method: 'post',
        data: data
    });
}

function queryNewsByNewsId(params) {
    return request({
        url: 'querynewsbynewsid',
        method: 'get',
        params
    });
}

function editNews(data) {
    return request({
        url: '/editnews',
        data,
        method: 'put'
    })
}

function deleteNews(params) {
    return request({
        url: '/deletenews',
        params,
        method: 'delete'
    })
}

export {getNewsList, addNews, queryNewsByNewsId, editNews, deleteNews}