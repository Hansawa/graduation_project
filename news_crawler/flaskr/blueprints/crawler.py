import ast
import json
import os
from multiprocessing import Process
from flask import Blueprint, request
from news_crawler.universal.run import run
from news_crawler.universal.universal import spiders
from news_crawler.utils import respBody

bp = Blueprint('crawler', __name__, url_prefix='/crawler')


@bp.route('/run', methods=['GET'])
def run_crawler_test_config():
    if request.method == 'GET':
        data = request.get_json()

        config_name = data['configName']
        config_content = data['configContent']
        config_content['settings']['MONGO_URI'] = 'localhost'
        config_content['settings']['MONGO_DB'] = 'test_news'
        config_content['start_end'] = [1, 1]

        old_path = os.getcwd()
        new_path = os.path.dirname(spiders.__file__)
        os.chdir(new_path)
        p = Process(target=run, args=('test', config_name, config_content, ))
        p.start()
        p.join()
        os.chdir(old_path)

        respBody['status'] = 200
        respBody['msg'] = f'crawl {config_name} news successful'
        return respBody
