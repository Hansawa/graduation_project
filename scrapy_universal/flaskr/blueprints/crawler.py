from flask import Blueprint, request
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner, CrawlerProcess

from scrapy_universal.flaskr.utils import get_config

bp = Blueprint('crawler', __name__, url_prefix='/crawler')


@bp.route('/run', methods=['GET'])
def run_crawler():
    if request.method == 'GET':
        data = request.args
        env = data['env']

        if env == "dev":
            name = "chinanews"
            config = get_config(name)
            project_settings = get_project_settings()
            project_settings.update(config.get("settings"))
            process = CrawlerProcess(project_settings)
            process.crawl("universal", name=name)
            process.start()
            pass
        elif env == "serve":
            spiderNames = ["huashengnews", "chinanews", "xinjingnews"]
            project_settings = get_project_settings()
            runner_spiderName = {}
            for spiderName in spiderNames:
                config = get_config(spiderName)
                project_settings.update(config.get("settings"))
                runner = CrawlerRunner(project_settings)
                runner_spiderName[runner] = spiderName

            @defer.inlineCallbacks
            def crawl():
                for runner, spiderName in runner_spiderName.items():
                    yield runner.crawl("universal", name=spiderName)
                reactor.stop()
            crawl()
            reactor.run()
            pass
        elif env == "test":
            pass