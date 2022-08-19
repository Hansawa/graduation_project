import os

from flask import Blueprint, current_app, request, send_file
from background_backend.flaskr.DBHelper import mongodb
from background_backend.flaskr.utils import respBody
from bson.objectid import ObjectId

bp = Blueprint('raw_news', __name__, url_prefix='/admin/raw_news')


@bp.route('/website/all', methods=['GET'])
def get_all_websites():
    if request.method == 'GET':
        cli = mongodb.get_cli()
        result = cli['raw_news'].get_collection('website').find({}, {'_id': 0})

        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to load table'
        else:
            respBody['status'] = 200
            respBody['msg'] = 'Load table successful'
            rowList = [row for row in result]
            columnList = list(rowList[0].keys())
            respBody['data'] = {
                'columnList': columnList,
                'rowList': rowList
            }

            return respBody


@bp.route('/website/news/all', methods=['GET'])
def get_all_news():
    if request.method == 'GET':
        params = request.args
        cli = mongodb.get_cli()
        result = cli['raw_news'].get_collection(params['websiteName']).find({}, {'_id': 1, 'title': 1})

        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to load table'
        else:
            respBody['status'] = 200
            respBody['msg'] = 'Load table successful'

            # 将 objectId 转成字符串
            rowList = []
            for row in result:
                row['_id'] = str(row['_id'])
                rowList.append(row)

            columnList = list(rowList[0].keys())
            respBody['data'] = {
                'columnList': columnList,
                'rowList': rowList
            }

            return respBody


@bp.route('/website/news/', methods=['GET'])
def get_news():
    if request.method == 'GET':
        params = request.args
        website_name = params['websiteName']
        _id = ObjectId(params['_id'])
        cli = mongodb.get_cli()
        result = cli['raw_news'].get_collection(website_name).find_one({'_id': _id}, {'_id': 0})
        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to load table'
        else:
            respBody['status'] = 200
            respBody['msg'] = 'Load table successful'
            respBody['data'] = result

            return respBody
