# menu = {'menuName': 'adminMenu', 'menu': [
#     {'id': '1', 'name': '欢迎！', 'path': 'welcome', 'icon': 'StarFilled'},
#     {
#         'id': '2', 'name': '爬虫管理', 'path': 'crawler', 'icon': 'Collection', 'children': [
#         {'id': '2-1', 'name': '爬虫设置', 'path': 'settings', 'icon': 'Collection', 'children': [
#             {'id': '2-1-1', 'name': 'sdfsdf', 'path': 'sdfsf', 'icon': 'Collection'}
#         ]},
#         {'id': '2-2', 'name': '配置文件', 'path': 'configs', 'icon': 'Collection'}
#     ]
#     },
#     {'id': '3', 'name': '评论管理', 'path': 'comment', 'icon': 'ChatDotSquare'},
#     {'id': '4', 'name': '用户管理', 'path': 'user', 'icon': 'User'},
#     {'id': '5', 'name': '我的账号', 'path': 'admin', 'icon': 'Tools'}
# ]}
# print(list(menu.keys()))
#
# import pymongo
#
# cli = pymongo.MongoClient(host='localhost')
# bgbedb = cli['bgbe']
#
# menuCollection = bgbedb['menu']
# # menuCollection.update_one(menu, {'$set': menu}, upsert=True)
# menu = menuCollection.find_one({'menuName': 'adminMenu'}, {'_id': 0, 'menuName': 0})
# print(menu)
# # cli.close()
import os

import pymongo
cli = pymongo.MongoClient(host='localhost')
db = cli['crawler']

collection = db['configs']
configList = os.listdir('D:\\graduation_project\\background_backend\\flaskr\\crawler_configs')

configDict = {}
for config in configList:
    configDict = {'configName': config.split('.')[0], 'configRelPath': config.split('.')[0]}
    collection.update_one(configDict, {'$set': configDict}, upsert=True)
cli.close()