"""

"""
from collections.abc import Generator
from proxy_pool.crawlers.base_crawler import BaseCrawler
from proxy_pool.schemas.Proxy import Proxy
import re

BASE_URL = 'http://www.ip3366.net/?stype=1&page={page}'


class Ip3366Crawler(BaseCrawler):
    """

    """
    urls = [BASE_URL.format(page=page) for page in range(1, 6)]
    ignore = True

    def _parse(self, html) -> Generator:
        """extract the host and port of Proxy from html text

        :param html: str
        :return: Generator of Proxy
        """
        results = re.findall(r'>(\d+\.\d+\.\d+\.\d+).*?>(\d+)', html, re.S)
        for result in results:
            yield Proxy(host=result[0], port=result[1])


if __name__ == '__main__':
    for proxy in Ip3366Crawler().crawl():
        print(proxy)
