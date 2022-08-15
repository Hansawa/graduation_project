import functools

from flask import Blueprint, jsonify, flash, g, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import background_backend.flaskr.sqlitedb as sqlitedb
import background_backend.flaskr.mongodb as mongodb
from ..utils.result import resultDict

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/menu', methods=['GET'])
def get_menu():
    if request.method == 'GET':
        cli = mongodb.get_cli()
        menuList = cli['bgbe'].get_collection('menu').find_one({'menuName': 'adminMenu'}, {'_id': 0, 'menuName': 0})
        if menuList is None:
            resultDict['status'] = 401
            resultDict['msg'] = 'Fail to load menu'
        else:
            resultDict['status'] = 200
            resultDict['msg'] = 'load menu successful'
            resultDict['data'] = {
                'menuList': menuList['menuList']
            }

        return resultDict


@bp.route('/crawler/configs/table/column', methods=['GET'])
def get_crawler_configs_table_column():
    if request.method == 'GET':
        cli = mongodb.get_cli()
        columnList = cli['bgbe'].get_collection('tablecolumn').find_one({'tableName': 'configsTable'}, {'_id': 0, 'tableName': 0})
        if columnList is None:
            resultDict['status'] = 401
            resultDict['msg'] = 'Fail to load table column'
        else:
            resultDict['status'] = 200
            resultDict['msg'] = 'load table column successful'
            resultDict['data'] = {
                'columnList': columnList['columnList']
            }

        return resultDict


@bp.route('/crawler/configs/table', methods=['GET'])
def get_crawler_configs_table():
    if request.method == 'GET':
        cli = mongodb.get_cli()
        table = cli['crawler'].get_collection('configs').find({}, {'_id': 0, 'configName': 1})

        if table is None:
            resultDict['status'] = 401
            resultDict['msg'] = 'Fail to load table'
        else:
            resultDict['status'] = 200
            resultDict['msg'] = 'load table successful'
            rowList = [row for row in table]
            resultDict['data'] = {
                'table': rowList
            }

        return resultDict


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data: dict = request.get_json()

        db = sqlitedb.get_db()
        admin: dict = db.execute(
            'SELECT * FROM admin WHERE adminName = ?'
            , (data['adminName'],)).fetchone()

        if admin is None:
            resultDict['status'] = 401
            resultDict['msg'] = 'Incorrect admin name'
        elif admin['password'] != data['password']:
            resultDict['status'] = 401
            resultDict['msg'] = 'Incorrect password'
        else:
            session.clear()
            session['adminId'] = admin['adminId']
            resultDict['status'] = 200
            resultDict['msg'] = 'Login successful'
            resultDict['data'] = {
                'adminId': admin['adminId'],
                'routePath': '/admin/welcome'
            }

        return resultDict


@bp.route('/check_logged', methods=['GET'])
def check_logged():
    data = request.args
    db = sqlitedb.get_db()

    admin = db.execute(
        'SELECT adminId FROM admin WHERE adminId = ?'
        , (data['adminId'],)).fetchone()

    if admin is None:
        resultDict['status'] = 401
        resultDict['msg'] = 'Please login again'
    else:
        resultDict['status'] = 200

    return resultDict


@bp.route('/name', methods=['GET'])
def get_name():
    data = request.args
    db = sqlitedb.get_db()

    admin = db.execute('SELECT adminName FROM admin WHERE adminId = ?'
                             , (data['adminId'],)).fetchone()

    if admin is None:
        resultDict['status'] = 401
        resultDict['msg'] = 'Miss name'
    else:
        resultDict['status'] = 200
        resultDict['msg'] = 'Found name successful'
        resultDict['data'] = {
            'adminName': admin['adminName']
        }

    return resultDict
