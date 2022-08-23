import requests
from flask import Blueprint, request, session
from backend.flaskr.DBHelper import sqlitedb
from backend.flaskr.DBHelper import mongodb
from backend.flaskr.utils import msg

bp = Blueprint('proxy', __name__, url_prefix='/admin/proxy')


@bp.route('/run', methods=['GET'])
def run_proxy_pool():
    try:
        requests.get('http://127.0.0.1:5000/run/getter')
        requests.get('http://127.0.0.1:5000/run/tester')

        return '', 200, msg('Run proxy pool successful')
    except Exception:
        return '', 401, msg('Fail to run proxy pool')


@bp.route('/stop', methods=['GET'])
def stop_proxy_pool():
    try:
        requests.get('http://127.0.0.1:5000/stop/getter')
        requests.get('http://127.0.0.1:5000/stop/tester')
        return '', 200, msg('Stop proxy pool successful')
    except Exception:
        return '', 401, msg('Fail to stop proxy pool')
