import json
import os
import ast

from bson import ObjectId
from flask import Blueprint, current_app, request, send_file, Response
from flask_socketio import emit
from werkzeug.utils import secure_filename
from background_backend.flaskr.DBHelper import mongodb
from background_backend.flaskr.utils import respBody
import requests


# from concurrent.futures import ThreadPoolExecutor
# executor = ThreadPoolExecutor(3)

bp = Blueprint('crawler', __name__, url_prefix='/admin/crawler')


# 获取全部测试配置文件信息
@bp.route('/config/test/all', methods=['GET'])
def get_all_crawler_test_configs():
    if request.method == 'GET':
        cli = mongodb.get_cli()
        result = cli['crawler'].get_collection('test_config').find({}, {'_id': 1, 'configName': 1})

        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to load table'
        else:
            respBody['status'] = 200
            respBody['msg'] = 'load table successful'

            row_list = []
            for row in result:
                row['_id'] = str(row['_id'])
                row_list.append(row)

            column_list = list(row_list[0].keys())
            respBody['data'] = {
                'columnList': column_list,
                'rowList': row_list
            }

        return respBody


# 下载测试配置文件
@bp.route('/config/test', methods=['GET'])
def download_crawler_test_config():
    if request.method == 'GET':
        data = request.args
        _id = ObjectId(data['_id'])

        cli = mongodb.get_cli()
        result = cli['crawler'].get_collection('test_config').find_one({'_id': _id}, {'_id': 0, 'configName': 0})

        # 生成配置文件的二进制数据给前端，前端通过 blob 生成 json 文件
        config_content = result['configContent']
        # 解决中文乱码（不用 ascii 转化），增加缩进（格式化）
        config_content_json = json.dumps(config_content, ensure_ascii=False, indent=2)
        config_content_bin = config_content_json.encode('utf8')

        return Response(config_content_bin, mimetype='application/json')


# 上传测试配置文件
@bp.route('/config/test', methods=['POST'])
def upload_crawler_test_config():
    if request.method == 'POST':
        file_content = request.files['file']
        # 去掉扩展名
        config_name = secure_filename(file_content.filename).split('.')[0]

        # 读取文件二进制流，解码成字符串，再生成字典
        config_content_bin = file_content.stream.read()
        config_content_str = config_content_bin.decode('utf8')
        config_content = ast.literal_eval(config_content_str)
        config = {
            'configName': config_name,
            'configContent': config_content
        }

        cli = mongodb.get_cli()
        result = cli['crawler'].get_collection('test_config').update_one({'configName': config_name}, {'$set': config},
                                                                         upsert=True)

        if result is None:
            respBody['status'] = 401
            respBody['msg'] = f'Fail to upload {config_name}'
        else:
            respBody['status'] = 200
            respBody['msg'] = f'upload {config_name} successful'

        return respBody


# 获取测试配置内容
@bp.route('/config/test/content', methods=['GET'])
def get_crawler_test_config_content():
    if request.method == 'GET':
        params = request.args
        _id = ObjectId(params['_id'])

        cli = mongodb.get_cli()
        result = cli['crawler'].get_collection('test_config').find_one({'_id': _id})

        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to load config content'
        else:
            config_id = str(result['_id'])
            config_name = result['configName']
            config_content = json.dumps(result['configContent'], ensure_ascii=False, indent=2)
            respBody['status'] = 200
            respBody['msg'] = 'load config content successful'
            respBody['data'] = {
                'configId': config_id,
                'configName': config_name,
                'configContent': config_content
            }

        return respBody


# 保存修改后的测试配置文件内容
@bp.route('/config/test/content', methods=['POST'])
def save_crawler_test_config_content():
    if request.method == 'POST':
        data = request.get_json()
        _id = ObjectId(data['configId'])
        config_content = ast.literal_eval(data['configContent'])
        config = {
            'configName': data['configName'],
            'configContent': config_content
        }

        cli = mongodb.get_cli()
        result = cli['crawler'].get_collection('test_config').update_one({'_id': _id}, {'$set': config}, upsert=True)

        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to save config'
        else:
            respBody['status'] = 200
            respBody['msg'] = 'Save config successful'

        return respBody


# 运行测试配置
@bp.route('/config/test/run', methods=['GET'])
def run_crawler_test_config():
    params = request.args
    _id = ObjectId(params['configId'])

    cli = mongodb.get_cli()
    result = cli['crawler'].get_collection('test_config').find_one({'_id': _id}, {'_id': 0})

    drop_result = cli['test_news'].drop_collection(result['configName'])

    if result and drop_result is None:
        respBody['status'] = 401
        respBody['msg'] = 'Fail to run test config'
        return respBody
    else:
        config_name = result['configName']
        config_content = result['configContent']
        data = {
            'configName': config_name,
            'configContent': config_content
        }
        resp = requests.get('http://localhost:8081/crawler/run', json=data)

        print(resp)
        respBody['status'] = 200
        respBody['msg'] = 'Start the crawler successful'
        return respBody


@bp.route('/config/all', methods=['GET'])
def get_all_crawler_configs():
    if request.method == 'GET':
        cli = mongodb.get_cli()
        result = cli['crawler'].get_collection('configs').find({}, {'_id': 0, 'configName': 1})

        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to load table'
        else:
            respBody['status'] = 200
            respBody['msg'] = 'load table successful'
            rowList = [row for row in result]
            columnList = list(rowList[0].keys())
            respBody['data'] = {
                'columnList': columnList,
                'rowList': rowList
            }

        return respBody


@bp.route('/config', methods=['GET'])
def get_crawler_config():
    if request.method == 'GET':
        data = request.args
        cli = mongodb.get_cli()
        result = cli['crawler'].get_collection('configs').find_one(data, {'_id': 0, 'configRelPath': 1})

        config_dir = current_app.config['CRAWLER_CONFIGS_DIR']
        configName = result['configRelPath'] + '.json'

        configabsPath = os.path.join(config_dir, configName)
        hasConfigFile = os.path.isfile(configabsPath)
        if result is None and not hasConfigFile:
            return
        else:
            return send_file(os.path.join(config_dir, configName), as_attachment=True)


@bp.route('/config', methods=['POST'])
def post_crawler_config():
    if request.method == 'POST':
        file_content = request.files['file']
        file_name = file_content.filename
        file_path = os.path.join(current_app.config['CRAWLER_CONFIGS_DIR'], file_name)

        file_content.save(file_path)
        respBody['status'] = 200
        respBody['msg'] = f'upload {file_name} successful'
        return respBody


@bp.route('/run', methods=['GET'])
def run_crawler():
    if request.method == 'GET':
        params: dict = request.args
        resp = requests.get('http://localhost:8081/crawler/run', params)

        if resp.status_code != 200:
            respBody['status'] = resp.status_code
            respBody['msg'] = 'Fail to run crawler'
        else:
            respBody['status'] = resp.status_code
            respBody['msg'] = 'Run crawler successful'

        return respBody
