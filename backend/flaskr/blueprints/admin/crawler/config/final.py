import json
import requests
from bson import ObjectId
from flask import Blueprint, request, Response
from backend.flaskr.DBHelper import mongodb
from backend.flaskr.utils import msg

bp = Blueprint('crawler_config_final', __name__, url_prefix='/admin/crawler/config/final')


# 获取全部最终配置
@bp.route('/all', methods=['GET'])
def get_all_crawler_final_configs():
    cli = mongodb.get_cli()
    try:
        result = cli['crawler'].get_collection('final_config').find({}, {'configContent': 0})

        row_list = []
        for row in result:
            row['_id'] = str(row['_id'])
            row['websiteId'] = str(row['websiteId'])
            row_list.append(row)

        if len(row_list) == 0:
            return '', 401, msg('No data')

        column_list = list(row_list[0].keys())

        resp_body = {
            'columnList': column_list,
            'rowList': row_list
        }
        return resp_body, 200, msg('load table successful')
    except Exception:
        return '', 401, msg('Fail to load table')


# 下载最终配置文件
@bp.route('/download', methods=['GET'])
def download_crawler_final_config():
    data = request.args
    _id = ObjectId(data['_id'])

    col = mongodb.get_cli()['crawler']
    result = col.get_collection('final_config').find_one({'_id': _id}, {'_id': 0, 'configName': 0})

    # 生成配置文件的二进制数据给前端，前端通过 blob 生成 json 文件
    config_content = result['configContent']
    # 解决中文乱码（不用 ascii 转化），增加缩进（格式化）
    config_content_json = json.dumps(config_content, ensure_ascii=False, indent=2)
    config_content_bin = config_content_json.encode('utf8')

    return Response(config_content_bin, mimetype='application/json', headers=msg('Download this config successful'))


# 删除某一个最终配置
@bp.route('/delete', methods=['GET'])
def delete_crawler_final_config():
    _id = ObjectId(request.args['_id'])

    try:
        cli = mongodb.get_cli()
        # 获得对应网站的 id
        col = cli['crawler'].get_collection('final_config')
        result = col.find_one({'_id': _id}, {'websiteId': 1})
        website_id = result['websiteId']

        # 获得新闻表名
        col = cli['news'].get_collection('website')
        result = col.find_one({'_id': website_id}, {'enName': 1})
        en_name = result['enName']

        # 删除该新闻表
        result = cli['news'].drop_collection(en_name)
        # 删除该网站信息
        result = col.delete_one({'_id': website_id})
        # 删除该最终配置
        col = cli['crawler'].get_collection('final_config')
        result = col.delete_one({'_id': _id})

        return '', 200, msg('Delete this config successful')
    except Exception:
        return '', 401, msg(f'Fail to delete this config')


crawling_has_finished = False  # 轮询结束条件参数


# 运行某个最终配置
@bp.route('/run', methods=['GET'])
def run_crawler_final_config():
    params = request.args
    config_id = params['_id']

    cli = mongodb.get_cli()
    _id = ObjectId(config_id)
    result = cli['crawler'].get_collection('final_config').find_one({'_id': _id}, {'websiteCnName': 0})

    drop_result = cli['test_news'].drop_collection(config_id)

    if result and drop_result is None:
        return '', 401, msg('Fail to run test config')
    else:
        data = {
            'configId': config_id,
            'configContent': result['configContent']
        }
        requests.get('http://localhost:8081/crawler/run', json=data)

        global crawling_has_finished
        crawling_has_finished = True
        return '', 200, msg('crawl news successful')


# 前端轮询是否完成爬取
@bp.route('/polling', methods=['GET'])
def final_config_finished_polling():
    global crawling_has_finished
    if crawling_has_finished:
        crawling_has_finished = False
        return '', 200, msg('Crawling has finished')
    else:
        return '', 201, msg('Crawling, please wait...')
