import os
import json


def get_config(name):
    path = os.path.join('D:\\graduation_project\\news_crawler', 'crawler_configs', f'{name}.json')
    with open(path, 'r', encoding='utf8') as f:
        return json.loads(f.read())


# 请求结果
respBody: dict = {}
respBody['status']: int
respBody['msg']: str
respBody['token']: str
respBody['data']: dict
