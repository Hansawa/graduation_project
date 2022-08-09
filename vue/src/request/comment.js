import {request} from "./index";

function getAllComments() {
    return request({
        url: '/getallcomments',
        method: 'get'
    });
}

function queryCommentsBySearchType(params) {
    return request({
        url: '/querycommentsbysearchtype',
        params,
        method: 'get'
    });
}

function deleteComment(params) {
    return request({
        url: '/deletecomment',
        params,
        method: 'delete'
    });
}

export {getAllComments, queryCommentsBySearchType, deleteComment}