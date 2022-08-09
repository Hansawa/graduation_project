"""

"""
from proxy_pool.storages.redis_client import RedisClient
from proxy_pool.utils.crawlers_util import CrawlersUtil


class Getter:
    """

    """

    def __init__(self):
        self.redis_client = RedisClient()
        self.crawlers_cls = CrawlersUtil.get_crawlers_cls()

    def run(self):
        """Get proxies and store them in redis

        Instance all the crawlers_cls and run their crawl() to get proxies then store the proxies in redis

        :return:
        """
        for crawler in self.crawlers_cls:
            for proxy in crawler().crawl():
                print(f'{proxy}')
                self.redis_client.add(proxy.to_string())


if __name__ == '__main__':
    Getter().run()
