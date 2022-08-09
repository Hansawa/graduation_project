import {request} from "./index";

function adminLogin(data) {
    console.log(data);
    return request({
        url: '/adminlogin',
        method: 'post',
        data
    });
}

function queryAdminByAdminId(params) {
    return request({
        url: 'queryadminbyadminid',
        params,
        method: 'get'
    });
}

function editAdminInfo(data) {
    return request({
        url: '/editadmininfo',
        data,
        method: 'put'
    });
}

function editAdminPassword(data) {
    return request({
        url: '/editadminpassword',
        data,
        method: 'post'
    })
}

export {adminLogin, queryAdminByAdminId, editAdminInfo, editAdminPassword}