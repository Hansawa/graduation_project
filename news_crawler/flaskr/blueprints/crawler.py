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
def run_crawler_config():
    data = request.get_json()

    # 构造测试配置
    config_id = data['configId']
    config_content = data['configContent']
    config_content['settings']['MONGO_URI'] = 'localhost'
    config_content['settings']['MONGO_DB'] = 'test_news'
    config_content['settings']['COLLECTION'] = config_id
    config_content['start_end'] = [1, 1]

    old_path = os.getcwd()
    new_path = os.path.dirname(spiders.__file__)
    os.chdir(new_path)
    try:
        p = Process(target=run, args=('test', config_content,))
        p.start()
        p.join()
    except Exception:
        os.chdir(old_path)
        respBody['status'] = 401
        respBody['msg'] = f'Fail to crawl news'
        return

    os.chdir(old_path)
    respBody['status'] = 200
    respBody['msg'] = f'crawl news successful'
    return respBody


@bp.route('/crawl/all', methods=['POST'])
def crawl_all_website():
    config_contents = request.get_json()

    old_path = os.getcwd()
    new_path = os.path.dirname(spiders.__file__)
    os.chdir(new_path)
    try:
        p = Process(target=run, args=('serve', config_contents,))
        p.start()
        p.join()
    except Exception:
        os.chdir(old_path)
        return '', 401

    os.chdir(old_path)
    return '', 200
