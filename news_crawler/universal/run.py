from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from news_crawler.utils import get_config
from scrapy.crawler import CrawlerRunner, CrawlerProcess


def run(env, config_name, config_content):
    if env == 'dev':
        website_name = 'chinanews'
        spider_name = 'universal'
        config = get_config(website_name)
        project_settings = get_project_settings()
        project_settings.update(config.get('settings'))
        process = CrawlerProcess(project_settings)
        process.crawl(spider_name, name=website_name)
        process.start()
        pass
    elif env == 'test':
        spider_name = config_content['spider']
        project_settings = get_project_settings()
        project_settings.update(config_content['settings'])
        process = CrawlerProcess(project_settings)
        process.crawl(spider_name, config_content=config_content)
        process.start()
        pass
    elif env == 'serve':
        spider_name_list = ['huashengnews', 'chinanews', 'xinjingnews']
        project_settings = get_project_settings()
        runner_spidername = {}
        for spiderName in spider_name_list:
            config = get_config(spiderName)
            project_settings.update(config.get('settings'))
            runner = CrawlerRunner(project_settings)
            runner_spidername[runner] = spiderName

        @defer.inlineCallbacks
        def crawl():
            for runner, spider_name in runner_spidername.items():
                yield runner.crawl('universal', name=spider_name)
            reactor.stop()

        crawl()
        reactor.run()
        pass


if __name__ == '__main__':
    run('test', config_name='chinanews', config_content={
        "spider": "universal",
        "website": "中国新闻网",
        "type": "新闻",
        "index": "http://www.chinanews.com.cn/",
        "settings": {
            "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
            "DOWNLOAD_DELAY": 0,
            "RANDOMIZE_DOWNLOAD_DELAY": "True",
            "ROBOTSTXT_OBEY": "true",
            "MONGO_DB": "raw_news"
        },
        "allowed_domains": ["www.chinanews.com.cn"],
        "start_urls": ["http://www.chinanews.com.cn/scroll-news/news1.html"],
        "pagination_url": "http://www.chinanews.com.cn/scroll-news/news{pageNum}.html",
        "start_end": [1, 2],
        "step": 1,
        "rules": [
            {
                "link_extractor": {
                    "allow": "/\\w{2}/\\d{4}/\\d{2}-\\d{2}/.*\\.shtml",
                    "restrict_xpaths": "//div[@class=\"content_list\"]/ul"
                },
                "callback": "parse_detail"
            }
        ],
        "item": {
            "collection": "chinanews",
            "attrs": {
                "title": [
                    {
                        "method": "xpath",
                        "arg": "//div[@class=\"content_maincontent_more\"]//h1/text()"
                    }
                ],
                "url": [
                    {
                        "method": "respAttr",
                        "arg": "url"
                    }
                ],
                "text": [
                    {
                        "method": "xpath",
                        "arg": "//div[@class=\"content_maincontent_content\"]"
                    }
                ],
                "datetime": [
                    {
                        "method": "xpath",
                        "arg": "//div[@class=\"content_left_time\"]/text()"
                    }
                ],
                "website": [
                    {
                        "method": "value",
                        "arg": "中国新闻网"
                    }
                ]
            }
        }
    })
