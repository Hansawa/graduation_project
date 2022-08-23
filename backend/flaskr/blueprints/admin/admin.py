from flask import Blueprint, request, session
from backend.flaskr.DBHelper import sqlitedb
from backend.flaskr.DBHelper import mongodb
from backend.flaskr.utils import msg

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/menu', methods=['GET'])
def get_menu():
    col = mongodb.get_cli()['bgbe']
    result = col.get_collection('menu').find_one({'menuName': 'adminMenu'}, {'_id': 0, 'menuName': 0})
    if result is None:
        return '', 401, msg('Fail to load menu')
    else:
        resp_body = {
            'menuList': result['menuList']
        }
        return resp_body, 200, msg('load menu successful')


@bp.route('/login', methods=['POST'])
def login():
    data: dict = request.get_json()

    db = sqlitedb.get_db()
    result: dict = db.execute(
        'SELECT * FROM admin WHERE adminName = ?'
        , (data['adminName'],)).fetchone()

    if result is None:
        return '', 401, msg('Incorrect admin name')
    elif result['password'] != data['password']:
        return '', 401, msg('Incorrect password')
    else:
        session.clear()
        session['adminId'] = result['adminId']
        resp_body = {
            'adminId': result['adminId'],
            'routePath': '/admin/welcome'
        }
        return resp_body, 200, msg('Login successful')


@bp.route('/check_logged', methods=['GET'])
def check_logged():
    data = request.args
    db = sqlitedb.get_db()

    result = db.execute(
        'SELECT adminId FROM admin WHERE adminId = ?'
        , (data['adminId'],)).fetchone()

    if result is None:
        return '', 401, msg('Please login again')
    else:
        return '', 200, msg('Logined successful')


@bp.route('/name', methods=['GET'])
def get_name():
    data = request.args
    db = sqlitedb.get_db()

    result = db.execute('SELECT adminName FROM admin WHERE adminId = ?'
                        , (data['adminId'],)).fetchone()

    if result is None:
        return '', 401, msg('Miss name')
    else:
        resp_body = {'adminName': result['adminName']}
        return resp_body, 200, msg('Found name successful')
