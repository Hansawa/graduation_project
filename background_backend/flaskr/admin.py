import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from ..utils.result import resultDict

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data: dict = request.get_json()

        db = get_db()
        admin: dict = db.execute(
            'SELECT * FROM admin WHERE adminName = ?', (data.get('adminName'),)
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
            resultDict['token'] = '123456'
            resultDict['data'] = {
                'adminId': admin['adminId']
            }

        return resultDict
