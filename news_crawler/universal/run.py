from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from news_crawler.utils import get_config
from scrapy.crawler import CrawlerRunner, CrawlerProcess


def run(env):
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
    elif env == 'serve':
        spiderNames = ['huashengnews', 'chinanews', 'xinjingnews']
        project_settings = get_project_settings()
        runner_spiderName = {}
        for spiderName in spiderNames:
            config = get_config(spiderName)
            project_settings.update(config.get('settings'))
            runner = CrawlerRunner(project_settings)
            runner_spiderName[runner] = spiderName

        @defer.inlineCallbacks
        def crawl():
            for runner, spiderName in runner_spiderName.items():
                yield runner.crawl('universal', name=spiderName)
            reactor.stop()
        crawl()
        reactor.run()
        pass
    elif env == 'test':
        pass


if __name__ == '__main__':
    env = 'serve'
    run(env)
