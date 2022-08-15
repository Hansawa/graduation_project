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
        menu: dict = cli['bgbe'].get_collection('menu').find_one({'menuName': 'adminMenu'}, {'_id': 0, 'menuName': 0})
        if menu is None:
            resultDict['status'] = 200
            resultDict['msg'] = 'Fail to load menu'
        else:
            resultDict['status'] = 200
            resultDict['msg'] = 'Get menu successful'
            resultDict['data'] = {
                'menuList': menu['menuList']
            }

        return resultDict


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data: dict = request.get_json()

        db = sqlitedb.get_db()
        admin: dict = db.execute(
            'SELECT * FROM admin WHERE adminName = ?', (data['adminName'],)
        ).fetchone()

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
                'routePath': '/welcome'
            }

        return resultDict


@bp.route('/check_logged', methods=['GET'])
def check_logged():
    data: dict = request.args
    db = sqlitedb.get_db()

    admin = db.execute(
        'SELECT adminId FROM admin WHERE adminId = ?', (data['adminId'],)
    ).fetchone()

    if admin is None:
        resultDict['status'] = 401
        resultDict['msg'] = 'Please login again'
    else:
        resultDict['status'] = 200

    return resultDict
