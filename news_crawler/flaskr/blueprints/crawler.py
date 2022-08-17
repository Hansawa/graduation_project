import os
from multiprocessing import Process
from flask import Blueprint, request
from news_crawler.universal.run import run
from news_crawler.universal.universal import spiders

bp = Blueprint('crawler', __name__, url_prefix='/crawler')


@bp.route('/run', methods=['GET'])
def run_crawler():
    if request.method == 'GET':
        data = request.args
        env = data['env']
        old_path = os.getcwd()
        new_path = os.path.dirname(spiders.__file__)
        os.chdir(new_path)
        p = Process(target=run, args=('dev', ))
        p.start()
        os.chdir(old_path)

    return {'status': 200}
