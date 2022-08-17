import os
import json


def get_config(name):
    path = os.path.join(os.getcwd(), 'crawler_configs', f'{name}.json')
    with open(path, 'r', encoding='utf8') as f:
        return json.loads(f.read())
