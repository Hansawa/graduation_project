"""Used for defining an abstract superclass of every crawler classes.

Typical usage example:
    from [<package_name>. ...]BaseCrawler import BaseCrawler
    class <crawler_name>(BaseCrawler):
        ...
"""
from abc import ABC, abstractmethod
from collections.abc import Generator
import requests
import time
# import requests.utils


class BaseCrawler(ABC):
    """An abstract superclass of every crawler classes.

    The template method pattern is used by this class.

    Attributes:
        urls: some urls which will be crawled.

    Methods:
        fetch():
        parse():
        crawl():
    """
    urls = []
    ignore = False

    def _fetch(self, url):
        """

        :param url: str
        :return: str
        """
        print(url)
        resp = requests.get(url=url)
        if resp.status_code == requests.codes.ok:
            # 从 html 文本中查找该文本使用的字符编码并赋值给 resp.encoding，
            # 让 resp.content 被解码时使用正确的字符编码进行解码
            # resp.encoding = requests.utils.get_encodings_from_content(resp.text)[0]
            return resp.text

    """Will be implement by subclass with rules of data extracting.

    :param html: str.
    :return: Generator of Proxy
    """
    @abstractmethod
    def _parse(self, html: str) -> Generator: ...

    def crawl(self) -> Generator:
        """template method of crawling.

        :return: Generator of Proxy
        """
        for url in self.urls:
            time.sleep(1)
            html = self._fetch(url=url)
            for proxy in self._parse(html):
                yield proxy


if __name__ == '__main__':
    pass
