import functools

from flask import Blueprint, jsonify, flash, g, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from ..utils.result import resultDict

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data: dict = request.get_json()

        db = get_db()
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
            resultDict['msg'] = 'login succeeded'
            resultDict['data'] = {
                'adminId': admin['adminId'],
                'routePath': '/welcome'
            }

        return resultDict


@bp.route('/check_logged', methods=['GET'])
def check_logged():
    data: dict = request.args
    db = get_db()

    admin = db.execute(
        'SELECT adminId FROM admin WHERE adminId = ?', (data['adminId'],)
    ).fetchone()

    if admin is None:
        resultDict['status'] = 401
        resultDict['msg'] = 'Please login again'
    else:
        resultDict['status'] = 200

    return resultDict
