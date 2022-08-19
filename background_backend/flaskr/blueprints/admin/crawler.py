import json
import os
import ast

from flask import Blueprint, current_app, request, send_file
from background_backend.flaskr.DBHelper import mongodb
from background_backend.flaskr.utils import respBody
import requests

# from concurrent.futures import ThreadPoolExecutor
# executor = ThreadPoolExecutor(3)

bp = Blueprint('crawler', __name__, url_prefix='/admin/crawler')


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


@bp.route('/config/test', methods=['GET'])
def download_crawler_test_config():
    if request.method == 'GET':
        data = request.args
        cli = mongodb.get_cli()
        result = cli['crawler'].get_collection('test_config').find_one(data, {'_id': 0, 'configName': 1})

        config_dir = current_app.config['CRAWLER_TEST_CONFIGS_DIR']
        config_name = result['configName'] + '.json'

        config_abs_path = os.path.join(config_dir, config_name)
        has_config = os.path.isfile(config_abs_path)
        if result is None and not has_config:
            return
        else:
            return send_file(os.path.join(config_dir, config_name), as_attachment=True)


@bp.route('/config/test', methods=['POST'])
def upload_crawler_test_config():
    if request.method == 'POST':
        file_content = request.files['file']
        file_name = file_content.filename
        file_path = os.path.join(current_app.config['CRAWLER_TEST_CONFIGS_DIR'], file_name)

        file_content.save(file_path)
        respBody['status'] = 200
        respBody['msg'] = f'upload {file_name} successful'
        return respBody


@bp.route('/config/test/content', methods=['GET'])
def get_crawler_test_config_content():
    if request.method == 'GET':
        params = request.args

        config_dir = current_app.config['CRAWLER_TEST_CONFIGS_DIR']
        config_name = params['configName'] + '.json'

        config_abs_path = os.path.join(config_dir, config_name)
        has_config = os.path.isfile(config_abs_path)

        if not has_config:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to load config'
        else:
            config_content = ''
            with open(config_abs_path, 'r', encoding='utf8') as f:
                config_content = f.read()

            respBody['status'] = 200
            respBody['msg'] = 'load config successful'
            respBody['data'] = {
                'configName': params['configName'],
                'configContent': config_content
            }

        return respBody


@bp.route('/config/test/content', methods=['POST'])
def save_crawler_test_config_content():
    if request.method == 'POST':
        data = request.get_json()

        config_dir = current_app.config['CRAWLER_TEST_CONFIGS_DIR']
        config_name = data['configName'] + '.json'
        config_content = data['configContent']

        config_abs_path = os.path.join(config_dir, config_name)
        has_config = os.path.isfile(config_abs_path)

        if not has_config:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to save config'
        else:
            with open(config_abs_path, 'w', encoding='utf8') as f:
                f.write(config_content)

            respBody['status'] = 200
            respBody['msg'] = 'load config successful'

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
