# 爬取规则配置文件，将会动态加载到 spider 中
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'china': (
        Rule(LinkExtractor(allow='article/.*\.html', restrict_xpaths='//div[@id="rank-defList"]'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(., "下一页")]'), follow=True, process_request="process_request"),
    ),
    'huashengnews': (
        Rule(LinkExtractor(allow='article/.*\.html', restrict_xpaths='//div[@class="cont"]'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(., "下一页")]')),
    )
}
