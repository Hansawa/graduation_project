"""

"""
import re
import time
from collections.abc import Generator
from proxy_pool.crawlers.base_crawler import BaseCrawler
from proxy_pool.schemas.Proxy import Proxy


class IhuanCrawler(BaseCrawler):
    """

    """
    urls = [f'https://ip.ihuan.me/today/{time.strftime("%Y/%m/%d/%H", time.localtime())}.html']
    ignore = False
    
    def _parse(self, html: str) -> Generator:
        """

        :param html:
        :return:
        """
        results = re.findall(r'(\d+.\d+\.\d+\.\d+):(\d+)@', html)
        for result in results:
            yield Proxy(host=result[0], port=result[1])


if __name__ == '__main__':
    for proxy in IhuanCrawler().crawl():
        print(proxy)
