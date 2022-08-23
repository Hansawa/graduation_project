import ast
import json
import requests
from bson import ObjectId
from flask import Blueprint, request, Response
from werkzeug.utils import secure_filename
from backend.flaskr.DBHelper import mongodb
from backend.flaskr.utils import msg

bp = Blueprint('crawler_config_test', __name__, url_prefix='/admin/crawler/config/test')


# 获取全部测试配置文件信息
@bp.route('/all', methods=['GET'])
def get_all_crawler_test_configs():
    col = mongodb.get_cli()['crawler'].get_collection('test_config')
    result = col.find({}, {'configContent': 0})

    if result is None:
        return '', 401, msg('Fail to load table')
    else:
        row_list = []
        for row in result:
            if row['configName'] == 'universal':
                continue
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


# 下载测试配置文件
@bp.route('/download', methods=['GET'])
def download_crawler_test_config():
    params = request.args
    _id = ObjectId(params['_id'])

    col = mongodb.get_cli()['crawler'].get_collection('test_config')
    result = col.find_one({'_id': _id}, {'_id': 0, 'configName': 0})

    # 生成配置文件的二进制数据给前端，前端通过 blob 生成 json 文件
    config_content = result['configContent']
    # 解决中文乱码（不用 ascii 转化），增加缩进（格式化）
    config_content_json = json.dumps(config_content, ensure_ascii=False, indent=2)
    config_content_bin = config_content_json.encode('utf8')

    return Response(config_content_bin, mimetype='application/json', headers=msg('Download this config successful'))


# 上传测试配置文件
@bp.route('/upload', methods=['POST'])
def upload_crawler_test_config():
    file_content = request.files['file']

    # 去掉扩展名
    config_name = secure_filename(file_content.filename).split('.')[0]
    # 读取文件二进制流，解码成字符串，再生成字典
    config_content_bin = file_content.stream.read()
    config_content_str = config_content_bin.decode('utf8')
    config_content = ast.literal_eval(config_content_str)

    col = mongodb.get_cli()['crawler'].get_collection('test_config')
    # 判断在数据库中是否存在
    result = col.find_one({'configName': config_name})

    if result is not None:
        result = col.update_one({'configName': config_name}, {'$set': {'configContent': config_content}})
    else:
        config = {
            'configName': config_name,
            'websiteCnName': '',
            'websiteEnName': '',
            'configContent': config_content
        }
        result = col.insert_one(config)

    if result is None:
        return '', 401, msg(f'Fail to upload {config_name}')
    else:
        return '', 200, msg(f'upload {config_name} successful')


# 获取测试配置内容
@bp.route('/content', methods=['GET'])
def get_crawler_test_config_content():
    params = request.args
    _id = ObjectId(params['_id'])

    col = mongodb.get_cli()['crawler']
    result = col.get_collection('test_config').find_one({'_id': _id})

    if result is None:
        return '', 401, msg('Fail to load config content')
    else:
        resp_body = {
            '_id': str(result['_id']),
            'configName': result['configName'],
            'websiteCnName': result['websiteCnName'],
            'websiteEnName': result['websiteEnName'],
            'configContent': json.dumps(result['configContent'], ensure_ascii=False, indent=2)
        }
        return resp_body, 200, msg('load config content successful')


# 保存修改后的测试配置文件内容
@bp.route('/content', methods=['POST'])
def save_crawler_test_config_content():
    data = request.get_json()
    _id = ObjectId(data['_id'])
    config = {
        'configName': data['configName'],
        'websiteCnName': data['websiteCnName'],
        'websiteEnName': data['websiteEnName'],
        'configContent': ast.literal_eval(data['configContent'])
    }

    col = mongodb.get_cli()['crawler']
    result = col.get_collection('test_config').update_one({'_id': _id}, {'$set': config}, upsert=True)

    if result is None:
        return '', 401, msg('Fail to save config')
    else:
        return '', 200, msg('Save config successful')


crawling_has_finished = False  # 轮询结束条件参数


# 运行测试配置
@bp.route('/run', methods=['GET'])
def run_crawler_test_config():
    params = request.args
    config_id = params['_id']

    cli = mongodb.get_cli()
    _id = ObjectId(config_id)
    result = cli['crawler'].get_collection('test_config').find_one({'_id': _id}, {'websiteCnName': 0})

    drop_result = cli['test_news'].drop_collection(config_id)

    if result and drop_result is None:
        return '', 401, msg('Fail to run test config')
    else:
        data = {
            'configId': config_id,
            'websiteEnName': result['websiteEnName'],
            'configContent': result['configContent']
        }
        requests.get('http://localhost:8081/crawler/run', json=data)

        global crawling_has_finished
        crawling_has_finished = True
        return '', 200, msg('crawl news successful')


# 前端轮询是否完成爬取
@bp.route('/polling', methods=['GET'])
def test_config_finished_polling():
    global crawling_has_finished
    if crawling_has_finished:
        crawling_has_finished = False
        return '', 200, msg('Crawling has finished')
    else:
        return '', 201, msg('Crawling, please wait...')


# 删除测试数据
@bp.route('/temp/delete', methods=['GET'])
def delete_temp():
    params = request.args
    _id = params['_id']

    result = mongodb.get_cli()['test_news'].drop_collection(_id)

    if result is None:
        return '', 401, msg('Fail to delete temp data')
    else:
        return '', 200, msg('Delete temp data successful')


# 删除某一个测试配置
@bp.route('/delete', methods=['GET'])
def delete_crawler_test_config():
    _id = ObjectId(request.args['_id'])

    col = mongodb.get_cli()['crawler'].get_collection('test_config')
    result = col.delete_one({'_id': _id})

    if result is None:
        return '', 401, msg('Fail to delete this config')
    else:
        return '', 200, msg('Delete this config successful')


# 提交某个测试配置
@bp.route('/submit', methods=['POST'])
def submit_test_config():
    data = request.get_json()
    _id = ObjectId(data['_id'])
    website_cn_name = data['websiteCnName']
    website_en_name = data['websiteEnName']
    if website_cn_name == '' or website_en_name == '':
        return '', 401, msg('Website name can not null!')

    db = mongodb.get_cli()['crawler']
    col = db.get_collection('test_config')

    # 查看该测试配置是否在数据库
    result = col.find_one({'_id': _id})
    config = result

    if result is None:
        return '', 401, msg('config miss, please refresh')
    else:
        # 在 news 数据库中的 website 表插入当前配置对应的网站数据
        db = mongodb.get_cli()['news']
        col = db.get_collection('website')
        website = {
            'cnName': website_cn_name,
            'enName': website_en_name,
        }
        result = col.update_one({'enName': website_en_name}, {'$set': website}, upsert=True)

        if result.upserted_id is None:
            return '', 401, msg('final config has existed, please delete it first')
        else:
            # 插入最终配置文件数据库
            config_name = config['configName']
            config['websiteId'] = result.upserted_id
            config.pop('websiteCnName')
            config.pop('websiteEnName')

            db = mongodb.get_cli()['crawler']
            col = db.get_collection('final_config')

            result = col.update_one({'configName': config_name}, {'$set': config}, upsert=True)

            if result is None:
                return '', 401, msg('Fail to submit this config')
            else:
                return '', 200, msg('Submit this config successful')
