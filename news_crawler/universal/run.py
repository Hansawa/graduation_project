from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
# from news_crawler.utils import get_config
from scrapy.crawler import CrawlerRunner, CrawlerProcess


def run(env, config_contents):
    try:
        if env == 'dev':
            pass
        elif env == 'test':
            config_content = config_contents
            spider_name = config_content['spider']
            project_settings = get_project_settings()
            project_settings.update(config_content['settings'])
            process = CrawlerProcess(project_settings)
            process.crawl(spider_name, config_content=config_content)
            process.start()
            pass
        elif env == 'serve':
            runner_config = {}
            for config_content in config_contents:
                project_settings = get_project_settings()
                project_settings.update(config_content.get('settings'))
                runner = CrawlerRunner(project_settings)
                runner_config[runner] = config_content
            @defer.inlineCallbacks
            def crawl():
                for runner, config_content in runner_config.items():
                    yield runner.crawl('universal', config_content=config_content)
                reactor.stop()
            crawl()
            reactor.run()
            pass
    except ValueError:
        print('error')
