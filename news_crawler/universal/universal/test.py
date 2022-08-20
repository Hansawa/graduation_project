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
s = ''' 官方往来。这是中国与各国建立和发展外交关系的核心共识和根本政治基础，涵义清楚明确。任何国家都应秉持善意，完整履行与
中国建交时的承诺。</p>\r\n\n<p>\u3000\u3000美国提出的所谓“与台湾关系法”、“对台六项保证”，七国集团外长声明中所谓“各自的一个中国政
策”、“如适用”等文字游戏，其本质都是通过国内法、甚至上不了台面的秘密保证，对一个中国原则进行单方面曲解或者自行附加条件。</p>\r\n\n<p
>\u3000\u3000以所谓“三权分立”“议员出国访问是完全正常、例行的行为”等为借口纵容议会或其他政府部门与台开展官方交往更加荒谬可笑。政治
制度不是无视和逃避国际义务的借口。议会是国家的组成部分，议会对外活动理应被视为国家行为，而一国作为国际关系和国际法的主体，有义务遵守国
际法和国际关系基本准则，完整履行曾经做出的双边承诺。</p>\r\n\n<p>\u3000\u3000概括起来，所有这些分歧的核心就是以美国为首的部分国家，表
面上打着“奉行一个中国政策，不支持‘台独’”的幌子，企图通过单方面任意解释，虚化、掏空一个中国原则，在实际上制造“两个中国”、“一中一
台”，实现其“以台制华”的政治目的。这些行径歪曲联大第2758号决议，违反国际法，严重背弃有关国家对中国做出的政治承诺，侵犯中国的主权和尊
严，践踏国际关系基本准则，挑战二战后国际秩序。对此，中国政府已多次明白无误地表明了反对和谴责的严正立场。</p>\r\n\n<p>\u3000\u3000<stro
ng>三、佩洛西窜台后，中方采取一系列坚决反制举措。而美国却批评中方“单方面改变台海现状”，采取“挑衅性军事行动”“单方面使用武力”，指
责中方采取的反制措施“不负责任”。您对此如何评论？</strong></p>\r\n\n<p>\u3000\u3000美方谬论完全是颠倒黑白、倒打一耙。台海现状就是两岸
同属一个 '''
var = re.compile('<p>').sub('\n', s)
print(var)