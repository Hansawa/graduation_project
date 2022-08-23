from flask import Blueprint, request
from backend.flaskr.DBHelper import mongodb
from backend.flaskr.utils import msg
from bson.objectid import ObjectId

bp = Blueprint('test_news', __name__, url_prefix='/admin/news/test')


@bp.route('/all', methods=['GET'])
def get_all_test_news():
    params = request.args
    config_id = params['_id']

    cli = mongodb.get_cli()
    result = cli['test_news'].get_collection(config_id).find({}, {})

    if result is None:
        return None, 401, msg('Fail to load table')
    else:
        # 将 objectId 转成字符串
        rowList = []
        for row in result:
            row['_id'] = str(row['_id'])
            rowList.append(row)
        if len(rowList) == 0:
            return '', 401, msg('No data')
        columnList = list(rowList[0].keys())
        resp_body = {
            'columnList': columnList,
            'rowList': rowList
        }
        return resp_body, 200, msg('Load table successful')


@bp.route('/', methods=['GET'])
def get_test_news():
    params = request.args
    website_name = params['websiteName']
    _id = ObjectId(params['_id'])
    cli = mongodb.get_cli()
    result = cli['raw_news'].get_collection(website_name).find_one({'_id': _id}, {'_id': 0})
    if result is None:
        return None, 401, msg('Fail to load table')
    else:
        resp_body = result
        return resp_body, 200, msg('Load table successful')
