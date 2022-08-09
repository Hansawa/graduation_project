import {request} from "./index";

function getUserList(params) {
    return request({
        url: '/getuserlist',
        method: 'get',
        params: params
    });
}

function resetUserPwd(data) {
    return request({
        url: '/resetuserpwd',
        data,
        method: 'post'
    });
}

function deleteUser(params) {
    return request({
        url: '/deleteuser',
        params,
        method: 'get'
    });

}

export {getUserList, resetUserPwd, deleteUser}