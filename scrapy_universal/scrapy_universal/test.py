from utils import get_config
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Item, Field

# =====================实现已被抽离的抓取逻辑表=========================
config = get_config('huashengnews')
rules = []
# 从爬虫配置中获取每一个抓取逻辑配置
for rule_kwargs in config.get('rules'):
    # 获取连接提取器设置并构造相应的实例，连接提取器作用为从返回的 Respone（HTML文本） 中提取符合规定的链接
    link_extractor = LinkExtractor(**rule_kwargs.get('link_extractor'))
    # 将连接提取器实例重新存入抓取逻辑配置字典中
    rule_kwargs['link_extractor'] = link_extractor
    # 使用配置字典设置并构造抓取逻辑
    rule = Rule(**rule_kwargs)
    # 添加到抓取逻辑表中
    rules.append(rule)

print(rules[0].callback)

# ====================动态生成 UniversalItem 类===================
config = get_config('huashengnews')
attr_field_dict = {}

for key, value in config.get('item').get('attrs').items():
    # 设置 UniversalItem 类的属性的类为 Field()
    attr_field_dict[key] = Field()

UniversalItem = type('UniversalItem', (Item, object), attr_field_dict)
ChinaVoiceItem = UniversalItem()

# ====================正确动态生成 UniversalItem 类的方法================
# Item 类自带一个属性-Field 字典，代表着该 Item的所有属性及其类型为 Field
config = get_config('huashengnews')
UniversalItem = Item()
for key, value in config.get('item').get('attrs').items():
    UniversalItem.fields[key] = Field()
    print(UniversalItem.get(key))

UniversalItem['text'] = 'dsfsdf'
print(UniversalItem.get('text'))

{
    "link_extractor": {
        "restrict_xpaths": "//a[contains(., \"下一页\")]"
    }
}

# ======================换页测试=========================
# range() 可迭代对象
# list()对象迭代器
print(list(range(1, 10)))

config = get_config('huashengnews')
start_end = config.get("start_end")
step = config.get("step")
pagination_url = config.get("pagination_url")
print(range(start_end[0] + step, start_end[1] + step))
for pageNum in range(start_end[0] + step, start_end[1] + step, step):
    print(eval("f'"+pagination_url+"'"))
# 存入链接数组
# urls = [eval(pagination_url) for pageNum in range(start_end[0] + step, start_end[1] + step)]
# print(urls)

import requests
r = requests.get('https://www.bjnews.com.cn/detail/165940181114278.html')
r.encoding = 'Unicode'
print(r.text)

a = 'sdfsdfs'
b = "sdfsdfs"

print(id(a) == id(b))