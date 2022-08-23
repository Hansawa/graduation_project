from bson import ObjectId
from flask import Blueprint, request

from backend.flaskr.DBHelper import mongodb
from backend.flaskr.utils import msg

bp = Blueprint('final_news', __name__, url_prefix='/admin/news/final')


@bp.route('/website/all', methods=['GET'])
def get_all_websites():
    result = mongodb.get_cli()['news'].get_collection('website').find({}, {})

    if result is None:
        return '', 401, msg('Fail to load table')
    else:
        row_list = []
        for row in result:
            row['_id'] = str(row['_id'])
            row_list.append(row)

        if len(row_list) == 0:
            return '', 401, msg('No data')
        column_list = list(row_list[0].keys())

        resp_body = {
            'columnList': column_list,
            'rowList': row_list
        }
        return resp_body, 200, msg('load table successful')


@bp.route('/all', methods=['GET'])
def get_all_news():
    params = request.args
    websiteName = params['websiteName']

    col = mongodb.get_cli()['news'].get_collection(websiteName)
    result = col.find({}, {})

    if result is None:
        return '', 401, msg('Fail to load table')
    else:
        row_list = []
        for row in result:
            row['_id'] = str(row['_id'])
            row_list.append(row)

        if len(row_list) == 0:
            return '', 401, msg('No data')
        column_list = list(row_list[0].keys())

        resp_body = {
            'columnList': column_list,
            'rowList': row_list
        }
        return resp_body, 200, msg('load table successful')


@bp.route('/delete', methods=['GET'])
def delete_news():
    params = request.args
    website_name = params['websiteName']
    _id = ObjectId(params['_id'])

    result = mongodb.get_cli()['news'].get_collection(website_name).delete_one({'_id': _id})

    if result is None:
        return '', 401, msg('Fail to delete news')
    else:
        return '', 200, msg('Delete news successful')


@bp.route('/', methods=['GET'])
def get_news():
    params = request.args
    website_name = params['websiteName']
    _id = ObjectId(params['_id'])

    result = mongodb.get_cli()['news'].get_collection(website_name).find({'_id': _id})

    if result is None:
        return '', 401, msg('Fail to load table')
    else:
        row_list = []
        for row in result:
            row['_id'] = str(row['_id'])
            row_list.append(row)

        if len(row_list) == 0:
            return '', 401, msg('No data')

        resp_body = {
            'rowList': row_list
        }
        return resp_body, 200, msg('load table successful')
