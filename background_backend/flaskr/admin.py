import os

from flask import Blueprint, current_app, request, session, send_from_directory, make_response, send_file
from . import sqlitedb
from . import mongodb
from ..utils.respBody import respBody
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(3)

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/menu', methods=['GET'])
def get_menu():
    if request.method == 'GET':
        cli = mongodb.get_cli()
        result = cli['bgbe'].get_collection('menu').find_one({'menuName': 'adminMenu'}, {'_id': 0, 'menuName': 0})
        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Fail to load menu'
        else:
            respBody['status'] = 200
            respBody['msg'] = 'load menu successful'
            respBody['data'] = {
                'menuList': result['menuList']
            }

        return respBody

# 获取表头
# @bp.route('/crawler/configs/table/column', methods=['GET'])
# def get_crawler_configs_table_column():
#     if request.method == 'GET':
#         cli = mongodb.get_cli()
#         result = cli['bgbe'].get_collection('tablecolumn')\
#             .find_one({'tableName': 'configsTable'}, {'_id': 0, 'tableName': 0})
#         if result is None:
#             respBody['status'] = 401
#             respBody['msg'] = 'Fail to load table column'
#         else:
#             respBody['status'] = 200
#             respBody['msg'] = 'load table column successful'
#             respBody['data'] = {
#                 'columnList': result['columnList']
#             }
#
#         return respBody


@bp.route('/crawler/configs/table', methods=['GET'])
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


@bp.route('/crawler/config', methods=['GET'])
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


@bp.route('crawler/config', methods=['POST'])
def post_crawler_config():
    fileContent = request.files['file']
    fileName = fileContent.filename
    filePath = os.path.join(current_app.config['CRAWLER_CONFIGS_DIR'], fileName)

    # if os.path.exists(filePath):
    #     respBody['status'] = 401
    #     respBody['msg'] = f'{fileName} has existed'
    # else:
    fileContent.save(filePath)
    respBody['status'] = 200
    respBody['msg'] = f'upload {fileName} successful'
    return respBody


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data: dict = request.get_json()

        db = sqlitedb.get_db()
        result: dict = db.execute(
            'SELECT * FROM admin WHERE adminName = ?'
            , (data['adminName'],)).fetchone()

        if result is None:
            respBody['status'] = 401
            respBody['msg'] = 'Incorrect admin name'
        elif result['password'] != data['password']:
            respBody['status'] = 401
            respBody['msg'] = 'Incorrect password'
        else:
            session.clear()
            session['adminId'] = result['adminId']
            respBody['status'] = 200
            respBody['msg'] = 'Login successful'
            respBody['data'] = {
                'adminId': result['adminId'],
                'routePath': '/admin/welcome'
            }

        return respBody


@bp.route('/check_logged', methods=['GET'])
def check_logged():
    data = request.args
    db = sqlitedb.get_db()

    result = db.execute(
        'SELECT adminId FROM admin WHERE adminId = ?'
        , (data['adminId'],)).fetchone()

    if result is None:
        respBody['status'] = 401
        respBody['msg'] = 'Please login again'
    else:
        respBody['status'] = 200

    return respBody


@bp.route('/name', methods=['GET'])
def get_name():
    data = request.args
    db = sqlitedb.get_db()

    result = db.execute('SELECT adminName FROM admin WHERE adminId = ?'
                             , (data['adminId'],)).fetchone()

    if result is None:
        respBody['status'] = 401
        respBody['msg'] = 'Miss name'
    else:
        respBody['status'] = 200
        respBody['msg'] = 'Found name successful'
        respBody['data'] = {
            'adminName': result['adminName']
        }

    return respBody
