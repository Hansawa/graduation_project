import os

from flask import Blueprint, current_app, request, session, send_from_directory, make_response, send_file
from background_backend.flaskr.DBHelper import sqlitedb
from background_backend.flaskr.DBHelper import mongodb
from background_backend.flaskr.utils import respBody
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
