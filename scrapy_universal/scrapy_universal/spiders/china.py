from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    # 1. 起始链接，爬虫程序从这个链接开始爬取
    start_urls = ['http://tech.china.com/articles/']

    # 2. 爬取规则（功能：定义起始链接指向的网页中哪些链接需要继续发出请求，哪些链接指向的网页需要用哪个方法解析）
    rules = (
        # 匹配所需链接所在的区域，指定该链接指向的网页的解析方法
        Rule(LinkExtractor(allow='article/.*\.html', restrict_xpaths='//div[@id="rank-defList"]'), callback='parse_item'),
        # 匹配所需链接所在的区域，设置向该链接继续发送请求
        # callback 为空时，follow 默认为 True
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]//a[contains(., "下一页")]'), process_request='process_request'),
    )

    def process_request(self, request, response):
        urlList = list(request.url)
        urlList.insert(4, 's')
        request._set_url(''.join(urlList)) 
        print(request.url)
        return request

    # 3. 创建解析出的数据的保存容器（类） item，该类对应与数据库的表头

    # 4. 解析网页，提取数据至 item 实例中并生成 item 
    def parse_item(self, response):
        i = {}
        return i
        # item = NewsItem()
        # item['title'] = response.xpath('//h1[@id="chan_newsTitle"]/text()').extract_first()
        # item['url'] = response.url
        # item['text'] = ''.join(response.xpath('//div[@id="chan_newsDetail"]//text()').extract()).strip()
        # item['datetime'] = response.css('div[class="chan_newsInfo_source"] span[class="time"]::text').extract_first()
        # item['source'] = response.css('div[class="chan_newsInfo_source"] span[class="source"]::text').extract_first()
        # item['website'] = ' 中华网 '
        # yield item
