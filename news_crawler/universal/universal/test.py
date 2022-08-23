# import re
#
# from utils import get_config
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import Rule
# from scrapy import Item, Field
#
# # =====================实现已被抽离的抓取逻辑表=========================
# config = get_config('huashengnews')
# rules = []
# # 从爬虫配置中获取每一个抓取逻辑配置
# for rule_kwargs in config.get('rules'):
#     # 获取连接提取器设置并构造相应的实例，连接提取器作用为从返回的 Respone（HTML文本） 中提取符合规定的链接
#     link_extractor = LinkExtractor(**rule_kwargs.get('link_extractor'))
#     # 将连接提取器实例重新存入抓取逻辑配置字典中
#     rule_kwargs['link_extractor'] = link_extractor
#     # 使用配置字典设置并构造抓取逻辑
#     rule = Rule(**rule_kwargs)
#     # 添加到抓取逻辑表中
#     rules.append(rule)
#
# print(rules[0].callback)
#
# # ====================动态生成 UniversalItem 类===================
# config = get_config('huashengnews')
# attr_field_dict = {}
#
# for key, value in config.get('item').get('attrs').items():
#     # 设置 UniversalItem 类的属性的类为 Field()
#     attr_field_dict[key] = Field()
#
# UniversalItem = type('UniversalItem', (Item, object), attr_field_dict)
# ChinaVoiceItem = UniversalItem()
#
# # ====================正确动态生成 UniversalItem 类的方法================
# # Item 类自带一个属性-Field 字典，代表着该 Item的所有属性及其类型为 Field
# config = get_config('huashengnews')
# UniversalItem = Item()
# for key, value in config.get('item').get('attrs').items():
#     UniversalItem.fields[key] = Field()
#     print(UniversalItem.get(key))
#
# UniversalItem['text'] = 'dsfsdf'
# print(UniversalItem.get('text'))
#
# {
#     "link_extractor": {
#         "restrict_xpaths": "//a[contains(., \"下一页\")]"
#     }
# }
#
# # ======================换页测试=========================
# # range() 可迭代对象
# # list()对象迭代器
# print(list(range(1, 10)))
#
# config = get_config('huashengnews')
# start_end = config.get("start_end")
# step = config.get("step")
# pagination_url = config.get("pagination_url")
# print(range(start_end[0] + step, start_end[1] + step))
# for pageNum in range(start_end[0] + step, start_end[1] + step, step):
#     print(eval("f'"+pagination_url+"'"))
# # 存入链接数组
# # urls = [eval(pagination_url) for pageNum in range(start_end[0] + step, start_end[1] + step)]
# # print(urls)
#
# import requests
# r = requests.get('https://www.bjnews.com.cn/detail/165940181114278.html')
# r.encoding = 'Unicode'
# print(r.text)
#
# a = 'sdfsdfs'
# b = "sdfsdfs"
#
# print(id(a) == id(b))
#
# name = 'chinanews'
# universal = get_config(name)
# config = {
#     'configName': name,
#     'configDict': universal
# }
#
# import pymongo
#
# cli = pymongo.MongoClient('localhost')
# db = cli['crawler'].get_collection('configs').update_one(config, {'$set': config}, upsert=True)
# cli.close()

import re
s = '''西宁8月21日电 (记者 李江宁)20日晚，记者从西宁市大通县“8·18”山洪灾害抢险救援处置工作应急指挥部获悉，截至当日22时，山洪灾害已造成25人遇难，6人失联，23人获救，各项救援及保障工作仍在有序进行，灾害原因正在调查中。
　　据介绍，目前共转移安置群众3104人，其中集中安置1879人、投靠亲友1225人，经对受灾房屋安全鉴定，组织742人回迁原居住房屋。省级救灾物资储备库调拨运棉被褥、绒衣裤、防寒鞋、雨衣等共6600余件套。市、县两级有关部门紧急采购了拖鞋、洗漱包、枕头等生活用品及常用药品。
'''
s.replace(' ', '')

