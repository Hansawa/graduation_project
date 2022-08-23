from bson import ObjectId
from flask import Blueprint, request

from backend.flaskr.DBHelper import mongodb
from backend.flaskr.utils import msg

bp = Blueprint('user_news', __name__, url_prefix='/user/news')


@bp.route('/website/all', methods=['GET'])
def get_all_websites():
    result = mongodb.get_cli()['news'].get_collection('website').find({}, {'_id': 0})

    website_list = []
    for website in result:
        website_list.append(website)
    resp_body = {
        'websiteList': website_list
    }

    return resp_body, 200, msg('Load websites successful')


@bp.route('/all', methods=['GET'])
def get_all_news():
    params = request.args
    en_name = params['enName']

    result = mongodb.get_cli()['news'].get_collection(en_name).find({}, {'_id': 1, 'title': 1, 'datetime': 1})

    if result is None:
        return '', 401, msg('Fail to load news list')
    else:
        news_list = []
        for news in result:
            news['_id'] = str(news['_id'])
            news_list.append(news)

        resp_body = {
            'newsList': news_list
        }

        return resp_body, 200, msg('Load news list successful')


@bp.route('/detail', methods=['GET'])
def get_news_detail():
    params = request.args
    website = params['website']
    _id = ObjectId(params['newsId'])

    result = mongodb.get_cli()['news'].get_collection(website).find({'_id': _id}, {'_id': 0})

    if result is None:
        return '', 401, msg('Fail to load news detail')
    else:
        resp_body = {
            'newsDetail': result[0]
        }
        return resp_body, 200, msg('Load news detail successful')