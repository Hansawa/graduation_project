import requests
from flask import Blueprint, request

from backend.flaskr.DBHelper import mongodb
from backend.flaskr.utils import msg

bp = Blueprint('setting', __name__, url_prefix='/admin/crawler/setting')

crawling_has_finished = False  # 轮询条件变量


@bp.route('/crawl/all', methods=['GET'])
def crawl_all_website():
    cli = mongodb.get_cli()
    # 找出全部 final config
    result = cli['crawler'].get_collection('final_config').find({}, {'configContent': 1, 'websiteId': 1})
    configs = result

    if result is None:
        return '', 401, msg('No final config')
    # 找出对应网站 en 名，放入 COLLECTION
    config_contents = []
    for config in configs:
        result = cli['news'].get_collection('website').find_one({'_id': config['websiteId']}, {'enName': 1})
        config_content = config['configContent']
        config_content['settings']['COLLECTION'] = result['enName']
        config_contents.append(config_content)

    requests.post('http://localhost:8081/crawler/crawl/all', json=config_contents)

    global crawling_has_finished
    crawling_has_finished = True
    return '', 200, msg('Crawl all website successful')


# 前端轮询是否完成爬取
@bp.route('/polling', methods=['GET'])
def test_config_finished_polling():
    global crawling_has_finished
    if crawling_has_finished:
        crawling_has_finished = False
        return '', 200, msg('Crawling has finished')
    else:
        return '', 201, msg('Crawling, please wait...')
