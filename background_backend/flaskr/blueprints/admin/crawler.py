import os

from flask import Blueprint, current_app, request, send_file
from background_backend.flaskr.DBHelper import mongodb
from background_backend.flaskr.utils import respBody
import requests

# from concurrent.futures import ThreadPoolExecutor
# executor = ThreadPoolExecutor(3)

bp = Blueprint('crawler', __name__, url_prefix='/admin/crawler')


@bp.route('/configs/table', methods=['GET'])
def get_crawler_configs_table():
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

        configsDir = current_app.config['CRAWLER_CONFIGS_DIR']
        configName = result['configRelPath'] + '.json'

        configabsPath = os.path.join(configsDir, configName)
        hasConfigFile = os.path.isfile(configabsPath)
        if result is None and not hasConfigFile:
            return
        else:
            return send_file(os.path.join(configsDir, configName), as_attachment=True)


@bp.route('/config', methods=['POST'])
def post_crawler_config():
    if request.method == 'POST':
        fileContent = request.files['file']
        fileName = fileContent.filename
        filePath = os.path.join(current_app.config['CRAWLER_CONFIGS_DIR'], fileName)

        fileContent.save(filePath)
        respBody['status'] = 200
        respBody['msg'] = f'upload {fileName} successful'
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
