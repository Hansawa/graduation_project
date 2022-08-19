from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# .. 代表上级模块，这里代表上级模块下的 utils 模块
from news_crawler.utils import get_config
from scrapy import Item, Field
# from scrapy.loader import ItemLoader
from news_crawler.universal.universal.loader import UniversalLoader

class UniversalSpider(CrawlSpider):
    name = 'universal'

    # 在实例化 spider 时初始化它的 rules，start_urls，allowed_domains，从配置文件中读取值
    def __init__(self, name, *args, **kwargs):
        # 获取爬虫配置
        config = get_config(name)
        self.config = config

        # 设置允许爬取的域名，不在该范围内的连接将会被忽略
        self.allowed_domains = config.get('allowed_domains')

        # 设置起始 url 列表，当 spider 类没有实现 start_requests 方法时，就会从这个列表开始抓取
        # 把用户构造的分页链接存放进 start_urls 列表即可实现控制爬取区间
        start_end = config.get("start_end")
        step = config.get("step")
        pagination_url = config.get("pagination_url")
        urls = config.get("start_urls")
        urls += [eval("f'"+pagination_url+"'") for pageNum in range(start_end[0] + step, start_end[1] + step) if start_end[1] != 1]
        self.start_urls = urls

        # 此为直接从 rules 模块获取对应的抓取逻辑
        # self.rules = rules.get(config.get('rules'))

        # 此为从爬虫配置文件中获取对应的抓取逻辑
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
        self.rules = rules

        # 相当于 super(UniversalSpider, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

    # 对爬取网站的 url 进行预处理（http -> https）
    def process_request(self, request, response):
        url_list = list(request.url)
        url_list.insert(4, 's')
        request._set_url(''.join(url_list))
        return request

    def parse_detail(self, response):
        item_dict = self.config.get('item')
        if item_dict:
            # 动态创建 UniversalItem 类
            UniversalItem = Item()
            for key, value in item_dict.get('attrs').items():
                UniversalItem.fields[key] = Field()
            UniversalItem.fields['collection'] = item_dict.get('collection')

            # loader = eval(item_dict.get('loader'))(item=UniversalItem, response=response)
            loader = UniversalLoader(item=UniversalItem, response=response)
            # 动态获取属性配置
            # dict.get()：返回键对应的值，如果没有该键，使用给定的默认值
            # dict.items()：返回可遍历的(键, 值) 元组数组
            for key, value in item_dict.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, xpath=extractor.get('arg'), re=extractor.get('re'))
                    if extractor.get('method') == 'css':
                        loader.add_css(key, css=extractor.get('arg'), re=extractor.get('re'))
                    if extractor.get('method') == 'value':
                        loader.add_value(key, value=extractor.get('arg'), re=extractor.get('re'))
                    if extractor.get('method') == 'respAttr':
                        loader.add_value(key, value=getattr(response, extractor.get('arg')))
            yield loader.load_item()
