import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = request.get_json()
        return {
            'meta': {
                'status': 200,
                'msg': 'login succeeded'
            },
            'token': '123456',
            'data': {
                'adminId': '123456'
            }
        }
