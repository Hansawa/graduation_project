import pymongo

# menu = {'menuName': 'adminMenu', 'menuList': [
#     {'id': '1', 'name': '欢迎！', 'path': 'welcome', 'icon': 'StarFilled'},
#     {
#         'id': '2', 'name': '爬虫管理', 'path': 'crawler', 'icon': 'Collection', 'children':
#         [
#             {'id': '2-1', 'name': '爬虫设置', 'path': 'settings', 'icon': 'Collection'},
#             {'id': '2-2', 'name': '配置文件', 'path': 'configs', 'icon': 'Collection'},
#             {'id': '2-3', 'name': '未处理新闻', 'path': 'raw_news', 'icon': 'Collection'},
#         ]
#     },
#     {'id': '3', 'name': '评论管理', 'path': 'comment', 'icon': 'ChatDotSquare'},
#     {'id': '4', 'name': '用户管理', 'path': 'user', 'icon': 'User'},
#     {'id': '5', 'name': '我的账号', 'path': 'admin', 'icon': 'Tools'}
# ]}
# 插入一条数据
# import pymongo
#
# cli = pymongo.MongoClient(host='localhost')
# bgbedb = cli['bgbe']
#
# menuCollection = bgbedb['menu']
# menuCollection.update_one({'menuName': menu['menuName']}, {'$set': menu}, upsert=True)
# menu = menuCollection.find_one({'menuName': 'adminMenu'}, {'_id': 0, 'menuName': 0})
# print(menu)
# cli.close()

# 插入多条数据
# import os
# import pymongo
#
# cli = pymongo.MongoClient(host='localhost')
# db = cli['crawler']
#
# collection = db['configs']
# configList = os.listdir('D:\\graduation_project\\background_backend\\flaskr\\crawler_configs')
#
# configDict = {}
# for config in configList:
#     configDict = {'configName': config.split('.')[0], 'configRelPath': config.split('.')[0]}
#     collection.update_one(configDict, {'$set': configDict}, upsert=True)
# cli.close()

# configs = [
#     {'configName': 'chinanews'},
#     {'configName': 'huashengnews'},
#     {'configName': 'xinjingnews'},
# ]
#
# config = {'configName': 'xinjingnews', 'configContent': {
#     "spider": "universal",
#     "website": "新京报",
#     "type": "新闻",
#     "index": "https://www.bjnews.com.cn/news",
#     "settings": {
#         "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
#         "RANDOMIZE_DOWNLOAD_DELAY": "True",
#         "ROBOTSTXT_OBEY": "true"
#     },
#     "allowed_domains": ["www.bjnews.com.cn"],
#     "start_urls": ["https://www.bjnews.com.cn/news"],
#     "pagination_url": "https://www.bjnews.com.cn/news/{pageNum}.html",
#     "start_end": [1, 10],
#     "step": 1,
#     "rules": [
#         {
#             "link_extractor": {
#                 "allow": "https://www.bjnews.com.cn/detail/\\d*.html",
#                 "restrict_xpaths": "//div[@id=\"waterfall-container\"]"
#             },
#             "callback": "parse_detail"
#         }
#     ],
#     "item": {
#         "collection": "xinjingnews",
#         "attrs": {
#             "title": [
#                 {
#                     "method": "xpath",
#                     "arg": "//div[@class=\"bodyTitle\"]//h1/text()"
#                 }
#             ],
#             "url": [
#                 {
#                     "method": "respAttr",
#                     "arg": "url"
#                 }
#             ],
#             "text": [
#                 {
#                     "method": "xpath",
#                     "arg": "//div[@class=\"content-name\"]"
#                 }
#             ],
#             "datetime": [
#                 {
#                     "method": "xpath",
#                     "arg": "//div[@class=\"content\"]//span[@class=\"timer\"]/text()"
#                 }
#             ],
#             "website": [
#                 {
#                     "method": "value",
#                     "arg": "新京报"
#                 }
#             ]
#         }
#     }
# }}
from bson import ObjectId

websites = [
    {'configId': ObjectId('62ff6d17a85533fa5bcfc0f1'), 'cnName': '中国新闻网'},
    {'configId': ObjectId('62ff6d17a85533fa5bcfc0f7'), 'cnName': '新京报'},
    {'configId': ObjectId('62ff6d17a85533fa5bcfc0fd'), 'cnName': '华声新闻'}
]

cli = pymongo.MongoClient(host='localhost')
db = cli['test_news']

collection = db['website']
collection.insert_many(websites)
# for config in configs:
# collection.update_one({'configName': config['configName']}, {'$set': config}, upsert=True)

documents = collection.find()
for document in documents:
    print(document)
cli.close()
