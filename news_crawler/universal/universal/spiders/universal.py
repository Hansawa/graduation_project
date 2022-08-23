from abc import ABC
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from news_crawler.universal.universal.spiders.cls_creator import get_cls_universal_item, get_cls_universal_loader


class UniversalSpider(CrawlSpider, ABC):
    name = 'universal'
    config: dict
    allowed_domains: list
    start_urls: list
    rules: list
    UniversalItem: type
    UniversalLoader: type

    # 在实例化 spider 时初始化它的 rules，start_urls，allowed_domains，从配置文件中读取值
    def __init__(self, config_content, *args, **kwargs):
        # 获取爬虫配置
        config = config_content
        self.config = config

        # 设置允许爬取的域名，不在该范围内的连接将会被忽略
        self.allowed_domains = config.get('allowed_domains')

        # 设置起始 url 列表，当 spider 类没有实现 start_requests 方法时，就会从这个列表开始抓取
        # 把用户构造的分页链接存放进 start_urls 列表即可实现控制爬取区间
        start_end = config.get("start_end")
        step = config.get("step")
        pagination_url = config.get("pagination_url")
        urls = config.get("start_urls")
        urls += [eval("f'" + pagination_url + "'") for pageNum in range(start_end[0] + step, start_end[1] + step) if
                 start_end[1] != 1]
        self.start_urls = urls

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

        item = config.get('item')
        default_processor = item.get('default_processor')
        attrs = item.get('attrs')
        # 动态生成 UniversalItem 类
        self.UniversalItem = get_cls_universal_item(attrs)
        # 动态生成 UniversalLoader 类
        self.UniversalLoader = get_cls_universal_loader(default_processor, attrs)

        super(UniversalSpider, self).__init__(*args, **kwargs)

    # 对爬取网站的 url 进行预处理（http -> https）
    def process_request(self, request, response):
        url_list = list(request.url)
        url_list.insert(4, 's')
        request._set_url(''.join(url_list))
        return request

    def parse_detail(self, response):
        # 实例化 item 与 loader
        universal_item = self.UniversalItem()
        loader = self.UniversalLoader(item=universal_item, response=response)

        attrs = self.config.get('item').get('attrs')
        for key, value in attrs.items():
            for extractor in value.get('extractors'):
                if extractor.get('method') == 'xpath':
                    loader.add_xpath(key, xpath=extractor.get('arg'), re=extractor.get('re'))
                if extractor.get('method') == 'css':
                    loader.add_css(key, css=extractor.get('arg'), re=extractor.get('re'))
                if extractor.get('method') == 'value':
                    loader.add_value(key, value=extractor.get('arg'), re=extractor.get('re'))
                if extractor.get('method') == 'respAttr':
                    loader.add_value(key, value=getattr(response, extractor.get('arg')))
        yield loader.load_item()
